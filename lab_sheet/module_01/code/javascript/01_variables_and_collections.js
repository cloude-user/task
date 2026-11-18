/**
 * 01_variables_and_collections.js
 * ================================
 * Topic: JavaScript (Node.js) Variables, Types, Arrays, and Objects
 * Analogy: The Flexible Modern Locker Room
 *
 * ANALOGY FOR STUDENTS:
 * ---------------------
 * 1. const = A Permanent Laser-Engraved Plaque.
 *    - Once created, you CANNOT point it to another object. Use const for 90% of your code!
 * 2. let = A Dry-Erase Whiteboard Locker.
 *    - You can erase and write a new value anytime (mutable).
 * 3. var = An Old megaphone that echoes everywhere (Hoisting & Function scope).
 *    - DO NOT USE var in modern cloud code! It leaks out of if-blocks and causes bugs.
 * 4. Array [] = A high-speed conveyor belt (like Python lists, but with .map and .filter built in).
 * 5. Object {} = The Master Cloud Payload (Key-Value pairs, exactly like JSON).
 */

console.log("=".repeat(70));
console.log("📦 PART 1: const vs let (Laser Plaque vs Whiteboard)");
console.log("=".repeat(70));

// const: Binding cannot be reassigned
const region = "ap-south-1";
const hourlyRate = 0.0208;
const isProduction = true;
const unassignedSlot = null; // Intentional empty object reference

// let: Value can be reassigned
let instanceCount = 2;
instanceCount += 3; // Now 5

console.log(`Region:   ${region} (${typeof region})`);
console.log(`Count:    ${instanceCount} (${typeof instanceCount})`);
console.log(`Rate:     $${hourlyRate}/hr (${typeof hourlyRate})`);
console.log(`Is Prod:  ${isProduction} (${typeof isProduction})`);
console.log(`Slot:     ${unassignedSlot} (${typeof unassignedSlot})\n`);


console.log("=".repeat(70));
console.log("🛒 PART 2: ARRAYS & TRANSFORMATIONS (The Conveyor Belt)");
console.log("=".repeat(70));

const servers = ["web-01", "web-02", "app-01", "app-02", "db-01"];
console.log("Original servers:", servers);

// Adding items
servers.push("cache-01");
console.log("After push:      ", servers);

// Slicing (slice start, stop_before) - same as Python [0:2]
console.log("First 2 servers: ", servers.slice(0, 2));
console.log("Last server:     ", servers[servers.length - 1]);

// .filter and .map (JavaScript's equivalent to Python List Comprehensions!)
const webTier = servers
    .filter(s => s.startsWith("web"))
    .map(s => s.toUpperCase());
console.log("Filtered Web Tier:", webTier, "\n");


console.log("=".repeat(70));
console.log("🔑 PART 3: OBJECTS & OPTIONAL CHAINING (The Master Payload)");
console.log("=".repeat(70));

const ec2Config = {
    instanceId: "i-0987654321fedcba0",
    instanceType: "t3.micro",
    state: { code: 16, name: "running" },
    tags: {
        Environment: "Production",
        Project: "Cloud Portfolio",
        Center: "TASK Nalgonda"
    }
};

console.log("Instance ID:", ec2Config.instanceId);

// Optional Chaining (?.) & Nullish Coalescing (??)
// Analogy: Asking politely "Does this key exist? If not, don't crash, just give me default!"
const env = ec2Config.tags?.Environment ?? "Development";
const monitoring = ec2Config.monitoring?.status ?? "DISABLED (Default)";

console.log("Environment:", env);
console.log("Monitoring: ", monitoring, "\n");


console.log("=".repeat(70));
console.log("🎟️ PART 4: SETS & MAPS (Deduplication & Fast Lookups)");
console.log("=".repeat(70));

const loggedRegions = ["ap-south-1", "us-east-1", "ap-south-1", "eu-west-1", "us-east-1"];
// Set automatically deduplicates
const uniqueRegions = new Set(loggedRegions);

console.log("Raw logs:", loggedRegions);
console.log("Unique Set:", Array.from(uniqueRegions));
console.log("Has 'ap-south-1'?", uniqueRegions.has("ap-south-1"));
