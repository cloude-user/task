# 📘 Module 01: Python & JavaScript Master Handbook for Cloud Developers
**Telangana Academy for Skill and Knowledge (TASK) · Nalgonda Center**  
**Course:** Cloud Software Developer (AWS DVA-C02 Aligned)  
**Trainer:** Sundeep Hiremat  

---

## 🎯 Purpose & Executive Summary
In modern cloud development (especially on AWS), two programming languages dominate the industry:
1. **Python:** The undisputed leader for Cloud Automation, Data Engineering, Infrastructure Scripting (`boto3`), Machine Learning, and AWS Lambda functions.
2. **JavaScript / TypeScript (Node.js):** The standard for Web Applications, CloudFront Edge Functions, AWS CDK (Cloud Development Kit), and high-throughput asynchronous microservices.

This handbook is designed specifically for students and early-career developers. It covers foundational and advanced constructs in **Python** (including Lambdas, Decorators, Exception Handling, File I/O, and OOP), alongside a **side-by-side JavaScript equivalent guide** to build total cross-language fluency.

---

## 📑 Table of Contents
1. [Language Fundamentals & Execution Models](#1-language-fundamentals--execution-models)
2. [Variables, Types & Memory Scoping](#2-variables-types--memory-scoping)
3. [Collections & Data Structures Comparison](#3-collections--data-structures-comparison)
4. [Functions, Default Parameters, and Variable Arguments](#4-functions-default-parameters-and-variable-arguments)
5. [Anonymous Functions: Python Lambdas vs JS Arrow Functions](#5-anonymous-functions-python-lambdas-vs-js-arrow-functions)
6. [Higher-Order Functions & Python Decorators](#6-higher-order-functions--python-decorators)
7. [Exception & Error Handling (Resilience Patterns)](#7-exception--error-handling-resilience-patterns)
8. [File I/O, Context Managers & JSON Handling](#8-file-io-context-managers--json-handling)
9. [Object-Oriented Programming (OOP) in Cloud](#9-object-oriented-programming-oop-in-cloud)
10. [Asynchronous Programming: Callbacks, Promises & Async/Await](#10-asynchronous-programming-callbacks-promises--asyncawait)
11. [Cloud Developer Real-World Cheatsheet](#11-cloud-developer-real-world-cheatsheet)

---

## 1. Language Fundamentals & Execution Models

| Feature | Python 3.12+ | JavaScript (ES6+ / Node.js 20+) |
| :--- | :--- | :--- |
| **Execution Engine** | CPython Interpreter / Bytecode (`.pyc`) | V8 Engine (JIT compiled to machine code) |
| **Syntax Structure** | Indentation-sensitive (off-side rule) | C-style braces `{}` and semicolons (optional) |
| **Typing Discipline** | Strongly typed, dynamically inferred | Weakly typed, dynamically inferred |
| **Concurrency Model**| Multi-threading (GIL), Multi-processing, `asyncio` | Single-threaded Event Loop with non-blocking I/O |
| **Cloud Ecosystem**  | AWS Lambda (Python runtime), `boto3`, SageMaker | AWS Lambda (Node.js), AWS SDK v3 (`@aws-sdk/client-*`) |

---

## 2. Variables, Types & Memory Scoping

### Python
Python uses dynamic typing where variable names are references pointing to objects in memory:
```python
# Python variable declaration
region_name = "ap-south-1"    # str
max_instances = 5             # int
hourly_cost = 0.0225          # float
is_active = True              # bool (Capital T)
backup_vault = None           # NoneType (absence of value)

# Type inspection
print(type(region_name))      # <class 'str'>
print(isinstance(max_instances, int))  # True
```

### JavaScript
JavaScript provides three keywords for declaration with strict scoping rules:
```javascript
// const: Immutable binding (Preferred default for clean code)
const regionName = "ap-south-1";

// let: Block-scoped mutable variable (use when values reassign)
let maxInstances = 5;
maxInstances = 10; // Valid

// var: Function-scoped, hoisted (AVOID in modern code)
var oldStyle = "legacy";

// Primitive types
const hourlyCost = 0.0225;     // number (IEEE 754 64-bit float)
const isActive = true;         // boolean (lowercase t)
const emptySlot = null;        // intentional null object reference
let unassignedVar;             // undefined (variable declared but not assigned value)
```

> ⚠️ **Key Difference for Cloud Engineers:**
> * In Python, missing dictionary keys or unassigned values throw `KeyError` or `NameError`.
> * In JavaScript, accessing a non-existent property returns `undefined` without crashing immediately, which can cause silent bugs in serverless functions!

---

## 3. Collections & Data Structures Comparison

### Comparison Matrix
| Abstract Concept | Python | JavaScript | AWS Cloud Use Case |
| :--- | :--- | :--- | :--- |
| **Ordered Sequence** | `list` (`[1, 2, 3]`) | `Array` (`[1, 2, 3]`) | List of EC2 instance IDs, security group rules |
| **Immutable Sequence**| `tuple` (`(1, 2)`) | *Read-only Array / Freeze* | Database connection credentials, fixed coordinates |
| **Key-Value Map**    | `dict` (`{"id": 1}`) | `Object` / `Map` | JSON payloads, DynamoDB items, HTTP headers |
| **Unique Elements**   | `set` (`{1, 2}`) | `Set` (`new Set([1, 2])`) | Unique user IDs, unique availability zones |

### Code Comparison: Slicing, Filtering & Mapping

#### Python
```python
# Lists & Slicing
servers = ["web-01", "web-02", "app-01", "app-02", "db-01"]
print(servers[0:2])     # ['web-01', 'web-02'] (start:stop exclusive)
print(servers[-1])      # 'db-01' (last element)

# Dictionary operations
config = {
    "instance_type": "t3.micro",
    "vpc_id": "vpc-0abc123",
    "tags": {"Environment": "Production"}
}
# Safe access with fallback
env = config.get("tags", {}).get("Environment", "Development")

# List Comprehension (Idiomatic Python)
web_servers = [s.upper() for s in servers if s.startswith("web")]
print(web_servers)  # ['WEB-01', 'WEB-02']
```

#### JavaScript
```javascript
// Arrays & Slicing
const servers = ["web-01", "web-02", "app-01", "app-02", "db-01"];
console.log(servers.slice(0, 2)); // ['web-01', 'web-02']
console.log(servers[servers.length - 1]); // 'db-01' (or servers.at(-1))

// Object operations
const config = {
    instanceType: "t3.micro",
    vpcId: "vpc-0abc123",
    tags: { Environment: "Production" }
};
// Optional chaining (ES2020)
const env = config.tags?.Environment ?? "Development";

// Array Transformations (.map, .filter)
const webServers = servers
    .filter(s => s.startsWith("web"))
    .map(s => s.toUpperCase());
console.log(webServers); // ['WEB-01', 'WEB-02']
```

---

## 4. Functions, Default Parameters, and Variable Arguments (*args, **kwargs)

Cloud SDKs like `boto3` and `@aws-sdk` accept dynamic configurations. Understanding parameter types, default arguments, and variable argument packing/unpacking is essential.

### 4.1 Positional, Default, and Keyword-Only Arguments
```python
# The Mutable Default Argument Pitfall & Fix:
# NEVER use mutable objects (like [] or {}) as default arguments!
# WRONG: def attach_tags(instance_id, tags=[])
# RIGHT: def attach_tags(instance_id, tags=None)

def create_ec2_instance(
    image_id: str,                          # Mandatory positional argument
    instance_type: str = "t3.micro",        # Default argument
    *,                                      # Keyword-only separator (everything after MUST be named)
    enable_monitoring: bool = False,
    ebs_optimized: bool = True
):
    print(f"Creating {instance_type} from {image_id} (Monitoring: {enable_monitoring})")

# Valid call:
create_ec2_instance("ami-0abcdef123", "t3.small", enable_monitoring=True)

# Invalid call (raises TypeError):
# create_ec2_instance("ami-0abcdef123", "t3.small", True) # positional not allowed after '*'
```

### 4.2 Dynamic Argument Packing: `*args` and `**kwargs`
* `*args`: Collects any arbitrary number of extra positional arguments into a **tuple**.
* `**kwargs`: Collects any arbitrary number of extra keyword arguments into a **dictionary**.

```python
def configure_cloud_client(service_name, *regions, **client_options):
    """
    Simulates how AWS boto3.client() accepts dynamic service options.
    """
    print(f"Service: {service_name}")
    print(f"Target Regions ({type(regions).__name__}): {regions}")
    print(f"Configuration Options ({type(client_options).__name__}): {client_options}")

# Calling with variable arguments:
configure_cloud_client(
    "Amazon S3",
    "ap-south-1", "ap-south-2", "us-east-1",  # *regions -> ('ap-south-1', 'ap-south-2', 'us-east-1')
    timeout_seconds=30, max_retries=5, use_ssl=True, verify_certs=True  # **client_options
)
```

### 4.3 Argument Unpacking (`*` and `**`)
```python
# Unpacking lists into *args and dicts into **kwargs
default_tags = ("Production", "WebTier", "TASK-Nalgonda")
cloud_params = {"instance_type": "t3.medium", "auto_shutdown": True}

def launch_server(name, *tags, **params):
    print(name, tags, params)

# Unpack directly with * and **:
launch_server("web-server-01", *default_tags, **cloud_params)
```

### 4.4 JavaScript Equivalent: Rest Parameters `...` and Destructuring
```javascript
// Rest parameters (...) collect arguments into a real JavaScript Array
function configureCloudClient(serviceName, ...regions) {
    console.log(`Service: ${serviceName}`);
    console.log("Regions array:", regions);
}

// Object destructuring with defaults (exact equivalent to kwargs with defaults)
function createEc2Instance({ imageId, instanceType = "t3.micro", enableMonitoring = false, ...otherOptions }) {
    console.log(`Creating ${instanceType} from ${imageId}`);
    console.log("Extra options:", otherOptions);
}

createEc2Instance({ imageId: "ami-0abc", enableMonitoring: true, env: "Prod", costCenter: "EDU" });
```

## 5. Anonymous Functions: Python Lambdas vs JS Arrow Functions

> 🔔 **Crucial Clarity:**
> In computer science, an **anonymous function** (a function without a name) is called a **lambda expression**.  
> Do not confuse a **Python lambda function** with **AWS Lambda** (the cloud serverless compute service)!

### Python `lambda`
Python lambdas are restricted to a **single expression** whose result is implicitly returned:
$$\text{Syntax:} \quad \lambda \text{ arguments } : \text{ expression }$$

```python
# Standard function
def square(x):
    return x ** 2

# Equivalent lambda
square_lambda = lambda x: x ** 2
print(square_lambda(5)) # 25

# Real Cloud Use Case: Sorting Cloud Resources by Cost
ec2_fleet = [
    {"id": "i-01", "type": "t3.large", "hourly_cost": 0.0832},
    {"id": "i-02", "type": "t2.nano",  "hourly_cost": 0.0058},
    {"id": "i-03", "type": "t3.micro", "hourly_cost": 0.0208}
]

# Sort by cost ascending
sorted_fleet = sorted(ec2_fleet, key=lambda inst: inst["hourly_cost"])
for inst in sorted_fleet:
    print(f"{inst['id']} ({inst['type']}): ${inst['hourly_cost']}/hr")
```

### JavaScript Arrow Functions `() => {}`
JavaScript arrow functions are more powerful than Python lambdas because they support both single-expression returns and full multi-line statement blocks:
```javascript
// Single-expression (implicit return)
const square = x => x ** 2;

// Multi-line block (explicit return needed)
const calculateTotal = (price, tax) => {
    const total = price + (price * tax);
    return total.toFixed(2);
};

// Real Cloud Use Case: Sorting Cloud Resources
const ec2Fleet = [
    { id: "i-01", type: "t3.large", hourlyCost: 0.0832 },
    { id: "i-02", type: "t2.nano",  hourlyCost: 0.0058 },
    { id: "i-03", type: "t3.micro", hourlyCost: 0.0208 }
];

ec2Fleet.sort((a, b) => a.hourlyCost - b.hourlyCost);
console.log(ec2Fleet);
```

---

## 6. Higher-Order Functions & Python Decorators

A **higher-order function** is a function that either:
1. Takes one or more functions as arguments.
2. Returns a function as its result.

### Understanding Python Decorators (`@decorator`)
In Python, a decorator is a syntactic wrapper that modifies or enhances a function's behavior **without changing its source code**.

#### Step 1: Anatomy of a Decorator
```python
import functools
import time

def execution_logger(func):
    """Decorator that logs function execution time (Latency tracking)."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"🚀 [START] Invoking function: '{func.__name__}'")
        start_time = time.time()
        
        # Execute original function
        result = func(*args, **kwargs)
        
        elapsed = (time.time() - start_time) * 1000
        print(f"✅ [FINISH] '{func.__name__}' completed in {elapsed:.2f} ms")
        return result
    return wrapper

# Applying the decorator with '@'
@execution_logger
def provision_database(db_name, engine="mysql"):
    time.sleep(0.5) # simulate network call
    return f"Database '{db_name}' ({engine}) provisioned successfully."

# Invoking
status = provision_database("production_users", engine="aurora-mysql")
print(status)
```

#### Step 2: Cloud Resilience Decorator: `@retry_on_failure`
In AWS, API calls frequently encounter transient network errors or throttling (`429 Too Many Requests`). A decorator solves this cleanly:
```python
import time
import functools

def retry_api_call(max_retries=3, delay_seconds=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"⚠️ Attempt {attempts} failed with error: {e}. Retrying in {delay_seconds}s...")
                    time.sleep(delay_seconds)
            raise RuntimeError(f"❌ Function '{func.__name__}' failed after {max_retries} attempts.")
        return wrapper
    return decorator

@retry_api_call(max_retries=3, delay_seconds=2)
def query_aws_metadata():
    import random
    if random.random() < 0.7:
        raise ConnectionResetError("AWS Metadata Service 169.254.169.254 timed out")
    return {"InstanceId": "i-0987654321", "State": "running"}

# Test execution
try:
    data = query_aws_metadata()
    print("Success:", data)
except RuntimeError as err:
    print(err)
```

### JavaScript Equivalent: Higher-Order Wrapper Functions
In JavaScript, decorators exist via TypeScript or Babel, but standard JS achieves the exact same pattern using Higher-Order Functions:
```javascript
// Higher-Order Function in JavaScript
function withExecutionLogger(fn) {
    return async function (...args) {
        console.log(`🚀 [START] Invoking: ${fn.name}`);
        const start = performance.now();
        const result = await fn(...args);
        const duration = (performance.now() - start).toFixed(2);
        console.log(`✅ [FINISH] ${fn.name} finished in ${duration} ms`);
        return result;
    };
}

async function fetchS3Metadata(bucketName) {
    // Simulate async fetch
    await new Promise(r => setTimeout(r, 300));
    return { bucket: bucketName, region: "ap-south-1" };
}

// Wrap the function
const loggedFetch = withExecutionLogger(fetchS3Metadata);
loggedFetch("nalgonda-cloud-bucket").then(res => console.log(res));
```

---

## 7. Exception & Error Handling (Resilience Patterns)

Resilient cloud code must catch failures gracefully rather than crashing servers.

### Python: `try / except / else / finally`
```python
class InsufficientBudgetException(Exception):
    """Custom cloud domain exception."""
    pass

def launch_server_with_shield(instance_type, current_spend, monthly_budget):
    try:
        cost_map = {"t2.micro": 15, "t3.medium": 45, "c5.xlarge": 150}
        
        if instance_type not in cost_map:
            raise ValueError(f"Unknown instance type: '{instance_type}'")
            
        projected_spend = current_spend + cost_map[instance_type]
        if projected_spend > monthly_budget:
            raise InsufficientBudgetException(
                f"Budget breached! Projected: ${projected_spend}, Cap: ${monthly_budget}"
            )
            
        print(f"🎉 Instance '{instance_type}' launched successfully.")
        return True

    except ValueError as ve:
        print(f"🔴 Configuration Error: {ve}")
        return False
    except InsufficientBudgetException as be:
        print(f"🛑 Cost Shield Triggered: {be}")
        return False
    except Exception as e:
        print(f"💥 Unexpected Error: {e}")
        return False
    else:
        print("🟢 No errors encountered during provisioning cycle.")
    finally:
        print("🔒 [Audit Log] Cloud provisioning transaction closed.")

# Test calls
launch_server_with_shield("c5.xlarge", 400, 450) # Budget breach
```

### JavaScript: `try / catch / finally / throw`
```javascript
class InsufficientBudgetError extends Error {
    constructor(message) {
        super(message);
        this.name = "InsufficientBudgetError";
    }
}

function launchServerWithShield(instanceType, currentSpend, monthlyBudget) {
    try {
        const costMap = { "t2.micro": 15, "t3.medium": 45, "c5.xlarge": 150 };
        
        if (!costMap[instanceType]) {
            throw new Error(`Unknown instance type: ${instanceType}`);
        }
        
        const projected = currentSpend + costMap[instanceType];
        if (projected > monthlyBudget) {
            throw new InsufficientBudgetError(`Budget breached! Projected: $${projected}, Cap: $${monthlyBudget}`);
        }
        
        console.log(`🎉 Instance ${instanceType} launched.`);
        return true;
    } catch (error) {
        if (error instanceof InsufficientBudgetError) {
            console.error(`🛑 Cost Shield: ${error.message}`);
        } else {
            console.error(`💥 Error: ${error.message}`);
        }
        return false;
    } finally {
        console.log("🔒 [Audit Log] Transaction cycle completed.");
    }
}
```

---

## 8. File I/O, Context Managers & JSON Handling

AWS Cloud resources communicate entirely through **JSON** documents (policies, events, API calls).

### Python Context Manager & JSON
```python
import json

# Writing Cloud Config
server_config = {
    "Project": "Cloud Portfolio",
    "Center": "TASK Nalgonda",
    "Trainer": "Sundeep Hiremat",
    "Instances": [
        {"id": "i-01", "role": "web", "public_ip": "13.233.45.10"},
        {"id": "i-02", "role": "db",  "public_ip": None}
    ]
}

# The 'with' context manager automatically closes files
with open("cloud_config.json", "w", encoding="utf-8") as f:
    json.dump(server_config, f, indent=4)
print("File written successfully.")

# Reading and parsing JSON
with open("cloud_config.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)

print("Loaded Trainer:", loaded_data["Trainer"])
for inst in loaded_data["Instances"]:
    print(f"Server {inst['id']} - IP: {inst['public_ip']}")
```

### JavaScript (Node.js) File System & JSON
```javascript
const fs = require('fs');

const serverConfig = {
    Project: "Cloud Portfolio",
    Center: "TASK Nalgonda",
    Trainer: "Sundeep Hiremat",
    Instances: [
        { id: "i-01", role: "web", publicIp: "13.233.45.10" },
        { id: "i-02", role: "db",  publicIp: null }
    ]
};

// Serialize and write file (synchronous for simplicity)
fs.writeFileSync("cloud_config.json", JSON.stringify(serverConfig, null, 4));

// Read and deserialize
const rawData = fs.readFileSync("cloud_config.json", "utf-8");
const loadedData = JSON.parse(rawData);

console.log("Loaded Trainer:", loadedData.Trainer);
loadedData.Instances.forEach(inst => {
    console.log(`Server ${inst.id} - IP: ${inst.publicIp}`);
});
```

---

## 9. Object-Oriented Programming (OOP) in Cloud

In enterprise cloud development, everything from AWS SDK clients to Kubernetes controllers is modeled using Object-Oriented Programming.

---

### 9.1 Encapsulation, Privacy Levels & Name Mangling
Python does not have a strict `private` keyword like Java or C++. Instead, it uses **naming conventions** and an active compiler transformation called **Name Mangling**.

| Visibility | Syntax | Convention / Behavior |
| :--- | :--- | :--- |
| **Public** | `self.instance_id` | Accessible from anywhere inside and outside the class. |
| **Protected** | `self._state` | Single leading underscore. Convention: internal to class & subclasses. |
| **Private (Mangled)** | `self.__iam_secret` | Double leading underscore. **Python actively renames the attribute** to `_ClassName__attribute` to prevent accidental overwriting or outside tampering. |

#### Real Cloud Code Example: Name Mangling in Action
```python
class SecureCloudInstance:
    def __init__(self, instance_id: str, iam_secret_key: str):
        self.instance_id = instance_id          # Public
        self._operating_status = "INITIALIZING" # Protected
        self.__iam_secret_key = iam_secret_key  # Private (Name Mangled!)

    def get_masked_key(self):
        """Safe inspection method."""
        return f"****-****-{self.__iam_secret_key[-4:]}"

server = SecureCloudInstance("i-prod-007", "AWS_SECRET_KEY_NALGONDA_9999")

print(server.instance_id)            # Output: i-prod-007 (Public works)
print(server._operating_status)      # Output: INITIALIZING (Protected works)
print(server.get_masked_key())       # Output: ****-****-9999 (Method works)

# Trying to access __iam_secret_key directly throws AttributeError!
try:
    print(server.__iam_secret_key)
except AttributeError as e:
    print("❌ DIRECT ACCESS BLOCKED:", e)

# 🔍 HOW PYTHON MANGLED THE NAME:
# Python renamed '__iam_secret_key' to '_SecureCloudInstance__iam_secret_key'
mangled_name = "_SecureCloudInstance__iam_secret_key"
print(f"Direct access via mangled name ({mangled_name}):", getattr(server, mangled_name))
```

---

### 9.2 OOP Decorators: `@property`, `@setter`, `@classmethod`, `@staticmethod`

#### A. `@property` and `@setter` (State Guards & Attribute Validation)
In cloud infrastructure, instances cannot transition to arbitrary states (e.g. you cannot jump from `TERMINATED` back to `RUNNING`). We use `@property` and `@name.setter` to enforce business logic:
```python
import re

class ManagedServer:
    VALID_STATES = {"PENDING", "RUNNING", "STOPPED", "TERMINATED"}

    def __init__(self, server_id: str, ip_address: str):
        self.server_id = server_id
        self._state = "PENDING"
        self._ip_address = None
        self.ip_address = ip_address # triggers setter validation!

    # Getter
    @property
    def state(self):
        return self._state

    # Setter with State Machine Validation
    @state.setter
    def state(self, new_state: str):
        new_state = new_state.upper()
        if new_state not in self.VALID_STATES:
            raise ValueError(f"Invalid state: '{new_state}'. Allowed: {self.VALID_STATES}")
        if self._state == "TERMINATED":
            raise RuntimeError(f"Cannot restart {self.server_id}! A TERMINATED server is permanently destroyed.")
        print(f"🔄 State Transition: {self._state} ➔ {new_state}")
        self._state = new_state

    # IP Address Setter with Regex Validation
    @property
    def ip_address(self):
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip: str):
        pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
        if not re.match(pattern, ip):
            raise ValueError(f"Invalid IPv4 Address format: '{ip}'")
        self._ip_address = ip

node = ManagedServer("i-001", "13.233.45.10")
node.state = "RUNNING"
node.state = "STOPPED"
node.state = "TERMINATED"

# Attempting illegal restart -> BLOCKED!
# node.state = "RUNNING"  # Raises RuntimeError!
```

#### B. `@classmethod` (Alternative Constructors & Factory Methods)
A `@classmethod` receives `cls` (the class) and is the standard Python design pattern for building objects from JSON strings, dictionary manifests, or predefined templates:
```python
import json

class CloudServerFactory:
    def __init__(self, instance_id: str, instance_type: str, region: str, hourly_cost: float):
        self.instance_id = instance_id
        self.instance_type = instance_type
        self.region = region
        self.hourly_cost = hourly_cost

    def __repr__(self):
        return f"<Server {self.instance_id} [{self.instance_type}] in {self.region} (${self.hourly_cost}/hr)>"

    # Alternative Constructor 1: From JSON API payload
    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(
            instance_id=data["id"],
            instance_type=data.get("type", "t3.micro"),
            region=data.get("region", "ap-south-1"),
            hourly_cost=data.get("cost", 0.0208)
        )

    # Alternative Constructor 2: Free Tier Template
    @classmethod
    def free_tier_template(cls, instance_id: str):
        return cls(instance_id, instance_type="t2.micro", region="ap-south-1", hourly_cost=0.0)

# Instantiate from JSON payload:
api_data = '{"id": "i-web-api", "type": "t3.large", "region": "ap-south-1", "cost": 0.0832}'
server_from_api = CloudServerFactory.from_json(api_data)
print(server_from_api)
```

#### C. `@staticmethod` (Utility Functions)
A `@staticmethod` does not access `self` or `cls`. It is a pure helper function logically organized within the class namespace:
```python
class CloudCalculator:
    @staticmethod
    def gib_to_tib(gib: float) -> float:
        return round(gib / 1024, 4)

    @staticmethod
    def calculate_egress_cost(gb_transferred: float, rate_per_gb: float = 0.09) -> float:
        # AWS outbound internet data transfer
        return round(gb_transferred * rate_per_gb, 2)

print("10,240 GiB in TiB:", CloudCalculator.gib_to_tib(10240)) # 10.0
print("Cost for 500 GB egress: $", CloudCalculator.calculate_egress_cost(500)) # $45.0
```

---

### 9.3 Inheritance, Polymorphism & Abstract Base Classes (ABC)
```python
from abc import ABC, abstractmethod

# 1. Abstract Contract
class BaseCloudDriver(ABC):
    def __init__(self, resource_id: str, region: str = "ap-south-1"):
        self.resource_id = resource_id
        self.region = region

    @abstractmethod
    def provision(self):
        """Must be implemented by subclasses!"""
        pass

    @abstractmethod
    def destroy(self):
        """Must be implemented by subclasses!"""
        pass

# 2. Subclasses implementing the contract
class EC2Driver(BaseCloudDriver):
    def provision(self):
        print(f"🚀 [EC2] Provisioning virtual machine '{self.resource_id}' in {self.region}")
    def destroy(self):
        print(f"💥 [EC2] Terminating virtual machine '{self.resource_id}'")

class S3Driver(BaseCloudDriver):
    def provision(self):
        print(f"🪣 [S3] Creating S3 bucket 's3://{self.resource_id}' in {self.region}")
    def destroy(self):
        print(f"🗑️ [S3] Deleting S3 bucket 's3://{self.resource_id}'")

# 3. Polymorphic Fleet Management:
fleet = [EC2Driver("i-001"), EC2Driver("i-002"), S3Driver("task-assets")]
for item in fleet:
    item.provision()
```

---

### 9.4 Dunder (Magic) Methods for Cloud Objects
* `__str__`: Returns clean, user-friendly display string (for `print()` and UI).
* `__repr__`: Returns unambiguous developer debug string (for logs and REPL).
* `__len__`: Returns count of items (e.g. cluster size or bucket object count).
* `__eq__`: Compares objects by identity rather than memory address.

```python
class AutoScalingCluster:
    def __init__(self, name: str):
        self.name = name
        self.instances = []

    def add(self, instance_id: str):
        self.instances.append(instance_id)

    def __len__(self):
        return len(self.instances)

    def __str__(self):
        return f"AutoScalingCluster '{self.name}' with {len(self.instances)} active instances"

    def __repr__(self):
        return f"AutoScalingCluster(name='{self.name}', instances={self.instances})"

    def __eq__(self, other):
        return isinstance(other, AutoScalingCluster) and self.name == other.name

asg = AutoScalingCluster("asg-web-prod")
asg.add("i-01")
asg.add("i-02")
print(str(asg))    # AutoScalingCluster 'asg-web-prod' with 2 active instances
print(len(asg))    # 2
```

---

### 9.5 JavaScript (ES6+ Classes) Equivalent
```javascript
class CloudResource {
    #secretKey = "ENC_KEY_999"; // Private field (ES2022 # prefix - native name mangling!)

    constructor(resourceId, region = "ap-south-1") {
        this.resourceId = resourceId;
        this.region = region;
        this._state = "PENDING";
    }

    // Getter
    get state() {
        return this._state;
    }

    // Setter
    set state(newState) {
        if (this._state === "TERMINATED") {
            throw new Error(`Cannot restart ${this.resourceId}!`);
        }
        this._state = newState;
    }

    // Static Method
    static calculateUptime(hours) {
        return `${(hours / 24).toFixed(1)} days`;
    }
}

class EC2Server extends CloudResource {
    constructor(resourceId, instanceType = "t3.micro", region = "ap-south-1") {
        super(resourceId, region);
        this.instanceType = instanceType;
    }

    start() {
        this.state = "RUNNING";
        console.log(`Booting ${this.instanceType} on ${this.resourceId}`);
    }
}

const node = new EC2Server("i-js-001");
node.start();
console.log("State:", node.state);
console.log("Static helper:", CloudResource.calculateUptime(72));
```

## 10. Asynchronous Programming: Callbacks, Promises & Async/Await

In cloud systems, communicating with remote services (e.g. S3 uploads, DynamoDB queries) takes time. You **cannot block the CPU** while waiting for network responses.

### The JavaScript Event Loop & Promises
```javascript
// Simulating an asynchronous AWS S3 object upload
function uploadToS3(filename, data) {
    return new Promise((resolve, reject) => {
        console.log(`⏳ [S3 Upload] Uploading '${filename}'...`);
        setTimeout(() => {
            if (data && data.length > 0) {
                resolve({ status: 200, location: `s3://nalgonda-bucket/${filename}` });
            } else {
                reject(new Error("Cannot upload empty data payload!"));
            }
        }, 1500); // 1.5 second network delay
    });
}

// 1. Consuming via Promises (.then / .catch)
uploadToS3("app.log", "Sample log output")
    .then(response => console.log("Upload Success:", response.location))
    .catch(error => console.error("Upload Failed:", error.message));

// 2. Consuming via Modern Async / Await (Cleaner, Synchronous-looking style)
async function deployAssetPipeline() {
    try {
        console.log("Starting deployment pipeline...");
        const result = await uploadToS3("bundle.js", "console.log('hello');");
        console.log("🎉 Asset Live at:", result.location);
    } catch (err) {
        console.error("❌ Pipeline broke:", err.message);
    }
}

deployAssetPipeline();
```

### Python Asynchronous (`asyncio` equivalent)
```python
import asyncio

async def upload_to_s3(filename, data):
    print(f"⏳ [S3 Upload] Uploading '{filename}'...")
    await asyncio.sleep(1.5) # Non-blocking sleep
    if data:
        return {"status": 200, "location": f"s3://nalgonda-bucket/{filename}"}
    raise ValueError("Empty payload!")

async def deploy_pipeline():
    try:
        result = await upload_to_s3("bundle.js", "print('hello')")
        print("🎉 Asset Live at:", result["location"])
    except Exception as e:
        print("❌ Error:", e)

# Run the event loop
# asyncio.run(deploy_pipeline())
```

---

## 11. Cloud Developer Real-World Cheatsheet

| Task | Python Idiom | JavaScript (Node.js) Idiom |
| :--- | :--- | :--- |
| **Install AWS SDK** | `pip install boto3` | `npm install @aws-sdk/client-s3` |
| **Environment Variable** | `import os; val = os.environ.get("ENV")` | `const val = process.env.ENV;` |
| **Parse JSON String** | `import json; data = json.loads(text)` | `const data = JSON.parse(text);` |
| **Serialize to JSON** | `import json; text = json.dumps(data)` | `const text = JSON.stringify(data);` |
| **HTTP Request** | `import requests; r = requests.get(url)` | `const res = await fetch(url);` |
| **List Filtering** | `[x for x in items if x > 10]` | `items.filter(x => x > 10);` |
| **Dictionary Merge** | `{**dict1, **dict2}` | `{ ...obj1, ...obj2 }` |
| **String Formatting** | `f"Server {server_id} in {region}"` | `` `Server ${serverId} in ${region}` `` |

---
*Created by **Sundeep Hiremat** for TASK Nalgonda Center · Cloud Software Developer Training Program (2026).*

