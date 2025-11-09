document.addEventListener('DOMContentLoaded', function () {
    // 檢查是否為「正整數」（不用正則）
    function isPositiveInteger(text) {
        let s = String(text).trim();
        if (s.length === 0) return false;         // 空字串不行
        for (let i = 0; i < s.length; i++) {      // 逐字檢查是否都是 0~9
            const c = s[i];
            if (c < '0' || c > '9') return false;
        }
        const n = Number(s);                      // 轉數字後必須 > 0
        if (!Number.isFinite(n)) return false;
        if (n <= 0) return false;
        return true;
    }

    // 登入：必須勾選同意條款
    const loginForm = document.querySelector('.login');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            const agree = document.getElementById('agree');
            if (!agree || !agree.checked) {
                e.preventDefault();
                alert('請勾選同意條款');
                return;
            }
        });
    }

    // 查詢旅館：檢查正整數，再導向 /hotel/{id}
    const searchForm = document.querySelector('.get-hotel');
    if (searchForm) {
        searchForm.addEventListener('submit', function (e) {
            e.preventDefault();
            let val = document.getElementById('hid').value;

            if (!isPositiveInteger(val)) {
                alert('請輸入正整數');
                return;
            }

            const id = Number(val.trim());
            window.location.assign('/hotel/' + id);
        });
    }
});
