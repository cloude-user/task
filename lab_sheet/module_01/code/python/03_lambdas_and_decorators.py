"""
03_lambdas_and_decorators.py -> 03_lambdas_and_closures.py
==========================================================
Topic: Anonymous Lambda Functions & Function Closures (KISS Principle)
Analogy: The Disposable Paper Cup & The Personalized Stamp Maker

ANALOGY FOR STUDENTS:
---------------------
1. Lambda Function = The Disposable Paper Cup.
   - If you just need a sip of water right now, you don't take out a ceramic mug,
     wash it, and put it on a shelf (def function). You grab a paper cup (lambda),
     drink in one second, and toss it!
   - Lambda is for quick, 1-line operations inside sorted(), map(), or filter().

2. Function Closures = The Personalized Stamp Maker.
   - You configure the stamp once with a fixed prefix ("TASK-Nalgonda").
   - It gives you a tool that permanently remembers that setting without retyping it!
"""

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

# Filter using lambda: Volumes larger than or equal to 500 GiB
large_vols = list(filter(lambda v: v["size_gib"] >= 500, ebs_volumes))
print("\nLarge Volumes (>= 500 GiB):", [v["vol_id"] for v in large_vols])


print("\n" + "=" * 70)
print("📦 PART 2: FUNCTION CLOSURES (The Personalized Stamp Maker)")
print("=" * 70)

# Outer function creates and returns an inner function that remembers outer variables
def make_cloud_cost_calculator(hourly_rate: float, currency: str = "USD"):
    """
    Outer function sets up the rate and currency.
    Returns an inner function (closure) that remembers both!
    """
    def calculate(hours: int):
        total = hours * hourly_rate
        return f"{total:.2f} {currency}"
    return calculate

# Specialized calculators configured once
t3_micro_calculator = make_cloud_cost_calculator(0.0208, "USD")
c5_xlarge_calculator = make_cloud_cost_calculator(0.1700, "USD")
storage_inr_calculator = make_cloud_cost_calculator(6.50, "INR")

print("t3.micro for 24 hours:   ", t3_micro_calculator(24))
print("t3.micro for 720 hours:  ", t3_micro_calculator(720))
print("c5.xlarge for 24 hours:  ", c5_xlarge_calculator(24))
print("Storage cost for 30 days:", storage_inr_calculator(30))

print("\n" + "=" * 70)
print("✅ Core functions, lambdas, and closures demonstrated successfully (KISS Principle).")
print("=" * 70)
