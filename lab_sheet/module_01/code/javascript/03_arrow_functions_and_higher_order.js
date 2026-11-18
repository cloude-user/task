/**
 * 03_arrow_functions_and_higher_order.js
 * =======================================
 * Topic: Arrow Functions (() => {}) and Higher-Order Function Wrappers
 * Analogy: The Express Scooter & The Security Checkpoint
 *
 * ANALOGY FOR STUDENTS:
 * ---------------------
 * 1. Traditional function () {} = The Heavy Passenger Bus.
 *    - Carries its own 'this' luggage, requires explicit return keyword for multi-line.
 * 2. Arrow Function () => {} = The Lightweight Electric Scooter.
 *    - Quick, fast, single-expression returns implicitly!
 *    - JavaScript's equivalent to Python's lambda function!
 * 3. Higher-Order Functions = The Airport Baggage Scanner (Decorators in JS!).
 *    - A function that wraps another function to add timing, retries, or auth.
 */

console.log("=".repeat(70));
console.log("⚡ PART 1: ARROW FUNCTIONS vs REGULAR FUNCTIONS");
console.log("=".repeat(70));

// Regular function
function addVatRegular(price) {
    return price * 1.18;
}

// Arrow function (Single-line: implicit return)
const addVatArrow = price => price * 1.18;

console.log("Regular function:", addVatRegular(100));
console.log("Arrow function:  ", addVatArrow(100));


console.log("\n" + "=".repeat(70));
console.log("📊 PART 2: ARRAY PIPELINES (.map, .filter, .reduce, .sort)");
console.log("=".repeat(70));

const ec2Fleet = [
    { id: "i-01", type: "t3.large", cost: 0.0832, state: "running" },
    { id: "i-02", type: "t2.nano",  cost: 0.0058, state: "stopped" },
    { id: "i-03", type: "t3.micro", cost: 0.0208, state: "running" },
    { id: "i-04", type: "c5.xlarge", cost: 0.1700, state: "running" }
];

// 1. Sort by cost ascending using arrow function:
ec2Fleet.sort((a, b) => a.cost - b.cost);
console.log("Fleet sorted by price (cheapest first):");
ec2Fleet.forEach(inst => console.log(`  • ${inst.id} (${inst.type}): $${inst.cost}/hr`));

// 2. Filter running instances only:
const runningNodes = ec2Fleet.filter(inst => inst.state === "running");
console.log("\nRunning instances count:", runningNodes.length);

// 3. Reduce: Calculate total hourly burn rate of all running instances:
const totalHourlyBurn = runningNodes.reduce((sum, inst) => sum + inst.cost, 0);
console.log(`Total Hourly Cost: $${totalHourlyBurn.toFixed(4)}/hr`);


console.log("\n" + "=".repeat(70));
console.log("🛂 PART 3: HIGHER-ORDER WRAPPERS (Decorators in JavaScript)");
console.log("=".repeat(70));

// Higher-order function that measures execution time of any async operation
function withLatencyTracking(fn) {
    return async function (...args) {
        console.log(`🛫 [Checkpoint] Starting: '${fn.name}'`);
        const start = performance.now();
        
        // Execute original function!
        const result = await fn(...args);
        
        const duration = (performance.now() - start).toFixed(2);
        console.log(`🛬 [Checkpoint] '${fn.name}' finished in ${duration} ms`);
        return result;
    };
}

// Simulating an S3 bucket scan
async function scanS3Bucket(bucketName) {
    // simulate network delay
    await new Promise(resolve => setTimeout(resolve, 200));
    return `Bucket '${bucketName}' contains 42 objects.`;
}

// Wrap the function (Exact JS equivalent to Python @withLatencyTracking)
const trackedScan = withLatencyTracking(scanS3Bucket);

// Invoke
trackedScan("task-nalgonda-portfolio").then(res => console.log("Result:", res));
