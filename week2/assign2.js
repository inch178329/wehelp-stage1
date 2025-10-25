function func1(name) {
    let positions = {
        "悟空": { x: 0, y: 0, z: 0 },
        "丁滿": { x: -1, y: 4, z: 1 },
        "辛巴": { x: -3, y: 3, z: 0 },
        "貝吉塔": { x: -4, y: -1, z: 0 },
        "弗利沙": { x: 4, y: -1, z: 1 },
        "特南克斯": { x: 1, y: -2, z: 0 }
    };

    function distance(target, currentPosition) {
        let d = Math.abs(target.x - currentPosition.x) + Math.abs(target.y - currentPosition.y)
        if (target.z !== currentPosition.z) {
            d += 2;
        }
        return d;
    }
    // position名單以外的人不給測
    if (!positions[name]) {
        console.log("查無此人");
        return;
    }

    let target = positions[name];
    let distList = [];

    Object.keys(positions).forEach(function (key) {
        // 不自己減自己
        if (key === name) {
            return;
        }

        const currentPosition = positions[key];
        const d = distance(target, currentPosition);

        distList.push({ who: key, dist: d });
    });

    if (distList.length === 0) return;

    const allDistances = distList.map(function (record) {
        return record.dist;
    });

    // 把他切分成可以計算的數值
    const maxDist = Math.max(...allDistances);
    const minDist = Math.min(...allDistances);

    const farthestRecords = distList.filter(function (record) {
        return record.dist === maxDist;
    });
    const nearestRecords = distList.filter(function (record) {
        return record.dist === minDist;
    });

    const farthestNames = farthestRecords.map(function (record) {
        return record.who;
    });
    const nearestNames = nearestRecords.map(function (record) {
        return record.who;
    });

    const farStr = farthestNames.join("、");
    const nearStr = nearestNames.join("、");

    console.log(`${name}：最遠${farStr}；最近${nearStr}`);
}
console.log("=== Task 1 ===");
func1("辛巴");  // print 最遠弗利沙；最近丁滿、⾙吉塔
func1("悟空");  // print 最遠丁滿、弗利沙；最近特南克斯
func1("弗利沙");  // print 最遠⾟巴，最近特南克斯
func1("特南克斯");  // print 最遠丁滿，最近悟空


const schedule = {};

function func2(ss, start, end, criteria) {
    function isAvailable(svcName, start, end) {
        if (!schedule[svcName]) {
            return true;
        }
        for (let i = 0; i < schedule[svcName].length; i++) {
            const book = schedule[svcName][i];
            const bookedStart = book.start;
            const bookedEnd = book.end;
            const overlap = !(end <= bookedStart || start >= bookedEnd);
            if (overlap) {
                return false;
            }
        }
        return true;
    }

    function addBooking(svcName, start, end) {
        if (!schedule[svcName]) {
            schedule[svcName] = [];
        }
        schedule[svcName].push({ start: start, end: end });
    }

    function parseCriteria(criteria) {
        let op;
        let field;
        let rawValue;

        if (criteria.indexOf(">=") !== -1) {
            op = ">=";
            [field, rawValue] = criteria.split(">=");
        } else if (criteria.indexOf("<=") !== -1) {
            op = "<=";
            [field, rawValue] = criteria.split("<=");
        } else {
            op = "=";
            [field, rawValue] = criteria.split("=");
        }

        field = field.trim();
        rawValue = rawValue.trim();

        let value;
        if (field === "name") {
            value = rawValue;
        } else {
            value = Number(rawValue);
        }

        return {
            field: field,
            op: op,
            value: value
        };
    }

    function matchService(s, cond) {
        const fv = s[cond.field];

        if (cond.op === "=") {
            return fv === cond.value;
        } else if (cond.op === ">=") {
            return fv >= cond.value;
        } else if (cond.op === "<=") {
            return fv <= cond.value;
        }
        return false;
    }

    function pickBest(candidates, cond) {
        if (candidates.length === 0) {
            return null;
        }

        if (cond.op === "=" && cond.field === "name") {
            candidates.sort(function (a, b) {
                if (a.name < b.name) return -1;
                if (a.name > b.name) return 1;
                return 0;
            });
            return candidates[0];
        }

        if (cond.op === ">=") {
            candidates.sort(function (a, b) {
                let diff = a[cond.field] - b[cond.field]; // 小到大
                if (diff !== 0) return diff;
                // tie-break 用名字字母序
                if (a.name < b.name) return -1;
                if (a.name > b.name) return 1;
                return 0;
            });
            return candidates[0];
        }

        if (cond.op === "<=") {
            candidates.sort(function (a, b) {
                let diff = b[cond.field] - a[cond.field]; // 大到小
                if (diff !== 0) return diff;
                if (a.name < b.name) return -1;
                if (a.name > b.name) return 1;
                return 0;
            });
            return candidates[0];
        }
    }

    const cond = parseCriteria(criteria);
    const matchedAvailableList = ss.filter(function (svc) {
        return isAvailable(svc.name, start, end) && matchService(svc, cond);
    });

    const chosen = pickBest(matchedAvailableList, cond);

    if (!chosen) {
        console.log("Sorry");
        return;
    }
    console.log(chosen.name);
    addBooking(chosen.name, start, end);
}


