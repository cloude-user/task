"""
create_day01_all_notebooks.py
=============================
Generates 6 beginner-friendly, interactive Jupyter Notebooks (.ipynb)
for Day 01 of Cloud Software Developer / Cloud Engineer Mastery.

Written in warm, supportive 1st and 2nd person ("I", "We", "You")
with embedded diagram visuals, runnable code cells, and hands-on exercises:
1. 01_hello_python_and_basics.ipynb
2. 02_variables_numbers_and_memory.ipynb
3. 03_strings_and_cloud_formatting.ipynb
4. 04_lists_tuples_and_dictionaries.ipynb
5. 05_decisions_loops_and_cloud_functions.ipynb
6. 06_aws_cloud_foundations_and_budget_shield.ipynb
"""

import json
import os

NOTEBOOKS_DIR = os.path.dirname(os.path.abspath(__file__))

def make_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.12"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

def md_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().split("\n")]
    }

def code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in code.strip().split("\n")]
    }

# =============================================================================
# NOTEBOOK 1: Hello Python & Basics
# =============================================================================
nb1_cells = [
    md_cell("""# 🐍 Notebook 01: Welcome to Python! Let's Write Our First Code
**Cloud & Software Developer Mastery · Day 01**

Welcome! I am so excited to explore Python and Cloud Engineering with you.

Whether you come from JavaScript, Java, C++, or are looking at Python with fresh eyes, our goal in this notebook is to make Python feel intuitive, friendly, and natural. No scary jargon, no intimidation.

In this notebook, we will:
1. Understand how Python runs your code under the hood.
2. Write and run your very first Python instruction (`print`).
3. Learn how you and I leave notes in our code using **Comments**.
4. Discover Python's famous **Indentation rule** (and why it makes code so clean and readable!).
5. Complete a mini practice challenge.

Let's dive in together!"""),

    md_cell("""### 🔍 Step 1: How Does Python Actually Run Our Code?

Before we run code, let's understand what happens when you press **Run** on a Python file.

Take a look at this diagram:

![How Python Runs Your Code](../images/python_execution_model.png)

Here is the simple, 3-step flow:
- **Step 1: Your Code (`my_code.py`)**: You and I write clean, human-readable Python instructions.
- **Step 2: Bytecode (`my_code.pyc`)**: Python quietly compiles our text into compact instructions.
- **Step 3: Python Virtual Machine (PVM)**: The virtual machine runs those instructions line-by-line on your computer or cloud server.

Let's test this right now in the cell below!"""),

    code_cell("""# Let's run our very first line of Python code together!
print("Hello, Cloud & Software Developer World! We are learning Python together.")"""),

    md_cell("""### 💡 What Just Happened?
When you ran the cell above:
- Python called the built-in function `print()`.
- It sent our friendly message `"Hello, Cloud & Software Developer World!..."` directly to the console.

---

### 📝 Step 2: Comments (Leaving Notes for Yourself and Me)
In Python, any line starting with a hash symbol (`#`) is a **comment**.
Python completely skips comments when running code. We use them to explain our thinking, document cloud resources, or leave helpful hints.

We also have **multi-line docstrings** using triple quotes (`\"\"\"`), which are great for documenting cloud functions."""),

    code_cell("""# This is a single-line comment. Python completely ignores this line!
# We can use it to leave reminders or explain our logic.

print("Comments keep our code friendly and readable.")

\"\"\"
This is a multi-line docstring!
We can write paragraphs here to describe our cloud architectures,
API functions, or data processing pipelines.
\"\"\"
print("Docstrings are great for documenting functions.")"""),

    md_cell("""---
### 📐 Step 3: Printing Multiple Items & Math Results
`print()` is super versatile! You can pass multiple values separated by commas, and Python will automatically insert a space between them. You can also print the result of math calculations directly."""),

    code_cell("""# Printing multiple values together
print("Target Cloud Provider:", "Amazon Web Services", 2026)

# Printing arithmetic results instantly
print("Free Tier EC2 Hours per Month:", 24 * 31.25) # 750 hours!"""),

    md_cell("""---
### 📏 Step 4: Indentation (The 4-Space Rule)
In other languages like Java or C++, people use curly braces `{ }` to define blocks of code, and semicolons `;` at the end of every line.
In Python:
- **No semicolons needed!** Just press Enter.
- **No curly braces `{ }` for code blocks!** Instead, we simply indent by **4 spaces** after a colon (`:`).

Let's see how clean indentation looks:"""),

    code_cell("""# A simple preview of Python's clean indentation
cloud_service = "AWS"

if cloud_service == "AWS":
    # Notice the 4 spaces here!
    print("Welcome to Amazon Web Services!")
    print("Everything inside this indented block belongs to the if statement.")

print("This line is not indented, so it runs after the if block finishes.")"""),

    md_cell("""---
### 🎯 Mini Practice Challenge for You:
In the cell below:
1. Print a welcome message with your name and your goal in this course.
2. Add a friendly single-line comment explaining what your code does.
3. Calculate and print how many hours are in 30 days (`24 * 30`)."""),

    code_cell("""# TODO: Write your code here!
# 1. Print your welcome message
# 2. Add your comment
# 3. Print 24 * 30
"""),

    md_cell("""🎉 **Awesome job!** You have mastered the absolute foundations of Python syntax. Next, let's open **Notebook 02** to see how Python remembers data using Variables and Sticky Labels!""")
]

