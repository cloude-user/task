"""
05_exceptions_and_file_io.py
=============================
Topic: Exception Handling, Custom Exceptions, File I/O & JSON Serialization
Analogy: The Car Airbag & The Safe Deposit Box

ANALOGY FOR STUDENTS:
---------------------
1. try = Driving the car safely.
2. except = The Airbag deploying during an impact.
   - The car doesn't disintegrate into dust (server crash); the airbag catches you
     and you step out safely!
3. else = The trip was successful, no accident occurred!
4. finally = Unbuckling your seatbelt and taking your car keys with you.
   - Whether you had an accident or arrived safely, you ALWAYS unbuckle and take your keys!
5. Context Manager ('with') = The Bank Vault Door.
   - You step inside, do your business, and when you step out, the vault door
     clicks shut and locks automatically, even if you tripped on your shoelaces!
"""

import json
import os

print("=" * 70)
print("🛡️ PART 1: EXCEPTION HANDLING (The Airbag & Seatbelt)")
print("=" * 70)

# Custom Cloud Exception
class MonthlyQuotaExceeded(Exception):
    """Airbag deployed when student exceeds AWS monthly spending limit."""
    pass

def launch_server_safely(instance_type, current_cost, max_budget):
    print(f"\n🚗 [TRY] Attempting to launch '{instance_type}' (Current spend: ${current_cost})...")
    try:
        cost_lookup = {"t2.micro": 15.0, "t3.medium": 45.0, "c5.xlarge": 150.0}
        
        if instance_type not in cost_lookup:
            raise KeyError(f"Unknown instance type '{instance_type}'")
            
        new_cost = current_cost + cost_lookup[instance_type]
        if new_cost > max_budget:
            raise MonthlyQuotaExceeded(
                f"BUDGET BREACH! Launching {instance_type} would cost ${new_cost}, exceeding cap of ${max_budget}."
            )
            
        print(f"🎉 [SUCCESS] {instance_type} launched! New balance: ${new_cost}.")
        return True

    except KeyError as ke:
        print(f"⚠️ [AIRBAG 1 - Invalid Input]: {ke}")
        return False
    except MonthlyQuotaExceeded as mqe:
        print(f"🛑 [AIRBAG 2 - Cost Shield]: {mqe}")
        return False
    except Exception as e:
        print(f"💥 [AIRBAG 3 - General Crash]: Unexpected failure: {e}")
        return False
    else:
        print("🟢 [ELSE] Trip finished smoothly with zero collisions!")
    finally:
        print("🔒 [FINALLY] Unbuckling seatbelt & logging transaction to CloudTrail.")

# Test Scenario A: Breaches budget
launch_server_safely("c5.xlarge", 200.0, 250.0)

# Test Scenario B: Smooth success
launch_server_safely("t2.micro", 50.0, 250.0)


print("\n" + "=" * 70)
print("🏦 PART 2: FILE I/O & JSON (The Safe Deposit Box)")
print("=" * 70)

config_data = {
    "Project": "Cloud Portfolio",
    "Center": "TASK Nalgonda",
    "Trainer": "Sundeep Hiremat",
    "ActiveFleet": [
        {"id": "i-web-01", "role": "frontend", "public_ip": "13.233.45.10"},
        {"id": "i-db-01",  "role": "database", "public_ip": None}
    ],
    "Security": {
        "VpcId": "vpc-0987654321",
        "OpenPorts": [80, 443, 22]
    }
}

file_path = "cloud_manifest_demo.json"

# Writing JSON with 'with' (Safe Deposit Box auto-closing)
print(f"Writing cloud config to '{file_path}'...")
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(config_data, f, indent=4)
print("✅ File written and locked safely.")

# Reading JSON back into memory
print(f"Reading cloud config from '{file_path}'...")
with open(file_path, "r", encoding="utf-8") as f:
    loaded_data = json.load(f)

print(f"\n📂 Extracted from file:")
print(f"Trainer: {loaded_data['Trainer']}")
print(f"VPC ID:  {loaded_data['Security']['VpcId']}")
for s in loaded_data["ActiveFleet"]:
    print(f"  • {s['id']} ({s['role']}) -> Public IP: {s['public_ip']}")

# Cleanup demo file
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"\n🧹 Temporary file '{file_path}' cleaned up.")
