/**
 * 05_promises_async_await_json.js
 * =================================
 * Topic: Asynchronous Programming (Promises, async/await), Error Handling & JSON
 * Analogy: The McDonald's Buzzer Pager
 *
 * ANALOGY FOR STUDENTS:
 * ---------------------
 * 1. Synchronous Code = Standing in a line where the chef cooks ONE burger at a time.
 *    - Everyone freezes and waits! You cannot do anything while the burger fries.
 * 2. Asynchronous (The McDonald's Buzzer) = You place your order, the cashier hands you
 *    a buzzing plastic token (The Promise).
 *    - You go sit down, talk to your friends, check your phone.
 *    - When the burger is ready, the token buzzes (resolve)!
 *    - If they ran out of fries, the manager apologizes (reject)!
 * 3. async / await = Modern English way of writing asynchronous code.
 *    - It looks like regular step-by-step code, but Node.js doesn't freeze the computer!
 */

const fs = require('fs');

console.log("=".repeat(70));
console.log("🍔 PART 1: THE MCDONALD'S PROMISE TOKEN");
console.log("=".repeat(70));

// Function simulating an asynchronous cloud API call (AWS S3 Upload)
function uploadObjectToS3(filename, content) {
    return new Promise((resolve, reject) => {
        console.log(`⏳ [Upload Started] Uploading '${filename}' to AWS S3...`);
        
        setTimeout(() => {
            if (content && content.length > 0) {
                // Order ready! (Resolve the Promise)
                resolve({
                    statusCode: 200,
                    location: `s3://task-nalgonda-bucket/${filename}`,
                    sizeBytes: content.length
                });
            } else {
                // Out of fries! (Reject the Promise)
                reject(new Error(`Payload for '${filename}' cannot be empty!`));
            }
        }, 600); // 600ms simulated network latency
    });
}

// Consuming with Modern async / await & try / catch:
async function runDeploymentPipeline() {
    console.log("🏁 Deployment Pipeline Initiated...");
    try {
        const response = await uploadObjectToS3("portfolio.html", "<h1>Hello Nalgonda Cloud</h1>");
        console.log("🎉 SUCCESS: File available at:", response.location);
        console.log(`   Uploaded ${response.sizeBytes} bytes.`);
    } catch (error) {
        console.error("🛑 PIPELINE FAILED:", error.message);
    } finally {
        console.log("🔒 [Audit System] Pipeline run logged to CloudTrail.\n");
    }
}

// Run pipeline
runDeploymentPipeline().then(() => {
    console.log("=".repeat(70));
    console.log("📂 PART 2: JSON SERIALIZATION & FILE SYSTEM (Node.js)");
    console.log("=".repeat(70));

    const cloudManifest = {
        Project: "Cloud Portfolio",
        Center: "TASK Nalgonda",
        Trainer: "Sundeep Hiremat",
        Servers: [
            { id: "i-01", role: "web", publicIp: "13.233.45.10" },
            { id: "i-02", role: "db",  publicIp: null }
        ],
        Timestamp: new Date().toISOString()
    };

    const tempFile = "cloud_manifest_demo.json";

    // Serialize to JSON and write to disk
    console.log(`Writing config to '${tempFile}'...`);
    fs.writeFileSync(tempFile, JSON.stringify(cloudManifest, null, 4));
    console.log("✅ JSON written successfully.");

    // Read back and deserialize
    const rawContent = fs.readFileSync(tempFile, "utf-8");
    const parsedManifest = JSON.parse(rawContent);

    console.log("\nExtracted from JSON:");
    console.log("Project:", parsedManifest.Project);
    console.log("Trainer:", parsedManifest.Trainer);
    parsedManifest.Servers.forEach(s => console.log(`  • ${s.id} (${s.role}) -> ${s.publicIp}`));

    // Clean up
    if (fs.existsSync(tempFile)) {
        fs.unlinkSync(tempFile);
        console.log(`\n🧹 Cleaned up temporary file '${tempFile}'.`);
    }
});