const services = [
    { "name": "S1", "r": 4.5, "c": 1000 },
    { "name": "S2", "r": 3, "c": 1200 },
    { "name": "S3", "r": 3.8, "c": 800 }
];

console.log("=== Task 2 ===");
func2(services, 15, 17, "c>=800");    // S3
func2(services, 11, 13, "r<=4");      // S3
func2(services, 10, 12, "name=S3");   // Sorry
func2(services, 15, 18, "r>=4.5");    // S1
func2(services, 16, 18, "r>=4");      // Sorry
func2(services, 13, 17, "name=S1");   // Sorry
func2(services, 8, 9, "c<=1500");     // S2


function func3(index) {
    let ary = [];
    let newValue = 25;
    let aryRules = [-2, -3, +1, +2];

    for (let i = 0; i <= index; i++) {
        ary.push(newValue);
        let rule = aryRules[i % aryRules.length];
        newValue = newValue + rule;
    }
    console.log(ary[index]);

}
console.log("=== Task 3 ===");
func3(1);  // print 23 
func3(5);  // print 21 
func3(10);  // print 16 
func3(30);  // print 6

function func4(sp, stat, n) {

    let bestFitLeft = Infinity;
    let bestFitIdx = -1;
    let fallbackCap = -1;
    let fallbackIdx = -1;

    for (let i = 0; i < sp.length; i++) {
        // 1 for invalid, continue fot skip this turn
        if (stat[i] == '1') {
            continue;
        }
        /* 迴圈用到了遍歷搜尋演算法的概念，也就是說
        當您的目標是「遍歷所有選項，並選出一個最佳選項」時，您必須在迴圈開始前建立一個「記錄器」，這個記錄器需要記錄兩件事：最佳值 (Value) 和 最佳值的索引 (Index)。
        這四個變數就是針對兩套不同的選擇標準（最佳解best fit和備選fallback）所建立的兩組「記錄器」。 */
        let cap = sp[i];
        let left = cap - n;
        //最佳解，車廂有適當的空位的(不用坐在人家大腿上) 
        if (cap >= n) {
            if (left < bestFitLeft) {
                bestFitIdx = i;
                bestFitLeft = left;
            }
        }
        // 備選，有位子坐就好了，但還是要全部都看過一次
        if (cap > fallbackCap) {
            fallbackCap = cap;
            fallbackIdx = i;
        }
    }
    let ans = (bestFitIdx == -1) ? fallbackIdx : bestFitIdx;
    console.log(ans);

}
console.log("=== Task 4 ===");
func4([3, 1, 5, 4, 3, 2], "101000", 2);  // print 5 
func4([1, 0, 5, 1, 3], "10100", 4);  // print 4 
func4([4, 6, 5, 8], "1000", 4);  // print 2 