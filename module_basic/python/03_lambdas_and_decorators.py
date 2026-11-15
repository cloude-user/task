"""
03_lambdas_and_decorators.py
=============================
Topic: Anonymous Lambda Functions & Function Decorators
Analogy: The Disposable Cup & The Airport Security Checkpoint

ANALOGY FOR STUDENTS:
---------------------
1. Lambda Function = The Disposable Paper Cup / Quick Token.
   - If you just need a sip of water right now, you don't take out a ceramic mug,
     wash it, and put it on a shelf (def function). You grab a paper cup (lambda),
     drink in one second, and toss it!
   - Lambda is for quick, 1-line operations inside sorted(), map(), or filter().

2. Decorator (@) = The Airport Security Scanner & Passport Stamp.
   - Every passenger (function) that wants to board the flight (execute)
     MUST pass through the security scanner first.
   - The security guard (decorator wrapper) checks your ticket, logs your arrival time,
     and if you're cleared, lets you proceed!
"""

import time
import functools

print("=" * 70)
print("🥤 PART 1: LAMBDA FUNCTIONS (The Disposable Paper Cup)")
print("=" * 70)

# Standard function (The Ceramic Mug)
def calculate_ebs_monthly_cost(gib):
    return gib * 0.08

# Equivalent Lambda (The Disposable Paper Cup)
# Syntax: lambda arguments : expression
calc_ebs = lambda gib: gib * 0.08

print("Ceramic Mug result: $", calculate_ebs_monthly_cost(100))
print("Paper Cup result:   $", calc_ebs(100))

# REAL CLOUD USE CASE: Sorting Cloud Storage by Sizing & Cost
ebs_volumes = [
    {"vol_id": "vol-01", "size_gib": 500, "type": "gp3", "cost_usd": 40.0},
    {"vol_id": "vol-02", "size_gib": 50,  "type": "io2", "cost_usd": 15.0},
    {"vol_id": "vol-03", "size_gib": 1000, "type": "gp2", "cost_usd": 100.0},
    {"vol_id": "vol-04", "size_gib": 20,   "type": "gp3", "cost_usd": 1.60}
]

# Sort by size ascending using a lambda key
by_size = sorted(ebs_volumes, key=lambda v: v["size_gib"])
print("\nEBS Volumes sorted by size (smallest to largest):")
for v in by_size:
    print(f"  • {v['vol_id']}: {v['size_gib']} GiB (${v['cost_usd']}/mo)")

# Filter using lambda: Volumes larger than 100 GiB
large_vols = list(filter(lambda v: v["size_gib"] >= 500, ebs_volumes))
print("\nLarge Volumes (>= 500 GiB):", [v["vol_id"] for v in large_vols])


print("\n" + "=" * 70)
print("🛂 PART 2: DECORATORS (The Airport Security Checkpoint)")
print("=" * 70)

# Decorator 1: Latency / Execution Time Logger (CloudWatch Metric Tracker)
def log_latency(func):
    """Airport Security Checkpoint: Measures how long passenger takes to pass."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n🛫 [Security Gate] Starting execution of: '{func.__name__}'")
        start = time.time()
        
        # Execute the original function!
        result = func(*args, **kwargs)
        
        elapsed_ms = (time.time() - start) * 1000
        print(f"🛬 [Security Gate] '{func.__name__}' completed in {elapsed_ms:.2f} ms")
        return result
    return wrapper

# Decorator 2: Cloud Resilience Auto-Retry (Exponential Backoff)
def retry_on_cloud_throttle(max_attempts=3, delay_sec=1):
    """Retries a failed API call if AWS responds with throttling / 429."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    attempts += 1
                    print(f"⚠️ [Attempt {attempts}/{max_attempts}] AWS API throttled: {err}. Retrying in {delay_sec}s...")
                    time.sleep(delay_sec)
            raise RuntimeError(f"❌ Function '{func.__name__}' failed permanently after {max_attempts} attempts.")
        return wrapper
    return decorator


# Applying BOTH decorators to an AWS API call!
# (Decorators stack like layers of security checkpoints!)
simulated_network_failures = 0

@log_latency
@retry_on_cloud_throttle(max_attempts=3, delay_sec=0.5)
def upload_file_to_s3(bucket_name, file_name):
    global simulated_network_failures
    simulated_network_failures += 1
    
    # Simulate network hiccups on first 2 calls
    if simulated_network_failures < 2:
        raise ConnectionResetError("503 Service Unavailable / Network Jitter")
        
    return f"s3://{bucket_name}/{file_name} uploaded successfully."

# Run the decorated function
response = upload_file_to_s3("task-nalgonda-assets", "portfolio_template.zip")
print("\nFinal Result from AWS:", response)
