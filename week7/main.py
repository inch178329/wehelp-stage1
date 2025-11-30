from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import mysql.connector
import os
from dotenv import load_dotenv

# ------------------- 載入環境變數 --------------------
load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "website")
SESSION_KEY = os.getenv("SECRET_KEY", "wehelp-week6-secret")

# ------------------- 雜湊加鹽設定（Argon2id） --------------------
pwd_hasher = PasswordHasher()

# ------------------- 預先載入資料（lifespan 管理 DB 連線） --------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    con = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME,
    )
    app.state.con = con
    print("資料庫連線完成")
    try:
        yield
    finally:
        con.close()
        print("斷開資料庫連線")

# ------------------- 宣告 FastAPI 物件 --------------------
app = FastAPI(lifespan=lifespan)

# 使用 SessionMiddleware 登入狀態管理
app.add_middleware(SessionMiddleware, secret_key=SESSION_KEY)

# 模板與靜態檔案路徑
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 小工具函式：拿資料庫連線
def get_db(request: Request):
    return request.app.state.con


# 小工具函式：取得目前登入使用者（從 session）
def get_current_user(request: Request):
    return request.session.get("user-info")

# ----------------------- API 本體 -------------------------

# ------------------- 首頁：註冊 + 登入表單 --------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request, msg: str | None = None):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "msg": msg,  # 多丟一個 msg 給模板
        },
    )


# ------------------- 註冊 /signup --------------------
@app.post("/signup")
def signup(
    request: Request,
    name: str = Form(""),
    email: str = Form(""),
    password: str = Form(""),
):
    # 簡單整理輸入
    name = (name or "").strip()
    email = (email or "").strip().lower()
    password = password or ""

    # 必填檢查（前端也會檢查，這裡再安全檢查一次）
    if not name or not email or not password:
        return RedirectResponse(
            url="/ohoh?msg=請完整填寫註冊資料",
            status_code=303,
        )

    con = get_db(request)
    cursor = con.cursor()

    # 檢查 email 是否已存在
    cursor.execute("SELECT id FROM member WHERE email = %s", (email,))
    row = cursor.fetchone()
    if row:
        cursor.close()
        return RedirectResponse(
            url="/ohoh?msg=重複的電子郵件",
            status_code=303,
        )

    # 雜湊密碼後寫入 DB
    hashed_password = pwd_hasher.hash(password)
    cursor.execute(
        "INSERT INTO member (name, email, password) VALUES (%s, %s, %s)",
        (name, email, hashed_password),
    )
    con.commit()
    cursor.close()

    # 註冊成功，帶一個 msg 回首頁
    return RedirectResponse(url="/?msg=signup_ok", status_code=303)



# ------------------- 登入 /login --------------------
@app.post("/login")
def login(
    request: Request,
    email: str = Form(""),
    password: str = Form(""),
):
    email = (email or "").strip().lower()
    password_input = password or ""

    con = get_db(request)
    cursor = con.cursor()
    cursor.execute(
        "SELECT id, name, email, password FROM member WHERE email = %s",
        (email,),
    )
    row = cursor.fetchone()
    cursor.close()

    # 找不到帳號
    if not row:
        return RedirectResponse(
            url="/ohoh?msg=電子郵件或密碼輸入錯誤",
            status_code=303,
        )

    user_id, name, db_email, db_password_hash = row

    # 驗證密碼
    try:
        pwd_hasher.verify(db_password_hash, password_input)
    except VerifyMismatchError:
        return RedirectResponse(
            url="/ohoh?msg=電子郵件或密碼輸入錯誤",
            status_code=303,
        )

    # 登入成功，寫入 session
    request.session["user-info"] = {
        "user_id": user_id,
        "name": name,
        "email": db_email,
    }

    return RedirectResponse(url="/member", status_code=303)


# ------------------- 登出 /logout --------------------
@app.get("/logout")
def logout(request: Request):
    request.session.pop("user-info", None)
    return RedirectResponse(url="/", status_code=303)


