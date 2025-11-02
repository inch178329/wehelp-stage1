const DATA_URL_NAME = "https://cwpeng.github.io/test/assignment-3-1";
const DATA_URL_IMAGE = "https://cwpeng.github.io/test/assignment-3-2";
const FALLBACK_IMAGE = "./images/IMG_6779.png";
const STAR_ICON = "./images/285661_star_icon.png";

function toHttpsAbsolute(url, hostFromApi) {
    if (!url || typeof url !== "string") return "";
    let u = url.trim();
    if (u.startsWith("http://")) u = "https://" + u.slice(7);     // http → https
    if (u.startsWith("/")) u = (hostFromApi || "https://www.travel.taipei") + u; // 加 host
    return u;
}

function isImageUrl(u) {
    if (!u || typeof u !== "string") return false;
    let lower = u.toLowerCase();
    return (
        lower.endsWith(".jpg") ||
        lower.endsWith(".jpeg") ||
        lower.endsWith(".png") ||
        lower.endsWith(".gif") ||
        lower.endsWith(".webp")
    );
}

function getFirstImageFromPics(pics, hostFromApi) {
    // A. 陣列格式
    if (Array.isArray(pics)) {
        for (let i = 0; i < pics.length; i++) {
            let p = pics[i];
            if (p && typeof p === "object") {
                let candidate = p.url || p.src || "";
                candidate = toHttpsAbsolute(candidate, hostFromApi);
                if (isImageUrl(candidate)) return candidate;
            }
            if (typeof p === "string") {
                let candidate = toHttpsAbsolute(p, hostFromApi);
                if (isImageUrl(candidate)) return candidate;
            }
        }
        return "";
    }

    if (typeof pics === "string") {
        let s = pics.trim();
        let ends = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG", ".gif", ".GIF", ".webp", ".WEBP"];
        let endPos = -1;
        let endExt = "";
        for (let i = 0; i < ends.length; i++) {
            let pos = s.indexOf(ends[i]);
            if (pos !== -1) {
                if (endPos === -1 || pos < endPos) {
                    endPos = pos;
                    endExt = ends[i];
                }
            }
        }
        if (endPos !== -1) {
            let fragment = s.slice(0, endPos + endExt.length);
            let absolute = toHttpsAbsolute(fragment, hostFromApi);
            if (isImageUrl(absolute)) return absolute;
        }
        return "";
    }

    return "";
}

function pickNameArray(json) {
    if (Array.isArray(json)) return json;
    if (json && Array.isArray(json.rows)) return json.rows;
    if (json && json.data && Array.isArray(json.data.results)) return json.data.results;
    if (json && json.result && Array.isArray(json.result.results)) return json.result.results;
    return [];
}

function pickSerial(item) {
    if (!item) return "";
    let keys = ["serial", "SERIAL_NO", "SERIAL", "id", "Id", "ID"];
    for (let i = 0; i < keys.length; i++) {
        let k = keys[i];
        if (typeof item[k] === "string" && item[k]) return item[k];
        if (typeof item[k] === "number") return String(item[k]);
    }
    return "";
}
function pickTitle(item) {
    if (!item) return "未命名景點";
    let keys = ["stitle", "sname", "title", "name", "SName", "Name"];
    for (let i = 0; i < keys.length; i++) {
        let k = keys[i];
        if (typeof item[k] === "string" && item[k].trim() !== "") return item[k];
    }
    return "未命名景點";
}

function clearNode(node) {
    while (node && node.firstChild) node.removeChild(node.firstChild);
}
function createBarBox(attraction, index) {
    let box = document.createElement("div");
    box.className = "p" + (index + 1);

    let img = document.createElement("img");
    img.className = "proImg";
    img.src = attraction.image || FALLBACK_IMAGE;
    img.alt = attraction.title;

    let span = document.createElement("span");
    span.className = "bar-title";
    span.textContent = attraction.title;

    box.appendChild(img);
    box.appendChild(span);
    return box;
}
function createCard(attraction) {
    let card = document.createElement("div");
    card.className = "card";

    let img = document.createElement("img");
    img.className = "dog";
    img.src = attraction.image || FALLBACK_IMAGE;
    img.alt = attraction.title;

    let title = document.createElement("div");
    title.className = "title";
    title.textContent = attraction.title;

    let star = document.createElement("img");
    star.className = "star";
    star.src = STAR_ICON;
    star.alt = "favorite";

    card.appendChild(img);
    card.appendChild(title);
    card.appendChild(star);
    return card;
}

async function init() {
    let promotions = document.querySelector(".promotions");
    let gallery = document.querySelector(".gallery");
    clearNode(promotions);
    clearNode(gallery);

    let imageMap = new Map();
    let hostFromApi = "https://www.travel.taipei";
    try {
        let resImg = await fetch(DATA_URL_IMAGE);
        let jsonImg = await resImg.json();
        if (jsonImg && typeof jsonImg.host === "string") hostFromApi = jsonImg.host;

        let imageRows = [];
        if (Array.isArray(jsonImg)) imageRows = jsonImg;
        else if (Array.isArray(jsonImg.rows)) imageRows = jsonImg.rows;
        else if (jsonImg && jsonImg.data && Array.isArray(jsonImg.data.results)) imageRows = jsonImg.data.results;
        else if (jsonImg && jsonImg.result && Array.isArray(jsonImg.result.results)) imageRows = jsonImg.result.results;

        for (let i = 0; i < imageRows.length; i++) {
            let row = imageRows[i];
            let serial = pickSerial(row);
            let pics = (row.pics !== undefined) ? row.pics : ((row.file !== undefined) ? row.file : "");
            let first = getFirstImageFromPics(pics, hostFromApi);
            if (serial && first) imageMap.set(serial, first);
        }
    } catch (err) {
        console.error("抓取圖片資料失敗：", err);
    }

    let combined = [];
    try {
        let resName = await fetch(DATA_URL_NAME);
        let jsonName = await resName.json();
        let nameList = pickNameArray(jsonName);

        for (let i = 0; i < nameList.length; i++) {
            let it = nameList[i];
            let serial = pickSerial(it);
            let title = pickTitle(it);
            let image = imageMap.get(serial) || FALLBACK_IMAGE;
            combined.push({ serial, title, image });
        }
    } catch (err) {
        console.error("抓取名稱資料失敗：", err);
    }

    if (combined.length === 0) return;

    let top3 = combined.slice(0, 3);
    let next10 = combined.slice(3, 13);

    let fragBars = document.createDocumentFragment();
    for (let i = 0; i < top3.length; i++) {
        fragBars.appendChild(createBarBox(top3[i], i));
    }
    promotions.appendChild(fragBars);

    let fragCards = document.createDocumentFragment();
    for (let i = 0; i < next10.length; i++) {
        fragCards.appendChild(createCard(next10[i]));
    }
    gallery.appendChild(fragCards);
}

document.addEventListener("DOMContentLoaded", init);
