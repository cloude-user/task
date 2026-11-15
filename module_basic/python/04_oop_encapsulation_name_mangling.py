"""
04_oop_encapsulation_name_mangling.py
======================================
Topic: Object-Oriented Programming (OOP), Name Mangling, and Decorators in Classes
Analogy: The Automotive Factory, The Bank Vault, and The Nightclub Bouncer

ANALOGY FOR STUDENTS:
---------------------
1. Class vs Object = Car CAD Blueprints (Class) vs Actual Cars driving on the road (Objects).
   - "Tata Nexon Blueprint" (Class) ➔ Your specific white Tata Nexon with registration TS-08-AB-1234 (Object).
2. Public = Car Exterior Color / Speedometer. (Anyone can see it).
3. Protected (_) = The Engine Dipstick. (Mechanics and internal family members check it; public shouldn't touch it randomly).
4. Private (__ with Name Mangling) = The Secret Factory Airbag Code / Master Bank Vault.
   - Python physically locks it behind a security gate: _ClassName__secret.
5. @property & @setter = The Nightclub Bouncer / Security Turnstile.
   - You don't just walk into the club (set state). The bouncer checks your ID.
   - If the server is already TERMINATED, the bouncer throws you out!
6. @classmethod = The Pre-configured Car Assembly Line.
   - e.g. Factory.build_sports_edition() or Factory.build_free_tier_economy().
7. @staticmethod = The Dashboard Digital Clock / Calculator.
   - Doesn't need the engine or steering wheel; just tells the time or converts GiB to TiB.
"""

from abc import ABC, abstractmethod
import json
import re

print("=" * 70)
print("🚗 PART 1: CLASS BLUEPRINTS & THE BANK VAULT (Name Mangling)")
print("=" * 70)

class CloudServer:
    # Class Attribute (The Manufacturer Logo: shared by all servers)
    cloud_provider = "AWS"

    def __init__(self, instance_id: str, iam_secret_key: str):
        # Public: Open to the world
        self.instance_id = instance_id
        
        # Protected (_): Internal use by convention
        self._operational_mode = "STANDARD"
        
        # Private (__): THE BANK VAULT (Python triggers NAME MANGLING!)
        self.__iam_secret_key = iam_secret_key

    def get_masked_credentials(self):
        """Safe method: shows last 4 digits only."""
        return f"****-****-{self.__iam_secret_key[-4:]}"

# Instantiating the server
node = CloudServer("i-prod-007", "SECRET_KEY_NALGONDA_SECURE_9999")

print(f"Server ID (Public):    {node.instance_id}")
print(f"Status (Protected):    {node._operational_mode}")
print(f"Masked Key (via safe method): {node.get_masked_credentials()}")

# Trying to access __iam_secret_key directly -> FAILS!
try:
    print(node.__iam_secret_key)
except AttributeError as err:
    print("❌ DIRECT ACCESS BLOCKED BY PYTHON:", err)

# 🔍 DEMONSTRATING NAME MANGLING:
# Notice how Python renamed '__iam_secret_key' to '_CloudServer__iam_secret_key'
mangled_name = "_CloudServer__iam_secret_key"
print(f"🔍 Accessing via mangled name ({mangled_name}):", getattr(node, mangled_name))


print("\n" + "=" * 70)
print("🚪 PART 2: @property & @setter (The Nightclub Bouncer)")
print("=" * 70)

