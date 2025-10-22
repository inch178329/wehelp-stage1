




function func3(index) {
    let ary = [];
    let newValue = 25;
    let aryRules = [-2,-3,+1,+2];
    
    for (let i = 0; i < 50; i++) {
        ary.push(newValue);
        let rule = aryRules[i%aryRules.length];
        newValue = newValue+rule;
    }
    console.log(ary[index]);
    
}
console.log("=== Task 3 ===");
func3(1);  // print 23 
func3(5);  // print 21 
func3(10);  // print 16 
func3(30);  // print 6