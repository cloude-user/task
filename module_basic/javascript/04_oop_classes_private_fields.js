/**
 * 04_oop_classes_private_fields.js
 * =================================
 * Topic: ES6 Classes, Private Fields (#), Getters/Setters, Static Methods & Inheritance
 * Analogy: The Automotive Blueprint & The Private Bank Safe
 *
 * ANALOGY FOR STUDENTS:
 * ---------------------
 * 1. class = The CAD Drawing / Factory Machine.
 * 2. new ClassName() = Driving a brand new car off the showroom floor.
 * 3. #privateField (Hash prefix) = The Locked Glove Compartment (Native JavaScript Name Mangling!).
 *    - Nobody outside the class can touch it, read it, or override it!
 * 4. get & set = The Security Guard Turnstile.
 *    - Validates values before assigning them (e.g. rejecting invalid state transitions).
 * 5. static = The Showroom Calculator (Utility function that doesn't need a specific car).
 */

console.log("=".repeat(70));
console.log("🚗 PART 1: ES6 CLASSES & PRIVATE FIELDS (#)");
console.log("=".repeat(70));

class CloudServer {
    // Private Field (#): True Native JavaScript Private Attribute!
    // Analogy: The Secret Bank Vault (Cannot be accessed from outside!)
    #iamSecretKey;

    constructor(instanceId, iamSecretKey, region = "ap-south-1") {
        this.instanceId = instanceId;   // Public attribute
        this.region = region;           // Public attribute
        this._state = "PENDING";        // Protected convention
        this.#iamSecretKey = iamSecretKey; // Private
    }

    // Safe method to view masked credentials
    getMaskedCredentials() {
        return `****-****-${this.#iamSecretKey.slice(-4)}`;
    }

    // Public method
    boot() {
        this._state = "RUNNING";
        console.log(`🟢 [${this.instanceId}] Server booted and is now ${this._state} in ${this.region}.`);
    }
}

const server1 = new CloudServer("i-prod-888", "AWS_SECRET_KEY_NALGONDA_7777");
console.log("Server ID (Public):  ", server1.instanceId);
console.log("Masked Key (via method):", server1.getMaskedCredentials());

// Direct access to #iamSecretKey throws a SyntaxError at compile time!
// console.log(server1.#iamSecretKey); // ❌ Property '#iamSecretKey' is not accessible outside class


console.log("\n" + "=".repeat(70));
console.log("🚪 PART 2: GETTERS & SETTERS (The State Machine Guard)");
console.log("=".repeat(70));

class ManagedInstance {
    static VALID_STATES = new Set(["PENDING", "RUNNING", "STOPPED", "TERMINATED"]);

    constructor(instanceId) {
        this.instanceId = instanceId;
        this._state = "PENDING";
    }

    // Getter
    get state() {
        return this._state;
    }

    // Setter (Guards against invalid state transitions)
    set state(newState) {
        const normalized = newState.toUpperCase();
        if (!ManagedInstance.VALID_STATES.has(normalized)) {
            throw new Error(`Invalid state: '${newState}'. Allowed: ${Array.from(ManagedInstance.VALID_STATES)}`);
        }
        if (this._state === "TERMINATED") {
            throw new Error(`⛔ REJECTION: Instance ${this.instanceId} is TERMINATED. Cannot restart!`);
        }
        console.log(`🔄 State transition for ${this.instanceId}: ${this._state} ➔ ${normalized}`);
        this._state = normalized;
    }

    // Static Utility Method (Calculator)
    static estimateCost(hours, ratePerHour = 0.0208) {
        return `$${(hours * ratePerHour).toFixed(2)}`;
    }
}

const node = new ManagedInstance("i-web-alpha");
node.state = "RUNNING";
node.state = "STOPPED";
node.state = "TERMINATED";

// Try illegal restart:
try {
    node.state = "RUNNING";
} catch (err) {
    console.error("Caught expected error:", err.message);
}

console.log("Static utility cost estimation (730 hrs):", ManagedInstance.estimateCost(730));


console.log("\n" + "=".repeat(70));
console.log("🧬 PART 3: INHERITANCE & POLYMORPHISM (extends & super)");
console.log("=".repeat(70));

class CloudResource {
    constructor(id) {
        this.id = id;
    }
    deploy() {
        console.log(`Starting deployment of generic resource: ${this.id}`);
    }
}

class EC2Instance extends CloudResource {
    constructor(id, instanceType = "t3.micro") {
        super(id); // Call parent constructor
        this.instanceType = instanceType;
    }

    // Method overriding (Polymorphism)
    deploy() {
        console.log(`🚀 [EC2] Launching virtual machine ${this.id} (${this.instanceType})`);
    }
}

class S3Bucket extends CloudResource {
    deploy() {
        console.log(`🪣 [S3] Creating bucket s3://${this.id} with encryption enabled`);
    }
}

// Polymorphic loop
const cloudStack = [new EC2Instance("i-001"), new S3Bucket("task-nalgonda-assets")];
cloudStack.forEach(res => res.deploy());