class ManagedInstance:
    VALID_LIFECYCLE = {"PENDING", "RUNNING", "STOPPED", "TERMINATED"}

    def __init__(self, instance_id: str, ip_address: str):
        self.instance_id = instance_id
        self._state = "PENDING"
        self._ip_address = None
        self.ip_address = ip_address # triggers setter validation!

    # GETTER (Looking at the display)
    @property
    def state(self):
        return self._state

    # SETTER (The Bouncer guarding state transitions)
    @state.setter
    def state(self, new_state: str):
        new_state = new_state.upper()
        if new_state not in self.VALID_LIFECYCLE:
            raise ValueError(f"Unknown state '{new_state}'. Allowed: {self.VALID_LIFECYCLE}")
            
        # The ultimate guard: Cannot resurrect a destroyed instance!
        if self._state == "TERMINATED":
            raise RuntimeError(f"⛔ BOUNCER REJECTION: Server {self.instance_id} is TERMINATED. It cannot be restarted!")
            
        print(f"🔄 State Transition for {self.instance_id}: {self._state} ➔ {new_state}")
        self._state = new_state

    # IP Address Setter with Regex Validation
    @property
    def ip_address(self):
        return self._ip_address

    @ip_address.setter
    def ip_address(self, new_ip: str):
        pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
        if not re.match(pattern, new_ip):
            raise ValueError(f"Invalid IPv4 format: '{new_ip}'")
        self._ip_address = new_ip

# Testing the bouncer
inst = ManagedInstance("i-web-alpha", "13.233.45.10")
inst.state = "RUNNING"
inst.state = "STOPPED"
inst.state = "TERMINATED"

# Attempt illegal restart
try:
    inst.state = "RUNNING"
except RuntimeError as err:
    print(err)


print("\n" + "=" * 70)
print("🏭 PART 3: @classmethod & @staticmethod (Factory Lines & Calculators)")
print("=" * 70)

class ServerFactory:
    def __init__(self, name: str, instance_type: str, hourly_rate: float):
        self.name = name
        self.instance_type = instance_type
        self.hourly_rate = hourly_rate

    def __repr__(self):
        return f"<ServerFactory: '{self.name}' ({self.instance_type}) - ${self.hourly_rate}/hr>"

    # Class Method: Factory Line from JSON API string
    @classmethod
    def from_api_json(cls, json_payload: str):
        data = json.loads(json_payload)
        return cls(name=data["name"], instance_type=data["type"], hourly_rate=data["rate"])

    # Class Method: Free Tier Economy Assembly Line
    @classmethod
    def free_tier_edition(cls, name: str):
        return cls(name=name, instance_type="t2.micro", hourly_rate=0.0)

    # Static Method: Pure Math Calculator (Doesn't touch self or cls)
    @staticmethod
    def calculate_monthly_bill(hourly_rate: float, hours: int = 730) -> float:
        return round(hourly_rate * hours, 2)

# Using Class Methods (Factory Lines):
s1 = ServerFactory.from_api_json('{"name": "production-api", "type": "c5.xlarge", "rate": 0.17}')
s2 = ServerFactory.free_tier_edition("student-sandbox")

print("Created via JSON factory:     ", s1)
print("Created via Free-Tier factory:", s2)

# Using Static Method (Dashboard Calculator):
print("Monthly bill for production-api: $", ServerFactory.calculate_monthly_bill(0.17))


print("\n" + "=" * 70)
print("📜 PART 4: ABSTRACT BASE CLASSES (ABC) & POLYMORPHISM")
print("=" * 70)

# The Contract: Every Cloud Service MUST be able to deploy and destroy
class AbstractCloudService(ABC):
    def __init__(self, service_id: str):
        self.service_id = service_id

    @abstractmethod
    def deploy(self):
        pass

    @abstractmethod
    def destroy(self):
        pass

class EC2Service(AbstractCloudService):
    def deploy(self):
        print(f"🚀 [EC2] Launching virtual machine '{self.service_id}'...")
    def destroy(self):
        print(f"💥 [EC2] Terminating virtual machine '{self.service_id}'.")

class S3Service(AbstractCloudService):
    def deploy(self):
        print(f"🪣 [S3] Creating cloud bucket 's3://{self.service_id}'...")
    def destroy(self):
        print(f"🗑️ [S3] Deleting cloud bucket 's3://{self.service_id}'.")

# Polymorphic Execution (One loop handles all different cloud resources)
cloud_stack = [EC2Service("i-web-01"), EC2Service("i-app-01"), S3Service("task-nalgonda-data")]

print("--- DEPLOYING CLOUD STACK ---")
for resource in cloud_stack:
    resource.deploy()

print("\n--- DESTROYING CLOUD STACK ---")
for resource in cloud_stack:
    resource.destroy()
