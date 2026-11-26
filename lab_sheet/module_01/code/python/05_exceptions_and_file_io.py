"""
05_exceptions_and_file_io.py
=============================
Topic: Exception Handling, File Access Modes, tell(), seek(), Standard Libraries
Analogy: The Car Airbag & The Cassette Tape / Safe Deposit Box

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
     clicks shut and locks automatically!
6. tell() vs seek() = The Cassette Tape:
   - tell() reads the tape timestamp counter.
   - seek() rewinds (seek 0) or fast-forwards the tape.
7. File Modes ('r', 'w', 'a', 'r+', 'w+', 'a+'):
   - 'w' wipes the slate completely clean before writing.
   - 'a' jumps straight to the end so existing data is never destroyed!
"""

import json
import os
import shutil
import glob
import re
import urllib.request
import smtplib
from email.mime.text import MIMEText

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
print("📼 PART 2: FILE ACCESS MODES, tell() & seek() (The Cassette Tape)")
print("=" * 70)

log_filename = "server_tape_log.txt"

# 1. Step A: Initial writing in 'w' mode (creates new, wipes old)
with open(log_filename, "w", encoding="utf-8") as tape:
    tape.write("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
print(f"Created '{log_filename}' with 26 characters.")

# 2. Step B: Navigating pointer with tell() and seek() inside try/except/finally
file_stream = None
try:
    # 'r+' allows reading and writing without wiping the file
    file_stream = open(log_filename, "r+", encoding="utf-8")
    
    print(f"Initial pointer (tell): {file_stream.tell()}")  # 0
    read_head = file_stream.read(5)
    print(f"Read 5 bytes: '{read_head}'")                   # 'ABCDE'
    print(f"Pointer after read:   {file_stream.tell()}")   # 5
    
    # Rewind pointer back to index 2 ('C')
    file_stream.seek(2)
    print(f"Pointer after seek(2):{file_stream.tell()}")   # 2
    next_chunk = file_stream.read(4)
    print(f"Read 4 bytes from pos 2: '{next_chunk}'")      # 'CDEF'
    
    # Jump to end of file to append
    file_stream.seek(0, 2)
    print(f"Pointer at end (seek 0, 2): {file_stream.tell()}")
    file_stream.write("-VERIFIED")

except FileNotFoundError as fnf:
    print(f"❌ File not found: {fnf}")
except Exception as io_err:
    print(f"❌ IO Error: {io_err}")
else:
    print("✅ File pointer operations completed successfully!")
finally:
    if file_stream and not file_stream.closed:
        file_stream.close()
        print("🔒 File stream closed securely.")

# Step C: Verify updated contents
with open(log_filename, "r", encoding="utf-8") as tape:
    print("Final tape content:", tape.read())

if os.path.exists(log_filename):
    os.remove(log_filename)
    print(f"Cleaned up '{log_filename}'.")


print("\n" + "=" * 70)
print("🏦 PART 3: FILE I/O & JSON (The Safe Deposit Box)")
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
    print(f"🧹 Temporary file '{file_path}' cleaned up.")


print("\n" + "=" * 70)
print("🧰 PART 4: STANDARD LIBRARIES (os, shutil, glob, re, urllib, smtplib)")
print("=" * 70)

# 1. os, shutil, glob
print("• os.getcwd():", os.getcwd())
sample_match = glob.glob("*.py")
print("• glob.glob('*.py'):", sample_match[:3])

# 2. re (Regular Expressions)
sample_ip_log = "2026-11-22 ERROR [IP: 192.168.1.100] User login failure."
ip_found = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", sample_ip_log)
if ip_found:
    print("• re.search IP detected:", ip_found.group())
masked_log = re.sub(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", "[REDACTED]", sample_ip_log)
print("• re.sub masked log:   ", masked_log)

# 3. urllib.request
print("• urllib demo: Sending non-blocking check...")
try:
    with urllib.request.urlopen("https://httpbin.org/get", timeout=3) as resp:
        print(f"  HTTP Status: {resp.status}")
except Exception as e:
    print(f"  (Network notice: {e})")

# 4. smtplib template
mime_email = MIMEText("Cloud server deployment complete.")
mime_email["Subject"] = "TASK Notification"
mime_email["From"] = "system@nalgonda.edu"
mime_email["To"] = "students@nalgonda.edu"
print("• smtplib template ready:", mime_email["Subject"])
print("=" * 70)
