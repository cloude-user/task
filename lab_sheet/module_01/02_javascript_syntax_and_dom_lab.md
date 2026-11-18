# Lab Sheet 1.2: Modern JavaScript & DOM Manipulation
> **Module 1:** Programming Foundations  
> **Topic 1.b:** Modern ES2024 JavaScript, DOM Events & Asynchronous Fetch  
> **Target:** Cloud Software Developer Trainees  

---

## 🎯 Lab Objectives
1. Understand modern JavaScript syntax: `let`/`const`, arrow functions, and template literals.
2. Manipulate the Document Object Model (DOM) to update web pages dynamically.
3. Understand asynchronous JavaScript: Promises, `async`/`await`.
4. Fetch live external JSON data from a REST API using the browser `fetch()` API.

---

## 🛠️ Step-by-Step Hands-On Exercises

### Exercise 1: Modern JavaScript Syntax
Open your browser console (Press `F12` -> Console tab) or run in Node.js:
```javascript
// 1. Arrow functions and template literals
const calculateCloudCost = (hours, ratePerHour = 0.0116) => {
    const total = hours * ratePerHour;
    return `Total EC2 Cost for ${hours} hours: $${total.toFixed(4)}`;
};

console.log(calculateCloudCost(720)); // Full month (720 hrs)

// 2. Array destructuring and map
const cloudRegions = ["ap-south-1", "us-east-1", "eu-west-1"];
const [primaryRegion, secondaryRegion] = cloudRegions;
console.log(`Primary: ${primaryRegion}, Secondary: ${secondaryRegion}`);

const formattedRegions = cloudRegions.map(r => r.toUpperCase());
console.log(formattedRegions);
```

---

### Exercise 2: Interactive DOM & Fetch API
Create an `index.html` file:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cloud Status Dashboard</title>
    <style>
        body { font-family: sans-serif; padding: 2rem; background: #f8fafc; }
        .card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 500px; }
        button { background: #1e3a8a; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2563eb; }
        #status-display { margin-top: 1rem; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>AWS Region Health Checker</h2>
        <button id="check-btn">Check API Status</button>
        <div id="status-display">Click button to fetch status...</div>
    </div>

    <script>
        const btn = document.getElementById("check-btn");
        const display = document.getElementById("status-display");

        btn.addEventListener("click", async () => {
            display.innerText = "Contacting cloud endpoint...";
            try {
                // Fetch public test endpoint
                const response = await fetch("https://jsonplaceholder.typicode.com/todos/1");
                const data = await response.json();
                display.innerHTML = `<span style="color: green;">✓ Connected Successfully!</span><br/>Sample Payload: ${data.title}`;
            } catch (err) {
                display.innerHTML = `<span style="color: red;">✗ Failed to connect: ${err.message}</span>`;
            }
        });
    </script>
</body>
</html>
```
Double-click `index.html` to open it in Chrome or Firefox, click the button, and watch live data render via `fetch()`!

---

### ✅ Verification Checklist
- [ ] Arrow functions and array transformations tested.
- [ ] `index.html` interactive button updates DOM dynamically.
- [ ] Asynchronous API call successfully retrieves live JSON data.