# =============================================================================
# NOTEBOOK 2: Variables, Numbers & Memory
# =============================================================================
nb2_cells = [
    md_cell("""# 🏷️ Notebook 02: Variables, Numbers & Memory (Friendly Sticky Labels)
**Cloud & Software Developer Mastery · Day 01**

In this notebook, we will demystify how computers remember information in memory.

In many programming courses, variables are taught as "boxes" where you put values. But in Python, there is a much friendlier and more accurate mental model: **Sticky Labels!**

In this session, we will:
1. Understand variables as friendly name tags pointing to objects in memory.
2. See **Dynamic Typing** in action (Python figures out types automatically!).
3. Inspect actual memory addresses using `id()`.
4. Work with Numbers (integers, floating decimals, and arithmetic).
5. Calculate real-world cloud server costs.
6. Discover Python's special **Walrus operator (`:=`)**!"""),

    md_cell("""### 🏷️ Step 1: Variables in Python Are Sticky Labels

Take a look at this visual diagram:

![Variables as Sticky Labels](../images/variables_and_memory.png)

When you write:
```python
developer_name = "Sundeep"
```
Python creates a string object `"Sundeep"` somewhere in the computer's memory (heap), and then attaches the friendly label `developer_name` to it!

Let's prove this by inspecting memory addresses with `id()`:"""),

    code_cell("""# Let's create two variables pointing to the same cloud region
primary_region = "ap-south-1" # Mumbai
backup_region = "ap-south-1"  # Mumbai

print("primary_region value :", primary_region)
print("backup_region value  :", backup_region)

# id() gives us the unique integer memory address in RAM
print("primary_region memory address :", hex(id(primary_region)))
print("backup_region memory address  :", hex(id(backup_region)))

# Are they pointing to the exact same object in memory?
print("Do both point to the same memory object?", primary_region is backup_region)"""),

    md_cell("""### 💡 What Happened?
Both `primary_region` and `backup_region` have the exact same memory address! Python was smart: it created the string `"ap-south-1"` once, and placed both sticky labels on it to save RAM.

Now, what happens if we change `backup_region` to `"ap-south-2"` (Hyderabad)?"""),

    code_cell("""# Reassigning backup_region
backup_region = "ap-south-2" # Hyderabad

print("primary_region :", primary_region, "-> Address:", hex(id(primary_region)))
print("backup_region  :", backup_region,  "-> Address:", hex(id(backup_region)))
print("Are they identical now?", primary_region is backup_region)"""),

    md_cell("""Python simply peeled the `backup_region` sticky label off and attached it to a brand-new string `"ap-south-2"`!

---

### 📦 Step 2: What Can We Store? The Core Python Data Types

Take a look at the data types family:

![Python Core Types](../images/python_core_types.png)

Let's inspect the 4 core primitive types using `type()`:"""),

    code_cell("""# 1. String (Text)
cloud_service = "Amazon EC2"

# 2. Integer (Whole Numbers)
free_tier_hours = 750

# 3. Float (Decimals)
hourly_cost_usd = 0.0116 # Cost of a t3.micro in Mumbai

# 4. Boolean (True or False)
is_running = True

# 5. NoneType (Empty / Missing value)
optional_backup_tag = None

print("cloud_service       :", cloud_service, "| Type:", type(cloud_service).__name__)
print("free_tier_hours     :", free_tier_hours, "| Type:", type(free_tier_hours).__name__)
print("hourly_cost_usd     :", hourly_cost_usd, "| Type:", type(hourly_cost_usd).__name__)
print("is_running          :", is_running, "| Type:", type(is_running).__name__)
print("optional_backup_tag :", optional_backup_tag, "| Type:", type(optional_backup_tag).__name__)"""),

    md_cell("""---
### 🧮 Step 3: Doing Math & Calculating Cloud Costs
Python makes math effortless:
- `+` and `-` : Addition and Subtraction
- `*` and `/` : Multiplication and Division (Division `/` always gives a `float`!)
- `//` : Floor division (chops off decimals)
- `**` : Exponentiation / Power (`2 ** 10 = 1024`)
- `%` : Modulo (remainder)

Let's calculate the real monthly cost of running cloud servers:"""),

    code_cell("""# Cloud Cost Calculator
hours_in_month = 24 * 30 # 720 hours
server_count = 3
hourly_rate = 0.0116     # $0.0116 USD/hour for t3.micro

monthly_total = server_count * hourly_rate * hours_in_month

print("Total server hours consumed :", server_count * hours_in_month, "hours")
print("Gross monthly cost          : $" + str(round(monthly_total, 2)) + " USD")"""),

    md_cell("""---
### 🦭 Step 4: The Walrus Operator (`:=`)
Python 3.8 introduced the **Walrus operator** (`:=`). It looks like a walrus with eyes and tusks!
It allows you to **calculate and assign a variable directly inside an expression or if-check**:"""),

    code_cell("""# Without the walrus operator, you write 2 lines:
# hours = 24 * 35
# if hours > 750: ...

# With the Walrus operator (:=), we do it in one clean line!
if (total_hours := 24 * 35) > 750:
    print(f"Warning: {total_hours} hours exceeds the 750 Free Tier limit!")
else:
    print(f"Safe: {total_hours} hours is within the Free Tier!")"""),

    md_cell("""---
### 🎯 Mini Practice Challenge for You:
In the cell below:
1. Define a variable `instance_type` with the value `"t3.micro"`.
2. Define `monthly_budget` with the value `1.00` (float).
3. Calculate how many hours you could run an instance that costs `$0.05` per hour with a `$10.00` budget.
4. Print your result nicely!"""),

    code_cell("""# TODO: Write your practice code here!
"""),

    md_cell("""🎉 **Brilliant!** You now understand memory labels, data types, and arithmetic. Let's head to **Notebook 03** to master String Magic and Formatting!""")
]

