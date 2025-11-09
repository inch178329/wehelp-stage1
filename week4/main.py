from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import urllib.request as url_request
import json

# ---- 啟動時先把資料抓好（中英兩份合併成查表） ----
URL_CH = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
URL_EN = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

with url_request.urlopen(URL_CH) as resp:
    data_ch = json.loads(resp.read().decode("utf-8"))["list"]
with url_request.urlopen(URL_EN) as resp:
    data_en = json.loads(resp.read().decode("utf-8"))["list"]

# 以 _id 建立英文名稱對照，再組合單一輸出字串「中文、英文、電話」
en_by_id = {e["_id"]: e.get("hotel name", "") for e in data_en}
hotel_info = {}
for c in data_ch:
    _id = c["_id"]
    zh_name = c.get("旅宿名稱", "")
    en_name = en_by_id.get(_id, "")
    phone = c.get("電話或手機號碼", "")
    hotel_info[_id] = f"{zh_name}、{en_name}、{phone}"

# ---- FastAPI 基本設定 ----
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="wehelp-week4-secret") 

# ---- 連接前端三件套 ----
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ---- 路由 ----
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request},status_code=200)

@app.post("/login")
async def login(request: Request, email: str = Form(), password: str = Form()):
    if email == "abc@abc.com" and password == "abc":
        request.session["LOGGED_IN"] = True
        return RedirectResponse(url="/member", status_code=303)
    else:
        return RedirectResponse(url="/ohoh?msg=帳號、或密碼輸入錯誤", status_code=303)

@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    if request.session.get("LOGGED_IN"):
        return templates.TemplateResponse("member.html", {"request": request}, status_code=200)
    return RedirectResponse(url="/", status_code=303)

@app.get("/logout")
async def logout(request: Request):
    request.session["LOGGED_IN"] = False
    return RedirectResponse(url="/", status_code=303)

@app.get("/ohoh", response_class=HTMLResponse)
async def ohoh(request: Request, msg):
    return templates.TemplateResponse("ohoh.html", {"request": request, "msg": msg}, status_code=200)

@app.get("/hotel/{hotel_id}", response_class=HTMLResponse)
async def hotel(request: Request, hotel_id: str):
    # 僅接受正整數 id
    try:
        hid = int(hotel_id)
        if hid <= 0:
            raise ValueError
    except Exception:
        return templates.TemplateResponse(
            "hotel.html",
            {"request": request, "information": "查詢不到相關資料"},
            status_code=404
        )
    information = hotel_info.get(hid, "查詢不到相關資料")
    status = 200 if information != "查詢不到相關資料" else 404
    return templates.TemplateResponse(
        "hotel.html",
        {"request": request, "information": information},
        status_code=status
    )