# ------------------- 會員頁 /member --------------------
@app.get("/member", response_class=HTMLResponse)
def member(request: Request):
    user = get_current_user(request)
    if not user:
        # 沒有登入：直接帶回首頁
        return RedirectResponse(url="/", status_code=303)

    con = get_db(request)
    cursor = con.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT
            message.id,
            message.member_id,
            member.name,
            message.content
        FROM message
        JOIN member ON message.member_id = member.id
        ORDER BY message.time DESC
        """
    )
    messages = cursor.fetchall()
    cursor.close()

    context = {
        "request": request,
        "user_name": user["name"],
        "user_id": user["user_id"],
        "messages": messages,
    }
    return templates.TemplateResponse("member.html", context)


# ------------------- 錯誤頁 /ohoh --------------------
@app.get("/ohoh", response_class=HTMLResponse)
def error_page(request: Request, msg: str = ""):
    return templates.TemplateResponse(
        "ohoh.html",
        {"request": request, "msg": msg},
    )


# ------------------- 建立留言 /createMessage --------------------
@app.post("/createMessage")
def create_message(
    request: Request,
    content: str = Form(""),
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=303)

    text = (content or "").strip()
    if not text:
        # 空白就不寫入，直接回會員頁
        return RedirectResponse(url="/member", status_code=303)

    con = get_db(request)
    cursor = con.cursor()
    cursor.execute(
        "INSERT INTO message (member_id, content) VALUES (%s, %s)",
        (user["user_id"], text),
    )
    con.commit()
    cursor.close()

    return RedirectResponse(url="/member", status_code=303)


# ------------------- 刪除留言 /deleteMessage --------------------
@app.post("/deleteMessage")
def delete_message(
    request: Request,
    message_id: int = Form(...),
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=303)

    con = get_db(request)
    cursor = con.cursor()
    # 只允許刪除自己的留言
    cursor.execute(
        "DELETE FROM message WHERE id = %s AND member_id = %s",
        (message_id, user["user_id"]),
    )
    con.commit()
    cursor.close()

    return RedirectResponse(url="/member", status_code=303)

# ------------------- 查詢會員資料 API --------------------
@app.get("/member/{member_id}")
def api_get_member(member_id: int, request: Request):
    # 會員專屬功能(有登入才給查)
    user = get_current_user(request)
    if not user:
        return {"data": None}

    con = get_db(request)
    # 查出目標會員的 id / name / email
    cursor = con.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, name, email FROM member WHERE id = %s",
        (member_id,),
    )
    row = cursor.fetchone()
    cursor.close()

    # 查不到就回 data: null
    if not row:
        return {"data": None}

    # 查到了，如果不是查自己，就寫一筆 search_log（Task4 需要）
    # search_log 的欄位是 target_id / executor_id / created_at
    if row["id"] != user["user_id"]:
        log_cursor = con.cursor()
        log_cursor.execute(
            "INSERT INTO search_log (target_id, executor_id) VALUES (%s, %s)",
            (row["id"], user["user_id"]),
        )
        con.commit()
        log_cursor.close()

    return {"data": row}

# -------------------更新會員姓名(JSON) --------------------
@app.patch("/api/member")
async def api_update_member(request: Request):
    user = get_current_user(request)
    if not user:
        return {"error": True}

    try:
        body = await request.json()
    except Exception:
        return {"error": True}

    new_name = (body.get("name") or "").strip()
    if not new_name:
        return {"error": True}

    con = get_db(request)
    cursor = con.cursor()
    cursor.execute(
        "UPDATE member SET name = %s WHERE id = %s",
        (new_name, user["user_id"]),
    )
    con.commit()
    cursor.close()

    # 更新 session 裡記錄的姓名，讓之後重新載入頁面會看到新名字
    user["name"] = new_name
    request.session["user-info"] = user

    return {"ok": True}

# ------------------- Week7：誰查詢了我 API --------------------
@app.get("/api/member/search_log")
def api_get_search_history(request: Request):
    user = get_current_user(request)
    if not user:
        # 規格沒特別講，沒登入就回空陣列
        return {"records": []}

    con = get_db(request)
    cursor = con.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT
            s.id,
            s.executor_id,
            m.name AS executor_name,
            s.created_at
        FROM search_log AS s
        JOIN member AS m
            ON s.executor_id = m.id
        WHERE s.target_id = %s
        ORDER BY s.created_at DESC
        LIMIT 10
        """,
        (user["user_id"],),
    )
    rows = cursor.fetchall()
    cursor.close()

    return {"records": rows}