# =============================================================================
# NOTEBOOK 3: Strings & Cloud Formatting
# =============================================================================
nb3_cells = [
    md_cell("""# 🪄 Notebook 03: Working with Text & Cloud Resource Formatting
**Cloud & Software Developer Mastery · Day 01**

In cloud computing and AI engineering, **text is everywhere**:
- Cloud resource IDs (`i-0a89bc37f`)
- Amazon Resource Names (ARNs)
- JSON API payloads
- Log messages and error strings

In this notebook, we will master:
1. Single, double, and triple quotes.
2. Text cleaning superpowers (`.strip()`, `.lower()`, `.replace()`, `.split()`).
3. Slicing any chunk of text with positive and negative indices.
4. Modern **f-strings** (formatted string literals).
5. Escaping JSON braces `{{` and `}}` for cloud API templates!"""),

    md_cell("""### ✂️ Step 1: Quotes & Text Cleaning Superpowers
Python lets you use single quotes `'...'` or double quotes `\"...\"`. They are 100% equivalent!
Using double quotes lets you include single quotes inside without ugly backslash escaping: `"It's running!"`"""),

    code_cell("""# Text cleaning functions
raw_cloud_log = "   WARNING: EC2 instance i-09f821a CPU utilization high!   \\n"

print("Raw Log:")
print(repr(raw_cloud_log))

# .strip() removes whitespace and newlines from both ends
clean_log = raw_cloud_log.strip()
print("\\nAfter .strip():")
print(repr(clean_log))

# .lower() makes everything lowercase for safe matching
print("\\nLowercase for matching:")
print(clean_log.lower())

# .split() breaks a sentence into a clean list of words
words = clean_log.split()
print("\\nSplit into words list:")
print(words)"""),

    md_cell("""---
### 📏 Step 2: Grabbing Any Letter or Chunk with Slicing

Take a look at the string slicing guide:

![String Slicing Guide](../images/string_slicing_guide.png)

In Python:
- Forward counting starts at `0` (the first character is `word[0]`).
- Backward counting starts at `-1` (the last character is `word[-1]`).
- The slice formula is: `sequence[start : stop : step]`.
  - Remember: `stop` is non-inclusive (up to, but not including).

Let's test this on an AWS EC2 Instance ID:"""),

    code_cell("""instance_id = "i-09f48a12bc"

# Grabbing the prefix 'i-'
prefix = instance_id[0:2]
print("Prefix (0:2)        :", prefix)

# Grabbing the hex identifier (from index 2 to end)
identifier = instance_id[2:]
print("Identifier (2:)     :", identifier)

# Grabbing the very last character
last_char = instance_id[-1]
print("Last character (-1) :", last_char)

# Grabbing the last 4 characters
suffix = instance_id[-4:]
print("Last 4 chars (-4:)  :", suffix)"""),

    md_cell("""---
### 🎯 Step 3: F-Strings (The Developer's Best Friend)
Introduced in Python 3.6, **f-strings** (formatted string literals) make injecting variables into text effortless!
Just put an `f` before the opening quote: `f"Hello {name}"`."""),

    code_cell("""service = "ec2"
region = "ap-south-1"
account_id = "123456789012"
res_id = "i-09f48a12bc"

# Constructing an Amazon Resource Name (ARN) effortlessly
arn = f"arn:aws:{service}:{region}:{account_id}:instance/{res_id}"
print("Formatted AWS ARN:")
print(arn)

# Formatting numbers and currency directly inside { }
monthly_cost = 14.85672
print(f"\\nProjected Bill: ${monthly_cost:.2f} USD")"""),

    md_cell("""---
### 🛡️ Step 4: Escaping Curly Braces for Cloud JSON Schemas
What if your text needs to output literal `{` and `}` curly braces (like an AWS CloudFormation or JSON policy template)?
**The Simple Rule: Just double the curly braces: `{{` and `}}`!**"""),

    code_cell("""resource_name = "WebServerFleet"
max_size = 5

# Notice {{ and }} produce literal curly braces in the output!
cloud_config_json = f\"\"\"{{
  "Resource": "{resource_name}",
  "MaxSize": {max_size},
  "AutoScaling": true
}}\"\"\"

print("Rendered Cloud JSON Configuration:")
print(cloud_config_json)"""),

    md_cell("""---
### 🎯 Mini Practice Challenge for You:
In the cell below:
1. Define `app_name = "CloudPaymentService"`.
2. Define `version = 1.4`.
3. Use an f-string to print: `Deploying CloudPaymentService (v1.4) to AWS Mumbai (ap-south-1)`.
4. Slice `app_name` to extract just `"Payment"`!"""),

    code_cell("""# TODO: Write your practice code here!
"""),

    md_cell("""🎉 **Terrific!** Strings and ARNs are now second nature to you. Let's move to **Notebook 04** to discover Collections: Lists, Tuples, Dictionaries, and Sets!""")
]

