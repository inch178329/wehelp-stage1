import urllib.request as request
import json
import csv

hotelSrcZh="https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
hotelSrcEn="https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

def getHotelData(src):
    with request.urlopen(src) as response:
        return json.load(response)

def getDistrictName(address):
    if "區" in address:
        index_of_district = address.find("區")
        return address[ 3 : 6 ]

dataZh = getHotelData(hotelSrcZh)
dataEn = getHotelData(hotelSrcEn)

hotelOriginListZh = dataZh["list"]
hotelOriginListEn = dataEn["list"]
# print("中文旅館筆數：", len(hotelOriginListZh))
# print("英文旅館筆數：", len(hotelOriginListEn))
# print("中文第一筆原始資料：", hotelOriginListZh[0])
# print("英文第一筆原始資料：", hotelOriginListEn[0])

hotelPickedListZh = [
    {
        "_id": hotelData.get("_id"),
        "name": hotelData.get("旅宿名稱"),
        "address": hotelData.get("地址"),
        "tel": hotelData.get("電話或手機號碼"),
        "rooms": hotelData.get("房間數"),
    }
    for hotelData in hotelOriginListZh
]
print(hotelPickedListZh[0])

hotelPickedListEn = [
    {
        "_id": hotelData.get("_id"),
        "name": hotelData.get("hotel name"),
        "address": hotelData.get("address"),
        "tel": hotelData.get("tel"),
        "rooms": hotelData.get("the total number of rooms"),
    }
    for hotelData in hotelOriginListEn
]
print(hotelPickedListEn[0])

# 照id順序排序

hotelPickedListZh = sorted(
    hotelPickedListZh, 
    key=lambda x: x.get("_id", 0)
)

# 建英文索引
en_by_id = {}
for e in hotelPickedListEn:
    _id = e.get("_id")
    if _id is not None:
        en_by_id[_id] = e

# 合併與組列
rows = []
for z in hotelPickedListZh:
    z_id = z.get("_id")
    e = en_by_id.get(z_id, {})   # 找不到英文對應就用空字典

    row = [
        z.get("name", ""),       # ChineseName
        e.get("name", ""),       # EnglishName
        z.get("address", ""),    # ChineseAddress
        e.get("address", ""),    # EnglishAddress
        (z.get("tel") or e.get("tel") or ""),           # Phone
        (z.get("rooms") or e.get("rooms") or ""),       # RoomCount
    ]
    rows.append(row)             # JS: rows.push(row)
print("開始進行輸出")
with open ("hotels.csv","w",encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["ChineseName", "EnglishName", "ChineseAddress", "EnglishAddress", "Phone", "RoomCount"])
    for row in rows:
        writer.writerow(row)
print("資料輸出完成至hotels.csv")


print("\n開始進行行政區統計與輸出")

districtStats = {}

for hotel in hotelPickedListZh:
    districtName = getDistrictName(hotel.get("address", ""))
    
    # 房間數如果怪怪的就視為0
    try:
        roomCount = int(hotel.get("rooms") or 0)
    except (ValueError, TypeError):
        roomCount = 0

    if districtName not in districtStats:
        districtStats[districtName] = {
            "HotelCount": 0,
            "RoomCount": 0
        }
    
    # 進行累計
    districtStats[districtName]["HotelCount"] += 1
    districtStats[districtName]["RoomCount"] += roomCount

# 將字典轉換成列表，準備排序
districtRows = [
    [district, stats["HotelCount"], stats["RoomCount"]]
    for district, stats in districtStats.items()
]

# 排序
districtRowsSorted = sorted(
    districtRows, 
    key=lambda x: x[0]
)
# 輸出
with open ("districts.csv","w",encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["DistrictName", "HotelCount", "RoomCount"])
    for row in districtRowsSorted:
        writer.writerow(row)
        
print("行政區資料輸出完成至districts.csv")




