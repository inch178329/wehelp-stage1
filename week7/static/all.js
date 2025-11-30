document.addEventListener("DOMContentLoaded", function () {
    // 讀取從後端傳來的 msg（透過 body 的 data-msg）
    const body = document.body;
    const msg = body.dataset.msg;  // 對應 <body data-msg="...">

    if (msg === "signup_ok") {
        alert("註冊成功，請重新登入");
    }

    // 註冊表單：必填檢查
    const signupForm = document.querySelector(".signup");
    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            let nameInput = document.getElementById("signup-name");
            let emailInput = document.getElementById("signup-email");
            let passwordInput = document.getElementById("signup-password");

            let nameValue = nameInput.value.trim();
            let emailValue = emailInput.value.trim();
            let passwordValue = passwordInput.value.trim();

            if (nameValue === "" || emailValue === "" || passwordValue === "") {
                event.preventDefault();
                alert("請完整填寫註冊資料");
            }
        });
    }

    // 登入表單：必填 + 同意條款
    const loginForm = document.querySelector(".login");
    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            let emailInput = document.getElementById("email");
            let passwordInput = document.getElementById("pwd");
            let agreeCheckbox = document.getElementById("agree");

            let emailValue = emailInput.value.trim();
            let passwordValue = passwordInput.value.trim();

            if (emailValue === "" || passwordValue === "") {
                event.preventDefault();
                alert("請輸入信箱與密碼");
                return;
            }

            if (!agreeCheckbox || !agreeCheckbox.checked) {
                event.preventDefault();
                alert("請勾選同意條款");
                return;
            }
        });
    }

    // 刪除留言：confirm 二次確認
    const deleteForms = document.querySelectorAll(".delete-message");
    for (let i = 0; i < deleteForms.length; i++) {
        let form = deleteForms[i];
        form.addEventListener("submit", function (event) {
            let ok = confirm("確定要刪除這則留言嗎？");
            if (!ok) {
                event.preventDefault();
            }
        });
    }
    // ---------------- Week7：查詢會員資料 ----------------
    const queryBtn = document.getElementById("query-btn");
    if (queryBtn) {
        queryBtn.addEventListener("click", async function () {
            const idInput = document.getElementById("query-id");
            const resultEl = document.getElementById("query-result");

            const id = idInput.value.trim();
            if (!id) {
                resultEl.textContent = "請先輸入會員編號";
                return;
            }

            try {
                const res = await fetch(`/member/${id}`);
                const data = await res.json();

                if (data.data) {
                    resultEl.textContent = `${data.data.name}（${data.data.email}）`;
                } else {
                    resultEl.textContent = "查無此會員資料";
                }
            } catch (e) {
                console.error(e);
                resultEl.textContent = "查詢失敗，請稍後再試";
            }
        });
    }

    // ---------------- Week7：更新User姓名 ----------------
    const updateBtn = document.getElementById("update-btn");
    if (updateBtn) {
        updateBtn.addEventListener("click", async function () {
            const nameInput = document.getElementById("update-name");
            const statusEl = document.getElementById("update-result");

            const newName = nameInput.value.trim();
            if (!newName) {
                statusEl.textContent = "姓名不可為空白";
                return;
            }

            try {
                const res = await fetch("/api/member", {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ name: newName }),
                });
                const data = await res.json();

                if (data.ok) {
                    statusEl.textContent = "更新成功";
                } else {
                    statusEl.textContent = "更新失敗";
                }
            } catch (e) {
                console.error(e);
                statusEl.textContent = "更新失敗，請稍後再試";
            }
        });
    }

    // ---------------- Week7：誰查詢了我 ----------------
    const historyBtn = document.getElementById("history-btn");
    if (historyBtn) {
        historyBtn.addEventListener("click", async function () {
            const listEl = document.getElementById("query-history");
            listEl.innerHTML = "";

            try {
                const res = await fetch("/api/member/search_log");
                const data = await res.json(); // { records: [...] }

                if (!data.records || data.records.length === 0) {
                    const li = document.createElement("li");
                    li.className = "message-item";
                    li.textContent = "目前沒有查詢紀錄";
                    listEl.appendChild(li);
                    return;
                }

                data.records.forEach(function (item) {
                    const li = document.createElement("li");
                    li.className = "message-item";
                    li.textContent = `${item.executor_name} 在 ${item.created_at} 查詢了你`;
                    listEl.appendChild(li);
                });
            } catch (e) {
                console.error(e);
                const li = document.createElement("li");
                li.className = "message-item";
                li.textContent = "載入失敗";
                listEl.appendChild(li);
            }
        });
    }
});