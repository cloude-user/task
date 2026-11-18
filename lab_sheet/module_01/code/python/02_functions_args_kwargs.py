"""
02_functions_args_kwargs.py
============================
Topic: Functions, Default Parameters, Positional-only, *args and **kwargs
Analogy: The Courier Delivery System

ANALOGY FOR STUDENTS:
---------------------
1. Positional Arguments = The Mandatory Delivery Address.
   - You MUST write the house number and city in the exact order.
2. Default Arguments = The Standard Shipping Option.
   - If the customer doesn't choose shipping, it defaults to "Standard Delivery" ($5).
3. Keyword-Only Arguments (*) = The Fragile Glass Warning.
   - You CANNOT just mutter it; you MUST explicitly label it "Fragile=True".
4. *args = The Open Delivery Sack (Unordered items).
   - Whatever loose packages you drop into the truck get packed into a single tuple.
5. **kwargs = The Labeled Luggage Tags (Key-Value options).
   - "Weight=5kg", "Express=True", "Recipient=Sundeep". Packed into a dictionary!
"""

print("=" * 70)
print("📦 PART 1: DEFAULT ARGUMENTS & THE MUTABLE DEFAULT PITFALL")
print("=" * 70)

# WRONG (The Sticky Contamination Trap):
# def add_tag(tag, tags=[]): tags.append(tag); return tags
# In Python, default [] is created ONCE at compile time. All calls share the same list!

# RIGHT (Fresh parcel on every call):
def attach_tag_safe(resource_id: str, tag: str, current_tags: list = None) -> list:
    if current_tags is None:
        current_tags = []  # create brand new list for this specific call
    current_tags.append(tag)
    print(f"[{resource_id}] Tags attached: {current_tags}")
    return current_tags

print("Call 1 (Server A):")
attach_tag_safe("i-001", "Production")

print("Call 2 (Server B - notice it's clean and has NO Production tag!):")
attach_tag_safe("i-002", "Staging")


print("\n" + "=" * 70)
print("🛑 PART 2: KEYWORD-ONLY ARGUMENTS (The Explicit Danger Switch)")
print("=" * 70)

# The '*' forces everything after it to be passed with an explicit name!
def deploy_server(image_id: str, instance_type: str = "t3.micro", *, enable_termination_protection: bool = False):
    print(f"Launching {instance_type} from {image_id}")
    print(f"  Termination Protection: {enable_termination_protection}")

# Valid call (explicit):
deploy_server("ami-0abc123", "t3.small", enable_termination_protection=True)

# Invalid call:
# deploy_server("ami-0abc123", "t3.small", True) # Raises TypeError! Python protects you from passing wrong flags!


print("\n" + "=" * 70)
print("🎒 PART 3: *args (The Open Delivery Sack -> Tuple)")
print("=" * 70)

def notify_cloudwatch_alarms(severity: str, *target_emails):
    """*target_emails captures any count of emails into a single tuple."""
    print(f"🚨 [Alarm: {severity}] Sending alert to {len(target_emails)} recipients:")
    for email in target_emails:
        print(f"   ✉️ Sending email to: {email}")

notify_cloudwatch_alarms("CRITICAL", "devops@company.com", "oncall@company.com", "manager@company.com")


print("\n" + "=" * 70)
print("🏷️ PART 4: **kwargs (The Labeled Parcel Tags -> Dictionary)")
print("=" * 70)

def create_boto3_resource_client(service_name: str, region: str = "ap-south-1", **client_config):
    """Simulates how AWS boto3 client accepts dynamic keyword options."""
    print(f"\n⚡ Initializing AWS Client: '{service_name}' in region '{region}'")
    print(f"   Configuration Options ({type(client_config).__name__}):")
    for key, value in client_config.items():
        print(f"   • {key} = {value}")

create_boto3_resource_client(
    "ec2",
    "us-east-1",
    use_ssl=True,
    max_retries=5,
    timeout_seconds=30,
    verify_checksum=True
)


print("\n" + "=" * 70)
print("🪄 PART 5: UNPACKING OPERATORS (* and **)")
print("=" * 70)

# Analogy: Pouring the contents of a box directly onto the table
default_regions = ["ap-south-1", "ap-south-2", "us-east-1"]
custom_options = {"auto_scale": True, "min_size": 2, "max_size": 10}

def audit_fleet_deployment(fleet_name, *regions, **options):
    print(f"Auditing fleet '{fleet_name}'")
    print(f"Target Regions: {regions}")
    print(f"Fleet Options:  {options}")

# We unpack the list with * and unpack the dictionary with **
audit_fleet_deployment("Web-Production-Fleet", *default_regions, **custom_options)
