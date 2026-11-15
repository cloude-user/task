"""
01_variables_and_collections.py
================================
Topic: Python Data Types, Collections, and Slicing
Analogy: The Cloud Storage Locker System

ANALOGY FOR STUDENTS:
---------------------
1. Variable = A labeled plastic storage bin.
   - You put data inside and slap a sticker on it ("instance_type").
2. List [] = A numbered train compartments / shopping rack.
   - Ordered, flexible, you can add, remove, and change items anytime.
3. Tuple () = A sealed legal certificate / stamped birth certificate.
   - Once written, nobody can change it (Immutable). Perfect for database coordinates.
4. Dictionary {} = A hotel room keycard rack (Key ➔ Room / Name ➔ Phone).
   - You don't look up by number; you look up by the name on the keycard!
5. Set {} = A VIP guest list (No duplicates allowed).
   - If someone tries to enter twice, the list ignores the duplicate.
"""

print("=" * 70)
print("📦 PART 1: VARIABLES & TYPES (The Storage Locker)")
print("=" * 70)

# Primitive Types
region = "ap-south-1"      # str
instance_count = 3         # int
hourly_rate = 0.0208       # float
is_running = True          # bool
elastic_ip = None          # NoneType (Empty slot)

print(f"Region: {region} (Type: {type(region).__name__})")
print(f"Count:  {instance_count} (Type: {type(instance_count).__name__})")
print(f"Rate:   ${hourly_rate}/hr (Type: {type(hourly_rate).__name__})")
print(f"Active: {is_running} (Type: {type(is_running).__name__})")
print(f"IP:     {elastic_ip} (Type: {type(elastic_ip).__name__})\n")


print("=" * 70)
print("🛒 PART 2: LISTS & SLICING (The Numbered Train Compartments)")
print("=" * 70)

# Lists: Ordered, mutable sequence
servers = ["web-01", "web-02", "app-01", "app-02", "db-01"]
print("Original servers:", servers)

# Adding and removing
servers.append("cache-01")
print("After append:   ", servers)

# Slicing: [start : stop_before : step]
# Analogy: Slicing a loaf of bread between knife marks
print("First 2 servers (0:2):", servers[0:2])
print("Middle servers  (2:4):", servers[2:4])
print("Last server     (-1): ", servers[-1])
print("Reversed fleet  (::-1):", servers[::-1])

# List Comprehension (Fast, clean filtering)
web_tier = [s.upper() for s in servers if s.startswith("web")]
print("Filtered Web Tier:    ", web_tier, "\n")


print("=" * 70)
print("📜 PART 3: TUPLES (The Sealed Legal Certificate)")
print("=" * 70)

# Tuples: Immutable
db_credentials = ("mysql.cluster.internal", 3306, "admin")
print("DB Host:", db_credentials[0])
print("DB Port:", db_credentials[1])

# Unpacking tuples (Analogy: opening the sealed envelope into 3 labeled trays)
host, port, user = db_credentials
print(f"Unpacked: Host={host}, Port={port}, User={user}\n")


print("=" * 70)
print("🔑 PART 4: DICTIONARIES (The Hotel Keycard Rack)")
print("=" * 70)

# Dictionaries: Key ➔ Value
ec2_config = {
    "InstanceId": "i-0abc123456789def0",
    "InstanceType": "t3.micro",
    "State": {"Code": 16, "Name": "running"},
    "Tags": {
        "Environment": "Production",
        "Project": "Cloud Portfolio",
        "Center": "TASK Nalgonda"
    }
}

# Accessing
print("Instance ID:", ec2_config["InstanceId"])
# Safe access with .get() (Analogy: Asking front desk, returns 'Not Found' instead of crashing)
monitoring = ec2_config.get("DetailedMonitoring", "DISABLED (Default)")
print("Monitoring: ", monitoring)

# Nested access
env = ec2_config.get("Tags", {}).get("Environment", "Unknown")
print("Environment:", env, "\n")


print("=" * 70)
print("🎟️ PART 5: SETS (The VIP Guest List - No Duplicates)")
print("=" * 70)

# Sets eliminate duplicate data automatically
logged_regions = ["ap-south-1", "us-east-1", "ap-south-1", "eu-west-1", "us-east-1"]
unique_regions = set(logged_regions)

print("Logged calls (with duplicates):", logged_regions)
print("Unique Regions (Set deduplicated):", unique_regions)

# Set Operations (Union, Intersection)
approved_regions = {"ap-south-1", "ap-south-2", "us-east-1"}
active_and_approved = unique_regions.intersection(approved_regions)
print("Regions Active & Approved:", active_and_approved)

