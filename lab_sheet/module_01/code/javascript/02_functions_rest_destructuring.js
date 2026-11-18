/**
 * 02_functions_rest_destructuring.js
 * ===================================
 * Topic: Functions, Default Parameters, Rest Parameters (...), and Destructuring
 * Analogy: The Flexible Amazon Delivery Truck
 *
 * ANALOGY FOR STUDENTS:
 * ---------------------
 * 1. Default Parameters = Standard Free Shipping.
 *    - If the caller doesn't specify, default kicks in.
 * 2. Rest Parameters (...args) = The Cargo Van Backdoor.
 *    - Put any number of items into the van; JavaScript bundles them all into a real Array!
 *    - Exact equivalent of Python *args!
 * 3. Destructuring { key1, key2 } = The Pre-sorted Mail Sorter.
 *    - Instead of typing obj.region, obj.instanceType, you extract them directly!
 * 4. Spread Operator { ...obj } = Photocopying a document and adding extra notes.
 */

console.log("=".repeat(70));
console.log("📦 PART 1: DEFAULT PARAMETERS (The Standard Free Shipping)");
console.log("=".repeat(70));

function calculateStorageCost(sizeGiB, ratePerGiB = 0.08, currency = "USD") {
    const total = (sizeGiB * ratePerGiB).toFixed(2);
    return `${total} ${currency}`;
}

console.log("100 GiB (Default rate):", calculateStorageCost(100));
console.log("100 GiB (Premium rate):", calculateStorageCost(100, 0.125, "INR"));


console.log("\n" + "=".repeat(70));
console.log("🎒 PART 2: REST PARAMETERS (...args -> Array) (The Cargo Van)");
console.log("=".repeat(70));

// Rest parameters bundle loose arguments into an Array (like Python *args -> tuple)
function sendCloudWatchAlarm(severity, ...subscribers) {
    console.log(`🚨 [Alert: ${severity}] Dispatching notifications to ${subscribers.length} engineers:`);
    subscribers.forEach(email => console.log(`   ✉️ Sent alert to: ${email}`));
}

sendCloudWatchAlarm("HIGH", "sundeep@cloud.com", "devops@task.in", "oncall@nalgonda.edu");


console.log("\n" + "=".repeat(70));
console.log("🪄 PART 3: DESTRUCTURING & DEFAULTS (The Pre-Sorted Mail Sorter)");
console.log("=".repeat(70));

// Exact equivalent to Python **kwargs unpacking with defaults!
function launchEC2Instance({
    imageId,
    instanceType = "t3.micro",
    monitoring = false,
    ...extraTags
}) {
    console.log(`🚀 Launching ${instanceType} from AMI ${imageId}`);
    console.log(`   Detailed Monitoring: ${monitoring}`);
    console.log(`   Extra Metadata Tags:`, extraTags);
}

launchEC2Instance({
    imageId: "ami-0123456789",
    monitoring: true,
    Owner: "Sundeep",
    Project: "Cloud Portfolio",
    Center: "TASK Nalgonda"
});


console.log("\n" + "=".repeat(70));
console.log("📋 PART 4: SPREAD OPERATOR (...) (The Rapid Document Photocopy)");
console.log("=".repeat(70));

const baseConfig = { region: "ap-south-1", vpc: "vpc-01" };
const securityConfig = { securityGroup: "sg-web", ports: [80, 443] };

// Merge objects into one (exact equivalent to Python {**dict1, **dict2})
const fullDeploymentConfig = {
    ...baseConfig,
    ...securityConfig,
    environment: "Production",
    timestamp: new Date().toISOString()
};

console.log("Merged Configuration:", fullDeploymentConfig);
