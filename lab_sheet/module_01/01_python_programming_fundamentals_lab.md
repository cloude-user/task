# Lab Sheet 1.1: Python Programming Foundations & Core Logic
> **Module 1:** Programming Foundations  
> **Topic 1.a:** Python Developer Setup, Syntax, Collections & File I/O  
> **Target:** Cloud Software Developer Trainees  

---

## 🎯 Lab Objectives
1. Configure local Python 3.12+ development environment in VS Code.
2. Practice Python core syntax: Variables, data types, f-strings, conditionals, and loops.
3. Master Python collections: Lists, Dictionaries, Tuples, and Sets.
4. Write modular functions and manage clean virtual environments (`venv`).
5. Implement error handling (`try/except`) and parse JSON cloud data.

---

## 🛠️ Step-by-Step Hands-On Exercises

### Exercise 1: Python Virtual Environment Setup
Open your terminal (PowerShell or Bash) and execute:
```bash
# 1. Create a dedicated project directory
mkdir python_cloud_lab && cd python_cloud_lab

# 2. Create a clean virtual environment
python -m venv .venv

# 3. Activate the virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# 4. Verify python path
python --version
```

---

### Exercise 2: Variables, F-Strings & Collections
Create a script named `01_cloud_inventory.py`:
```python
# Cloud Server Inventory Script
servers = [
    {"name": "web-01", "ip": "10.0.1.10", "type": "t2.micro", "status": "running"},
    {"name": "api-01", "ip": "10.0.2.20", "type": "t3.medium", "status": "running"},
    {"name": "db-01",  "ip": "10.0.3.30", "type": "r5.large",  "status": "stopped"},
]

print("=== ACTIVE CLOUD INSTANCES ===")
for s in servers:
    if s["status"] == "running":
        print(f"Server: {s['name']:<8} | Private IP: {s['ip']:<12} | Tier: {s['type']}")
```
Run the script: `python 01_cloud_inventory.py`.

---

### Exercise 3: Exception Handling & JSON Processing
Create a script named `02_parse_cloud_config.py`:
```python
import json

cloud_config_json = '''
{
  "stack_name": "production-vpc",
  "region": "ap-south-1",
  "subnets": ["10.0.1.0/24", "10.0.2.0/24"],
  "max_instances": 5
}
'''

try:
    data = json.loads(cloud_config_json)
    print(f"Successfully loaded stack: {data['stack_name']} in Region: {data['region']}")
    print(f"Configured Subnets: {len(data['subnets'])}")
except json.JSONDecodeError as err:
    print(f"Error parsing configuration JSON: {err}")
except KeyError as err:
    print(f"Missing mandatory configuration key: {err}")
finally:
    print("Configuration parse execution completed.")
```
Run the script: `python 02_parse_cloud_config.py`.

---

### ✅ Verification Checklist
- [ ] Virtual environment `.venv` active in terminal.
- [ ] Inventory script filters and formats active servers cleanly.
- [ ] JSON parser handles parsing and exceptions gracefully.
