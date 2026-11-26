/**
 * 01_variables_and_collections.js
 * ================================
 * Topic: JavaScript Variables, Primitive vs Reference Types, Arrays, and Objects
 * Analogy: The Flexible Modern Locker Room & The Address Slip
 *
 * ANALOGY FOR STUDENTS:
 * ---------------------
 * 1. const = A Permanent Laser-Engraved Plaque.
 *    - Once created, you CANNOT point it to another object. Use const for 90% of your code!
 * 2. let = A Dry-Erase Whiteboard Locker.
 *    - You can erase and write a new value anytime (mutable).
 * 3. var = An Old megaphone that echoes everywhere (Hoisting & Function scope).
 *    - DO NOT USE var in modern cloud code! It leaks out of if-blocks and causes bugs.
 * 4. PRIMITIVE vs REFERENCE TYPES (Memory Model):
 *    - Primitive (number, string, boolean, null, undefined) = Pass by VALUE.
 *      Like writing a number on a sticky note and handing it to a friend. If they erase theirs,
 *      your note stays identical!
 *    - Reference (Array, Object, Function) = Pass by REFERENCE.
 *      Like handing your friend the key/address slip to your locker. If they open the locker
 *      and change the contents, YOUR locker content changes too!
 * 5. Array [] = A high-speed conveyor belt (like Python lists, but with .map and .filter built in).
 * 6. Object {} = The Master Cloud Payload (Key-Value pairs, exactly like JSON & Python dicts).
 */

console.log("=".repeat(70));
console.log("📦 PART 1: const vs let vs var (Laser Plaque vs Whiteboard)");
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
console.log("🧠 PART 2: PRIMITIVE vs REFERENCE TYPES (Value vs Address)");
console.log("=".repeat(70));

// A. Primitive Type (Pass by Value)
let initialBalance = 1000;
let clonedBalance = initialBalance; // Direct value copy
clonedBalance = 2500;

console.log("--- Primitive (Numbers) ---");
console.log("initialBalance:", initialBalance); // 1000 (Unaffected!)
console.log("clonedBalance: ", clonedBalance);  // 2500

// B. Reference Type (Pass by Pointer / Reference)
const serverNodeA = { id: "node-01", status: "STOPPED", ip: "10.0.1.15" };
const serverNodeB = serverNodeA; // Copies MEMORY ADDRESS, not a separate object!

serverNodeB.status = "RUNNING"; // Mutates the underlying shared memory

console.log("\n--- Reference (Objects / Memory Pointer) ---");
console.log("serverNodeA.status:", serverNodeA.status); // RUNNING! (Changed!)
console.log("serverNodeB.status:", serverNodeB.status); // RUNNING!
console.log("Comparison (serverNodeA === serverNodeB):", serverNodeA === serverNodeB); // true

// Comparison with Python:
// In Python: dict_a = {'status': 'STOPPED'}; dict_b = dict_a; dict_b['status'] = 'RUNNING'
// Result is identical in Python: dict_a['status'] becomes 'RUNNING'.


console.log("\n" + "=".repeat(70));
console.log("🛒 PART 3: ARRAYS & TRANSFORMATIONS (The Conveyor Belt)");
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
console.log("🔑 PART 4: OBJECTS & OPTIONAL CHAINING (The Master Payload)");
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
console.log("🎟️ PART 5: SETS & MAPS (Deduplication & Fast Lookups)");
console.log("=".repeat(70));

const loggedRegions = ["ap-south-1", "us-east-1", "ap-south-1", "eu-west-1", "us-east-1"];
// Set automatically deduplicates
const uniqueRegions = new Set(loggedRegions);

console.log("Raw logs:", loggedRegions);
console.log("Unique Set:", Array.from(uniqueRegions));
console.log("Has 'ap-south-1'?", uniqueRegions.has("ap-south-1"));
