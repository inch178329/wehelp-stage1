document.addEventListener("DOMContentLoaded", function () {
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
});