# =============================================================================
# NOTEBOOK 4: Lists, Tuples & Dictionaries
# =============================================================================
nb4_cells = [
    md_cell("""# 📚 Notebook 04: Collections — Lists, Tuples & Dictionaries
**Cloud & Software Developer Mastery · Day 01**

In real applications, we rarely work with a single variable in isolation. We work with **groups of data**:
- Lists of running EC2 instances
- Dictionaries containing server configuration details
- Sets of unique AWS regions
- Tuples of fixed coordinates

In this notebook, we will master:
1. **Lists vs Dictionaries**: When do we use which?
2. Ordered shopping carts (Lists) and list methods.
3. Locked settings (Tuples) and immutability.
4. Labeled drawers (Dictionaries) and safe `.get()` lookups.
5. Instant deduplication with Sets.
6. Parsing real AWS API JSON structures!"""),

    md_cell("""### 🛒 Step 1: Lists vs Dictionaries — The Simple Rule

Take a look at this comparison diagram:

![List vs Dictionary](../images/list_vs_dictionary.png)

- **Use a List** when items follow an order and you access them by position (`0, 1, 2...`).
  - *Example*: A list of server names, a queue of requests, or a series of hourly CPU metrics.
- **Use a Dictionary** when each item has a meaningful label/key (`key: value`).
  - *Example*: An EC2 instance profile (`'instance_id': 'i-123', 'state': 'running'`)."""),

    code_cell("""# 1. Lists in Action
active_regions = ["ap-south-1", "ap-south-2", "us-east-1"]

# Access by position
print("Primary Region (index 0) :", active_regions[0])
print("Backup Region (index 1)  :", active_regions[1])

# Adding a new region
active_regions.append("eu-central-1")
print("Updated Regions List     :", active_regions)
print("Total Active Regions     :", len(active_regions))"""),

    md_cell("""---
### 🔒 Step 2: Tuples (The Locked List)
A tuple is created with parentheses `( )`. 
Unlike a list, **a tuple CANNOT be changed after creation** (it is immutable). We use tuples to protect fixed settings or geographic coordinates from being accidentally overwritten!"""),

    code_cell("""# Fixed Mumbai Datacenter GPS Coordinates (Latitude, Longitude)
mumbai_dc_coords = (19.0760, 72.8777)

print("Datacenter Coordinates:", mumbai_dc_coords)
print("Latitude :", mumbai_dc_coords[0])
print("Longitude:", mumbai_dc_coords[1])

# If someone tries to change it:
# mumbai_dc_coords[0] = 20.0  <-- Python will raise a TypeError to protect your data!"""),

    md_cell("""---
### 🗄️ Step 3: Dictionaries (Labeled Key-Value Drawers)
Dictionaries use curly braces `{ key: value }`. They are the foundation of all JSON data in AWS!"""),

    code_cell("""# Modeling an Amazon EC2 Instance as a Dictionary
ec2_instance = {
    "InstanceId": "i-09f48a12bc",
    "InstanceType": "t3.micro",
    "State": "running",
    "Region": "ap-south-1",
    "PublicIp": "13.232.45.10"
}

# Accessing values by key
print("Instance ID   :", ec2_instance["InstanceId"])
print("Current State :", ec2_instance["State"])

# Safe access with .get()
# If a key doesn't exist, .get() safely returns a default value instead of crashing!
monitoring = ec2_instance.get("DetailedMonitoring", "disabled")
print("Monitoring    :", monitoring)"""),

    md_cell("""---
### ✨ Step 4: Sets (The Magic Deduplicator)
A Set `{ }` stores **only unique items**. If you add duplicates, Python silently and instantly strips them out!
Checking if an item is in a set is lightning fast ($O(1)$ time)."""),

    code_cell("""# A list with messy duplicate regions from multiple log files
reported_regions = ["ap-south-1", "us-east-1", "ap-south-1", "ap-south-2", "us-east-1", "ap-south-1"]

# Convert to set for instant deduplication!
unique_regions = set(reported_regions)

print("Raw list with duplicates :", reported_regions)
print("Clean deduplicated set   :", unique_regions)"""),

    md_cell("""---
### 🌐 Step 5: Parsing Real AWS API Responses
When you call AWS using Python Boto3, AWS returns nested dictionaries and lists. Let's practice navigating real AWS JSON!"""),

    code_cell("""# Simulated AWS EC2 DescribeInstances API response
aws_response = {
    "Reservations": [
        {
            "Instances": [
                {
                    "InstanceId": "i-01a2b3c4d5",
                    "InstanceType": "t3.micro",
                    "State": {"Name": "running"},
                    "Tags": [
                        {"Key": "Environment", "Value": "Production"},
                        {"Key": "Owner", "Value": "DevTeamAlpha"}
                    ]
                }
            ]
        }
    ]
}

# Navigating the nested structure step-by-step
first_instance = aws_response["Reservations"][0]["Instances"][0]
print("Found Instance ID :", first_instance["InstanceId"])
print("Current Status    :", first_instance["State"]["Name"])
print("Environment Tag   :", first_instance["Tags"][0]["Value"])"""),

    md_cell("""---
### 🎯 Mini Practice Challenge for You:
In the cell below:
1. Create a dictionary called `my_server` with keys: `"name"`, `"ip"`, and `"port"` (value `80`).
2. Add a new key `"status"` with the value `"active"`.
3. Use `.get()` to look up `"backup_status"`, defaulting to `"none"`.
4. Print your dictionary!"""),

    code_cell("""# TODO: Write your practice code here!
"""),

    md_cell("""🎉 **Outstanding!** You now know how to store, structure, and navigate data in Python. Let's open **Notebook 05** to master Decisions, Loops, and Functions!""")
]

