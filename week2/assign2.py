def func1(name):
    positions = {
        "悟空": {"x": 0, "y": 0, "z": 0},
        "丁滿": {"x": -1, "y": 4, "z": 1},
        "辛巴": {"x": -3, "y": 3, "z": 0},
        "貝吉塔": {"x": -4, "y": -1, "z": 0},
        "弗利沙": {"x": 4, "y": -1, "z": 1},
        "特南克斯": {"x": 1, "y": -2, "z": 0}
    }

    def distance(target, currentPosition):
        d = abs(target["x"] - currentPosition["x"]) + abs(target["y"] - currentPosition["y"])
        if (target["z"] != currentPosition["z"]):
            d += 2
        return d

    if (name not in positions):
        print("查無此人")
        return

    target = positions[name]
    distList = []

    for key in positions.keys():
        if (key == name):
            continue

        currentPosition = positions[key]
        d = distance(target, currentPosition)

        distList.append({"who": key, "dist": d})

    if (len(distList) == 0):
        return

    allDistances = list(map(lambda record: record["dist"], distList))

    maxDist = max(*allDistances)
    minDist = min(*allDistances)

    farthestRecords = list(filter(lambda record: record["dist"] == maxDist, distList))
    nearestRecords = list(filter(lambda record: record["dist"] == minDist, distList))

    farthestNames = list(map(lambda record: record["who"], farthestRecords))
    nearestNames = list(map(lambda record: record["who"], nearestRecords))

    farStr = "、".join(farthestNames)
    nearStr = "、".join(nearestNames)

    print(f"{name}：最遠{farStr}；最近{nearStr}")


print("=== Task 1 ===")
func1("辛巴")        # print 最遠弗利沙；最近丁滿、⾙吉塔
func1("悟空")        # print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙")      # print 最遠⾟巴，最近特南克斯
func1("特南克斯")    # print 最遠丁滿，最近悟空


schedule = {}

def func2(ss, start, end, criteria):
    def isAvailable(svcName, start, end):
        if (svcName not in schedule):
            return True
        for i in range(len(schedule[svcName])):
            book = schedule[svcName][i]
            bookedStart = book["start"]
            bookedEnd = book["end"]
            overlap = not (end <= bookedStart or start >= bookedEnd)
            if (overlap):
                return False
        return True

    def addBooking(svcName, start, end):
        if (svcName not in schedule):
            schedule[svcName] = []
        schedule[svcName].append({"start": start, "end": end})

    def parseCriteria(criteria):
        op = None
        field = None
        rawValue = None

        if (criteria.find(">=") != -1):
            op = ">="
            parts = criteria.split(">=")
            field = parts[0]
            rawValue = parts[1]
        elif (criteria.find("<=") != -1):
            op = "<="
            parts = criteria.split("<=")
            field = parts[0]
            rawValue = parts[1]
        else:
            op = "="
            parts = criteria.split("=")
            field = parts[0]
            rawValue = parts[1]

        field = field.strip()
        rawValue = rawValue.strip()

        if (field == "name"):
            value = rawValue
        else:
            value = float(rawValue)

        return {
            "field": field,
            "op": op,
            "value": value
        }

    def matchService(s, cond):
        fv = s[cond["field"]]

        if (cond["op"] == "="):
            return fv == cond["value"]
        elif (cond["op"] == ">="):
            return fv >= cond["value"]
        elif (cond["op"] == "<="):
            return fv <= cond["value"]
        return False

    def pickBest(candidates, cond):
        if (len(candidates) == 0):
            return None

        if (cond["op"] == "=" and cond["field"] == "name"):
            sorted_list = sorted(candidates, key=lambda x: x["name"])
            return sorted_list[0]

        if (cond["op"] == ">="):
            sorted_list = sorted(
                candidates,
                key=lambda x: (x[cond["field"]], x["name"])
            )
            return sorted_list[0]

        if (cond["op"] == "<="):
            sorted_list = sorted(
                candidates,
                key=lambda x: (-x[cond["field"]], x["name"])
            )
            return sorted_list[0]
        return None

    cond = parseCriteria(criteria)

    matchedAvailableList = list(filter(
        lambda svc: (isAvailable(svc["name"], start, end) and matchService(svc, cond)),
        ss
    ))

    chosen = pickBest(matchedAvailableList, cond)

    if (not chosen):
        print("Sorry")
        return
    print(chosen["name"])
    addBooking(chosen["name"], start, end)


services = [
    {"name": "S1", "r": 4.5, "c": 1000},
    {"name": "S2", "r": 3, "c": 1200},
    {"name": "S3", "r": 3.8, "c": 800}
]

print("=== Task 2 ===")
func2(services, 15, 17, "c>=800")     # S3
func2(services, 11, 13, "r<=4")       # S3
func2(services, 10, 12, "name=S3")    # Sorry
func2(services, 15, 18, "r>=4.5")     # S1
func2(services, 16, 18, "r>=4")       # Sorry
func2(services, 13, 17, "name=S1")    # Sorry
func2(services, 8, 9, "c<=1500")      # S2


def func3(index):
    ary = []
    newValue = 25
    aryRules = [-2, -3, +1, +2]

    for i in range(0, index + 1):
        ary.append(newValue)
        rule = aryRules[i % len(aryRules)]
        newValue = newValue + rule

    print(ary[index])


print("=== Task 3 ===")
func3(1)    # print 23
func3(5)    # print 21
func3(10)   # print 16
func3(30)   # print 6


def func4(sp, stat, n):
    bestFitLeft = float("inf")
    bestFitIdx = -1
    fallbackCap = -1
    fallbackIdx = -1

    for i in range(len(sp)):
        if (stat[i] == '1'):
            continue
        cap = sp[i]
        left = cap - n
        if (cap >= n):
            if (left < bestFitLeft):
                bestFitIdx = i
                bestFitLeft = left

        if (cap > fallbackCap):
            fallbackCap = cap
            fallbackIdx = i

    ans = fallbackIdx if (bestFitIdx == -1) else bestFitIdx
    print(ans)


print("=== Task 4 ===")
func4([3, 1, 5, 4, 3, 2], "101000", 2)     # print 5
func4([1, 0, 5, 1, 3], "10100", 4)        # print 4
func4([4, 6, 5, 8], "1000", 4)            # print 2
