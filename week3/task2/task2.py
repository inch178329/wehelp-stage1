import urllib.request as req
import http.cookiejar as cookiejar
import bs4
import csv
import time      # time 模組
import random    # random 模組 

PTT_HOST = "https://www.ptt.cc"
start_url = PTT_HOST +"/bbs/Steam/index.html"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
cj = cookiejar.CookieJar()
opener = req.build_opener(req.HTTPCookieProcessor(cj))
opener.addheaders = [("User-Agent", UA)]

def get_soup(url):
    with opener.open(url) as resp:
        html = resp.read().decode("utf-8")
    return bs4.BeautifulSoup(html, "html.parser")

soups = []
url = start_url
for i in range(3):
    print(f"--- 正在抓取第 {i+1} 頁: {url} ---")
    try:
        s = get_soup(url)
        soups.append(s)
    except Exception as e:
        print(f"抓取頁面失敗 ({url}): {e}")
        break # 抓取失敗則停止

    # 避免頻繁請求備索，模擬人類瀏覽行為
    # 隨機延遲 3 到 5 秒
    sleep_time = random.uniform(3, 5)
    print(f"--> 完成。等待 {sleep_time:.2f} 秒...")
    time.sleep(sleep_time)

    # 找到「上頁」連結，準備下一輪
    next_url = None
    for a in s.select("div.btn-group.btn-group-paging a"):
        if "上頁" in a.get_text(strip=True):
            next_url = PTT_HOST + a.get("href")
            break
    if next_url is None:
        break
    url = next_url

rows = []
for s_index, s in enumerate(soups):
    print(f"\n--- 解析第 {s_index+1} 頁的 {len(s.select('div.r-ent'))} 篇文章連結 ---")
    for ent in s.select("div.r-ent"):
        title_div = ent.find("div", class_="title")
        # 刪文/無連結直接跳過
        if not title_div or not title_div.a:
            continue

        title = title_div.a.get_text(strip=True)
        article_url = PTT_HOST + title_div.a.get("href")

        # 推文數：只有純數字才計入，其他（爆、X1、空白）視為 0
        nrec = ent.find("div", class_="nrec")
        raw = (nrec.get_text(strip=True) if nrec else "").upper()
        like = int(raw) if raw.isdigit() else 0

        # 進文章頁抓「時間」
        publish_time = ""
        try:
            article = get_soup(article_url)
            print(f"  - 正在抓取內文: {title[:15]}...")
            
            sleep_time = random.uniform(3, 5)
            time.sleep(sleep_time) 

            for tag in article.select("span.article-meta-tag"):
                if tag.get_text(strip=True) == "時間":
                    val = tag.find_next_sibling("span", class_="article-meta-value")
                    publish_time = val.get_text(strip=True) if val else ""
                    break
        except Exception as e:
            publish_time = ""  
            print(f"  - 抓取文章時間失敗 ({article_url}): {e}")

        rows.append([title, like, publish_time])

OUTPUT_FILENAME = "articles.csv"
with open(OUTPUT_FILENAME, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["ArticleTitle", "LikeCount", "PublishTime"])
    w.writerows(rows)

print(f"\n✅ 完成！已寫入 {len(rows)} 筆資料到 {OUTPUT_FILENAME}")