# =============================================================================
# NOTEBOOK 5: Decisions, Loops & Cloud Functions
# =============================================================================
nb5_cells = [
    md_cell("""# ⚙️ Notebook 05: Decisions, Loops & Reusable Cloud Functions
**Cloud & Software Developer Mastery · Day 01**

Now that you know how to store data, it is time to make decisions and automate repetitive work!

In this notebook, we will master:
1. **Decisions with `if / elif / else`**.
2. **Repeating tasks with `for` loops** (no off-by-one errors!).
3. Using `enumerate()` to count items automatically.
4. Packaging reusable logic into **Functions with `def`**.
5. Putting everything together to build our **First Mini Cloud Automation Agent**!"""),

    md_cell("""### 🔀 Step 1: Decisions (`if / elif / else`)

Take a look at the control flow diagram:

![Decisions and Loops](../images/if_else_and_loops.png)

Python checks conditions from top to bottom. As soon as one condition evaluates to `True`, Python executes its indented block and skips the rest!"""),

    code_cell("""# Checking server health status
cpu_utilization = 84.5 # percentage

if cpu_utilization >= 90.0:
    print("🚨 CRITICAL: CPU above 90%! Triggering Auto Scaling to add more servers.")
elif cpu_utilization >= 75.0:
    print("⚠️ WARNING: CPU above 75%. Monitoring closely.")
else:
    print("✅ HEALTHY: Server workload is normal.")"""),

    md_cell("""---
### 🔄 Step 2: Loops (`for` Loops Across Cloud Resources)
In other languages, people write manual counting loops like `for (int i = 0; i < len; i++)`, which often cause nasty off-by-one bugs.
In Python, we simply iterate directly over the items: `for server in servers:`. It runs smoothly and safely every time!"""),

    code_cell("""server_fleet = [
    {"id": "i-001", "name": "AuthService", "healthy": True},
    {"id": "i-002", "name": "PaymentAPI",  "healthy": False},
    {"id": "i-003", "name": "WebFrontend", "healthy": True}
]

# Inspecting each server in the fleet
for server in server_fleet:
    status_symbol = "✅" if server["healthy"] else "❌"
    print(f"{status_symbol} Server {server['name']} ({server['id']}) - Healthy: {server['healthy']}")"""),

    md_cell("""---
### 🔢 Step 3: `enumerate()` — Getting Both Index and Item
Need to number items as you loop? Don't create a manual counter variable! Just use `enumerate()`:"""),

    code_cell("""regions = ["ap-south-1 (Mumbai)", "ap-south-2 (Hyderabad)", "us-east-1 (Virginia)"]

# enumerate(list, start=1) numbers them starting at 1!
for rank, region_name in enumerate(regions, start=1):
    print(f"Priority {rank}: {region_name}")"""),

    md_cell("""---
### 📦 Step 4: Packaging Reusable Logic into Functions (`def`)
A function is a reusable block of code that takes inputs (arguments), does work, and returns a result with `return`.
Functions keep our code DRY (Don't Repeat Yourself)!"""),

    code_cell("""def estimate_ec2_cost(instance_count: int, hourly_rate: float = 0.0116, days: int = 30) -> float:
    \"\"\"
    Estimates monthly EC2 cost for a fleet of instances.
    Default hourly rate is $0.0116 (t3.micro in Mumbai).
    \"\"\"
    total_hours = instance_count * 24 * days
    total_cost = total_hours * hourly_rate
    return round(total_cost, 2)

# Calling our function with different inputs
single_dev_cost = estimate_ec2_cost(instance_count=1)
prod_cluster_cost = estimate_ec2_cost(instance_count=10, hourly_rate=0.0464) # larger instances

print(f"Single Dev Instance Monthly Cost : ${single_dev_cost} USD")
print(f"Production Cluster Monthly Cost  : ${prod_cluster_cost} USD")"""),

    md_cell("""---
### 🤖 Step 5: Putting It All Together: Our First Mini Cloud Automation Agent!
Let's combine strings, decisions, dictionaries, and functions to create an automated Cloud Assistant that inspects server requests!"""),

    code_cell("""def cloud_ops_agent(command: str) -> str:
    \"\"\"A simple rule-based cloud automation assistant.\"\"\"
    clean_cmd = command.strip().lower()
    
    if "cost" in clean_cmd or "budget" in clean_cmd:
        return "💰 Cloud Budget Info: The $1.00 Budget Shield is ACTIVE with 80% email alerts."
    elif "status" in clean_cmd or "health" in clean_cmd:
        return "📊 Fleet Status: 3 instances running in Mumbai (ap-south-1). All systems healthy."
    elif "region" in clean_cmd:
        return "🌐 Active Regions: ap-south-1 (Mumbai, Primary) and ap-south-2 (Hyderabad, Standby)."
    else:
        return f"🤖 Agent: Command '{command}' received. Logging to CloudWatch."

# Let's test our agent with different queries!
print(cloud_ops_agent("What is our current monthly cost?"))
print(cloud_ops_agent("Show server status please"))
print(cloud_ops_agent("Which active regions do we use?"))"""),

    md_cell("""---
### 🎯 Mini Practice Challenge for You:
In the cell below:
1. Write a function `check_free_tier(hours_used: float) -> str`.
2. If `hours_used > 750`, return `"Over limit!"`.
3. Otherwise, return `"Within Free Tier!"`.
4. Test it with `700` and `800` hours!"""),

    code_cell("""# TODO: Write your practice code here!
"""),

    md_cell("""🎉 **Incredible!** You have now mastered complete Python fundamentals: syntax, variables, text, collections, decisions, loops, and functions. 

Now, let's open **Notebook 06** to see how all of this connects directly to the **AWS Cloud & The $1.00 Budget Shield**!""")
]

# =============================================================================
# NOTEBOOK 6: AWS Cloud Foundations & The Budget Shield
# =============================================================================
nb6_cells = [
    md_cell("""# ☁️ Notebook 06: AWS Cloud Foundations & The $1.00 Budget Shield
**Cloud & Software Developer Mastery · Day 01**

Welcome to the Cloud portion of Day 01!

Now that you have solid Python superpowers, let's explore **what the Cloud actually is**, why companies build on AWS, and how you can experiment with complete confidence without ever having to worry about spending money.

In this notebook, we will:
1. Understand the Cloud through the friendly **Electric Power Grid** analogy.
2. Explore AWS Global & India Infrastructure (Mumbai `ap-south-1` & Hyderabad `ap-south-2`).
3. Learn who manages what using the **Landlord & Tenant** Shared Responsibility Model.
4. Deploy the **Zero-Spend $1.00 Budget Shield** using Python.
5. Generate an official AWS Budgets JSON configuration!"""),

    md_cell("""### 💡 Step 1: What is the Cloud? (The Power Grid Mental Model)

In the 1800s, when a factory opened, it had to build its own private steam engine, coal shed, and generator. It required a team of full-time mechanics just to generate electricity.

When Thomas Edison and Nikola Tesla built the centralized AC power grid, factories tore down their coal engines and plugged into the wall socket. They paid only for the kilowatt-hours they used.

**Amazon Web Services (AWS) is the planetary electric grid of computational power:**
- You don't buy physical computers, pour concrete, or buy diesel generators.
- You plug into AWS via code and APIs.
- You run your software and pay strictly for the seconds of compute you consume!"""),

    code_cell("""# Comparing On-Premise Datacenter vs Cloud Utility Model
def compare_hosting(physical_server_cost, power_and_cooling_annual, cloud_hourly_rate):
    hours_per_year = 24 * 365 # 8760 hours
    
    on_prem_cost = physical_server_cost + power_and_cooling_annual
    cloud_cost = cloud_hourly_rate * hours_per_year
    savings = on_prem_cost - cloud_cost
    
    return {
        "On-Premise (CapEx)": f"${on_prem_cost:,.2f} USD",
        "AWS Cloud (OpEx)": f"${cloud_cost:,.2f} USD",
        "First Year Savings": f"${savings:,.2f} USD ({round((savings/on_prem_cost)*100)}% cheaper!)"
    }

print("Hosting Cost Comparison:")
for k, v in compare_hosting(5000.0, 1800.0, 0.0116).items():
    print(f"• {k:<20}: {v}")"""),

    md_cell("""---
### 🌐 Step 2: Regions & Availability Zones (India Deep Dive)
- **AWS Region**: A separate geographic area (e.g. `ap-south-1` Mumbai, `ap-south-2` Hyderabad).
- **Availability Zone (AZ)**: Discrete physical data centers inside a region, separated by 10 to 100 kilometers, linked by high-speed dark fiber (< 1.5ms latency).
- In India, having **both Mumbai and Hyderabad** allows banks and healthcare systems to achieve 100% in-country Disaster Recovery without sensitive customer data ever leaving the country!"""),

    code_cell("""# Modeling Indian Cloud Infrastructure in Python
aws_india_infrastructure = {
    "ap-south-1": {
        "city": "Mumbai",
        "launched": 2016,
        "availability_zones": ["ap-south-1a", "ap-south-1b", "ap-south-1c"],
        "role": "Primary Commercial & Financial Capital Anchor"
    },
    "ap-south-2": {
        "city": "Hyderabad",
        "launched": 2022,
        "availability_zones": ["ap-south-2a", "ap-south-2b", "ap-south-2c"],
        "role": "Secondary In-Country Disaster Recovery & Gov Anchor"
    }
}

for region_code, info in aws_india_infrastructure.items():
    print(f"\\nRegion: {region_code} ({info['city']})")
    print(f"  Role: {info['role']}")
    print(f"  AZs : {', '.join(info['availability_zones'])}")"""),

    md_cell("""---
### 🤝 Step 3: The Shared Responsibility Model (The Landlord & Tenant Analogy)
Think of renting an apartment:
- **The Landlord (AWS)**: Responsible for the building foundations, exterior walls, roof, elevators, and front gate security (**Security OF the Cloud**).
- **The Tenant (You)**: Responsible for locking your apartment door, not leaving candles burning, and who you invite inside (**Security IN the Cloud**).

When you run an Amazon EC2 server:
- AWS ensures the physical server hardware and power don't fail.
- You ensure your software is updated, your firewall ports are secure, and your passwords/keys are protected!"""),

    code_cell("""# Shared Responsibility Matrix Checker
def who_is_responsible(component: str) -> str:
    component_lower = component.lower()
    if any(k in component_lower for k in ["physical", "datacenter", "hardware", "power", "cooling", "nitro"]):
        return "AWS Responsibility (Security OF the Cloud)"
    elif any(k in component_lower for k in ["os patch", "code", "password", "firewall", "data encryption", "iam"]):
        return "Customer / Developer Responsibility (Security IN the Cloud)"
    else:
        return "Shared / Service Dependent"

print("• Physical Server Power :", who_is_responsible("Physical Server Power"))
print("• Linux OS Security Patch:", who_is_responsible("Linux OS Security Patch"))
print("• Application Code Bugs :", who_is_responsible("Application Code Bugs"))
print("• Datacenter Perimeter  :", who_is_responsible("Datacenter Perimeter Gates"))"""),

    md_cell("""---
### 🛡️ Step 4: The Zero-Spend $1.00 Budget Shield
Every beginner worries: *"What if I accidentally leave a server running and get a big bill?"*

To solve this on Day 1, we set up **The $1.00 Budget Shield**:
- Free Tier gives you **750 hours/month** of micro instances (runs 1 server 24/7 for free).
- We create an automated AWS Budget set to **$1.00 USD**.
- We configure an automated email alert at **80% ($0.80)**.
- If actual OR forecasted spend crosses 80 cents, AWS instantly emails you!"""),

    code_cell("""def calculate_budget_shield(running_servers: int, days: int = 30):
    \"\"\"Calculates monthly hours, charges, and shield alert triggers.\"\"\"
    FREE_TIER_HOURS = 750.0
    HOURLY_RATE = 0.0116 # t3.micro in Mumbai
    BUDGET_LIMIT = 1.00
    ALERT_THRESHOLD = 0.80 # 80%
    
    total_hours = running_servers * 24 * days
    billable_hours = max(0.0, total_hours - FREE_TIER_HOURS)
    projected_bill = billable_hours * HOURLY_RATE
    alarm_fired = projected_bill >= ALERT_THRESHOLD
    
    return {
        "servers": running_servers,
        "total_hours": total_hours,
        "free_tier_allowed": FREE_TIER_HOURS,
        "billable_hours": billable_hours,
        "projected_bill_usd": f"${projected_bill:.2f}",
        "shield_alarm_triggered": alarm_fired
    }

print("Scenario A (1 Server 24/7):")
print(calculate_budget_shield(1))

print("\\nScenario B (2 Servers 24/7 - Exceeds Free Tier):")
print(calculate_budget_shield(2))"""),

    md_cell("""---
### 📄 Step 5: Generating the Official AWS Budgets JSON Payload
Let's use Python's built-in `json` module to generate the exact JSON configuration payload you can feed to the AWS CLI or AWS Console:"""),

    code_cell("""import json

def generate_budget_json(student_email: str):
    budget_payload = {
        "Budget": {
            "BudgetName": "CloudDeveloper-OneDollarShield",
            "BudgetLimit": {"Amount": "1.00", "Unit": "USD"},
            "TimeUnit": "MONTHLY",
            "BudgetType": "COST"
        },
        "NotificationsWithSubscribers": [
            {
                "Notification": {
                    "NotificationType": "ACTUAL",
                    "ComparisonOperator": "GREATER_THAN",
                    "Threshold": 80.0,
                    "ThresholdType": "PERCENTAGE"
                },
                "Subscribers": [
                    {"SubscriptionType": "EMAIL", "Address": student_email}
                ]
            }
        ]
    }
    return json.dumps(budget_payload, indent=2)

print("Generated AWS Budgets JSON (Ready for AWS CLI v2):")
print(generate_budget_json("student@college.edu"))"""),

    md_cell("""---
### 🏆 Day 01 Milestone Complete!
Look at what you have accomplished today:
1. **Python Foundations**: Syntax, variables as sticky labels, memory inspection with `id()`, strings, slicing, f-strings, lists, dictionaries, tuples, sets, decisions, loops, and functions.
2. **AWS Cloud Foundations**: The electric grid mental model, Regions, AZs, Mumbai & Hyderabad infrastructure, and the Shared Responsibility model.
3. **Financial Protection**: The $1.00 Budget Shield is verified and ready.

In **Day 02**, we will install the **AWS CLI v2** in our terminal, configure our credentials, and start running cloud commands directly from our command prompt! 🚀""")
]

# Write all notebooks to disk
notebooks_data = [
    ("01_hello_python_and_basics.ipynb", nb1_cells),
    ("02_variables_numbers_and_memory.ipynb", nb2_cells),
    ("03_strings_and_cloud_formatting.ipynb", nb3_cells),
    ("04_lists_tuples_and_dictionaries.ipynb", nb4_cells),
    ("05_decisions_loops_and_cloud_functions.ipynb", nb5_cells),
    ("06_aws_cloud_foundations_and_budget_shield.ipynb", nb6_cells),
]

for filename, cells in notebooks_data:
    filepath = os.path.join(NOTEBOOKS_DIR, filename)
    nb_content = make_notebook(cells)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(nb_content, f, indent=2)
    print(f"[CREATED] {filepath}")

print("\n>>> ALL 6 DAY 01 NOTEBOOKS SUCCESSFULLY GENERATED! <<<")

