# Module 03 · Part A: AWS VPC & Cloud Networking Master Guide
> **TASK (Telangana Academy for Skill and Knowledge) · Nalgonda Center**  
> **Course:** Cloud Software Developer (AWS EC2-Centric / DVA-C02 Alignment)  
> **Trainer:** Sundeep Hiremat  
> **PDF Guide:** [Module_03_Part_A_VPC_and_Networking_Master_Guide.pdf](file:///e:/trainer/task/notes/Module_03_Part_A_VPC_and_Networking_Master_Guide.pdf)

---

## 🗺️ Visual Architecture Diagram

![AWS VPC Architecture](file:///e:/trainer/task/module_03_aws_core/notes/diagrams/01_vpc_networking_architecture.png)

---

## 🎬 1. The Master Tollywood Analogy: "Sandhya 70mm Multiplex Compound" at RTC X Roads

When non-tech students in Telangana hear terms like *CIDR, subnets, route tables, IGW, NAT, and security groups*, it sounds like alien jargon.  
To make these concepts permanently stick, think of an AWS VPC as **The Famous Sandhya 70mm / Prasad's IMAX Multiplex Compound on the day of a massive Sankranti Tollywood Star Hero Blockbuster release (First Day First Show - FDFS)**:

| AWS Networking Component | Tollywood Cinema Analogy | What It Actually Does in AWS (Technical Reality) |
| :--- | :--- | :--- |
| **Amazon VPC** | **The Sandhya 70mm Boundary Compound Wall** | A logically isolated, private slice of the AWS Cloud dedicated to your account. Nobody enters or leaves the compound without explicit routes and gates. |
| **CIDR Block (`10.0.0.0/16`)** | **Total Theatre Seating Capacity & Layout (65,536 Chairs)** | Defines the total pool of internal private IP addresses (plots/chairs) available to assign to servers and services. |
| **Public Subnet (`10.0.1.0/24`)** | **Front Ticket Counter & Popcorn Canteen Area** | A subnet whose Route Table directs `0.0.0.0/0` directly to the **Internet Gateway**. It is open to any movie fan walking along RTC X Roads. |
| **Private Subnet (`10.0.2.0/24`)** | **The Projector Room & Producer's Cash Safe (Galla Pette)** | A subnet with NO direct route to the Internet Gateway. Completely shielded deep inside the building; road fans cannot just walk in! |
| **Internet Gateway (IGW)** | **The Main Double-Door Grand Highway Gate** | A horizontally scaled, redundant, highly available 2-way gate connecting the cinema compound to the public highway. Performs 1-to-1 NAT for public IPs. |
| **NAT Gateway** | **The Theatre Boy with an Outbound Gate Pass** | Deployed in the Public Canteen with an Elastic IP badge. Fetches projector spare parts or Swiggy biryani lunch from outside without letting outside strangers enter! |
| **Route Table** | **Theatre Direction Signboards ("Way to Screen 1 / Canteen")** | A set of routing rules that determine where network packets are directed (e.g., local traffic stays in the compound; outside traffic goes to IGW/NAT). |
| **Security Group (SG)** | **Bouncer Anna at the Screen 1 Door (Stateful Guard)** | **Stateful firewall** operating at the individual EC2/ENI level. If Bouncer Anna allows you in, he remembers your face and **automatically lets you return** from the interval without re-checking your ticket! |
| **Network ACL (NACL)** | **Police Checkpost at RTC X Roads Junction (Stateless)** | **Stateless firewall** operating at the subnet boundary. Police check your helmet & RC on entry, AND they **explicitly re-check your helmet & RC on exit**! |
| **Route 53 Resolver (`10.0.0.2`)** | **The Theatre Enquiry Counter Desk ("May I Help You?")** | Internal recursive DNS server at `VPC Base + 2`. Translates internal staff names (e.g., `safe.producer.internal`) and public domain names (`bookmyshow.com`). |

---

## 🔢 2. The 5 AWS Reserved IP Addresses in Every Subnet

> [!IMPORTANT]
> In traditional on-premises networking, only **2 IP addresses** are reserved per subnet (Network Address `.0` and Broadcast Address `.255`).  
> **In AWS, exactly 5 IP addresses are ALWAYS reserved** in every single CIDR subnet block!  
> For a `/24` subnet ($2^8 = 256$ total addresses), **only 251 IP addresses are usable**.

### The Mathematical Formula:
$$\text{Usable IPs} = 2^{(32 - \text{Prefix})} - 5$$

For `10.0.1.0/24`:
$$2^{(32 - 24)} - 5 = 256 - 5 = 251 \text{ usable IPs}$$

### Tabular Breakdown of the 5 Reserved IPs:

| IP Address | AWS Reservation Name | Tollywood Cinema Analogy & Technical Function |
| :--- | :--- | :--- |
| **`10.0.1.0`** | **Network Address** | **The Theatre Plot Boundary Line:** Identifies the network block itself on municipal records. You cannot place a viewer's chair directly on top of the boundary line! |
| **`10.0.1.1`** | **VPC Router** | **The Hall Security Officer & Default Gateway:** The internal router that directs traffic between different halls and out through the main gates. |
| **`10.0.1.2`** | **Amazon-Provided DNS (Route 53 Resolver)** | **The Central Enquiry Desk:** Internal DNS server that answers queries for internal and external names. Always calculated as `VPC CIDR Base + 2`. |
| **`10.0.1.3`** | **Future Use** | **The Reserved VIP Protocol Row:** Kept empty by AWS for future platform capabilities (e.g., MLA / Police Commissioner protocol). |
| **`10.0.1.255`** | **Network Broadcast** | **The Lobby Megaphone (Unused):** Reserved broadcast address. *Note: AWS VPC networking does not support IP broadcast or multicast, but this address remains reserved.* |

---

## 🚪 3. Traffic Routing: Internet Gateway (IGW) vs NAT Gateway

```
[ Public Internet: 0.0.0.0/0 (RTC X Roads Highway) ]
                        │ ▲
                        │ │  (Two-Way Direct Traffic)
                        ▼ │
        [ Internet Gateway (Main Grand Gate) ]
                        │ ▲
                        ▼ │
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏢 PUBLIC SUBNET (10.0.1.0/24) · "Front Ticket Counter & Canteen Area"       │
│  • Route Table: 0.0.0.0/0 ➔ igw-xxxx                                        │
│  • Hosts: Application Load Balancer (ALB) & Theatre Boy (NAT GW with EIP)   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ ▲
                                       │ │  (Outbound ONLY via NAT)
                                       ▼ │
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔒 PRIVATE SUBNET (10.0.2.0/24) · "Projector Room & Producer Cash Safe"     │
│  • Route Table: 0.0.0.0/0 ➔ nat-xxxx                                        │
│  • Hosts: EC2 App Servers ('Operator Desks') & RDS ('Galla Pette')          │
│  • Inbound Internet Scans: 100% BLOCKED                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1. Internet Gateway (IGW) - The Main Grand Boulevard Gate
- **What is it?** A horizontally scaled, redundant, highly available software component attached to the VPC.
- **Why use it?** Enables instances with public IPs in public subnets to connect directly to the internet, and internet movie fans to reach your public web services.
- **Requirements:**
  1. Must be attached to the VPC.
  2. Public Subnet's Route Table must contain: `Destination: 0.0.0.0/0` ➔ `Target: igw-xxxx`.
  3. The EC2 instance must have a **Public IPv4 address** or an **Elastic IP**.

### 2. NAT Gateway - The Theatre Boy with Outbound Gate Pass
- **What is it?** A managed AWS service that translates private IP addresses to a single public IP for outbound internet access.
- **Why use it?** Enables backend EC2 servers in the private projector room to download Linux patches (`apt update`, `pip install`) or call external APIs (Stripe, Twilio) **without exposing them to incoming internet attacks**.
- **Crucial Architecture Rules:**
  1. **Placement:** NAT Gateway **MUST be created inside a Public Subnet** (because it needs direct internet access).
  2. **Elastic IP:** NAT Gateway **MUST be allocated an Elastic IP (EIP)** badge.
  3. **Routing:** The Route Table of the **Private Subnet** must point: `Destination: 0.0.0.0/0` ➔ `Target: nat-xxxx`.

---

## 🛡️ 4. Firewalls: Security Groups (Stateful) vs Network ACLs (Stateless)

```
Incoming Packet
       │
       ▼
 [ Network ACL ]  <─── Subnet Level (Stateless Police Checkpost)
       │
       ▼
 [ Security Group ]  <─── Instance / ENI Level (Stateful Bouncer Anna)
       │
       ▼
  [ EC2 Instance ]
```

| Feature / Metric | Security Group (Bouncer Anna at Screen Door) | Network ACL (Police Checkpost at RTC X Roads) |
| :--- | :--- | :--- |
| **Operating Level** | Instance / ENI (Elastic Network Interface) level | Subnet boundary level (protects all instances in subnet) |
| **State Tracking** | **Stateful:** Bouncer Anna remembers you! If traffic is permitted inbound, **the return traffic is automatically allowed** out regardless of outbound rules. | **Stateless:** Police check your helmet & RC entering AND explicitly re-check your helmet & RC exiting! Return traffic must be explicitly allowed. |
| **Rule Types** | **Allow rules ONLY.** Everything else is denied by default (implicit deny). | **Allow AND Deny rules** are both supported. |
| **Evaluation Order** | All rules are evaluated simultaneously before granting access. | Rules are evaluated in strict **ascending numerical order** (e.g. 100, 200, *). The first rule that matches wins! |
| **Default Configuration** | Default SG: Allows all outbound, denies all inbound. Custom SG: Denies all inbound until rules added. | Default NACL: Allows all inbound and outbound. Custom NACL: Denies all inbound and outbound until rules added. |
| **Primary Use Case** | Primary day-to-day security: Opening port 80/443 for web, port 22 for SSH, port 5432 for Postgres. | Subnet-wide security policies: Blacklisting specific malicious IP addresses or blocking compromised CIDR ranges. |

---

## 📖 5. How the Amazon VPC DNS Resolver Works (`10.0.0.2` / Base + 2)

![DNS Resolution Flow](file:///e:/trainer/task/module_03_aws_core/notes/diagrams/02_dns_resolver_flow.png)

### The Reserved Address (`VPC Base + 2`)
Every AWS VPC provides a managed internal DNS service known as **AmazonProvidedDNS** (or the **Route 53 Resolver**).
The resolver IP is **always located at the 2nd usable IP of the VPC CIDR base**:
- For VPC `10.0.0.0/16` $\rightarrow$ Resolver IP is **`10.0.0.2`** (The Enquiry Counter)
- For VPC `172.16.0.0/16` $\rightarrow$ Resolver IP is **`172.16.0.2`**
- For VPC `192.168.0.0/16` $\rightarrow$ Resolver IP is **`192.168.0.2`**

### Step-by-Step Resolution Flow:
1. **The Application Query:** The movie operator on EC2 `10.0.2.15` asks for `safe.producer.internal` (the database) or `bookmyshow.com` (external API).
2. **Local Resolver Forwarding:** The operating system's DNS resolver configuration (`/etc/resolv.conf`) forwards the request to `10.0.0.2`.
3. **Route 53 Private Hosted Zone Check:**
   - The Route 53 Resolver first checks if the requested domain exists in a **Private Hosted Zone** associated with this VPC.
   - If found (e.g. `safe.producer.internal ➔ 10.0.3.50`), it returns the private IP within microseconds!
4. **Recursive Internet Resolution:**
   - If the domain is an external internet name (`bookmyshow.com`), the resolver acts as a recursive DNS server over the IGW/NAT to authoritative root nameservers and returns the public IP (`140.82.121.6`).
5. **Two Mandatory VPC DNS Settings:**
   - `enableDnsSupport = true`: Activates the built-in `10.0.0.2` resolver.
   - `enableDnsHostnames = true`: Assigns public DNS hostnames to instances with public IPs.

---

## 🌐 6. Public DNS vs Private DNS in Route 53

| Metric | Public Hosted Zone (Route 53) | Private Hosted Zone (Route 53) |
| :--- | :--- | :--- |
| **Everyday Metaphor** | **BookMyShow Public Movie Schedule Listings** | **Producer's Confidential Staff Intercom List** |
| **Accessibility** | Accessible by **anyone on the global internet** worldwide. | Accessible **ONLY by resources inside the VPCs** linked to the zone. |
| **Domain Examples** | `sandhya70mm.com`, `bookmyshow.com` | `safe.producer.internal`, `auth.vpc.local` |
| **Resolved IP Type** | Resolves to **Public IPv4/IPv6 addresses**, ALBs, or CloudFront. | Resolves to **Private RFC 1918 IPs** (e.g. `10.0.2.50`, `10.0.3.100`). |
| **Visibility / Privacy** | Visible to hackers running `dig` or `nslookup`. | **100% Invisible to the outside internet.** External queries return `NXDOMAIN` (domain does not exist). |
| **Use Case** | Serving public movie fans visiting your website. | Internal microservice-to-microservice traffic and database endpoints without hardcoding private IPs. |

---

## 🔒 7. How HTTPS Works Under the Hood (The Titanium Security Briefcase)

### The Analogy:
- **Plain HTTP (Port 80):** Like sending a postcard through the mail. Every tea stall boy, auto driver, and coffee shop Wi-Fi hacker can read your passwords in clear text!
- **HTTPS (Port 443):** Like locking your money and contract inside a **tamper-proof titanium briefcase** with a dual Godrej cryptographic lock.

```
[ Student Browser ]                                      [ AWS Application Load Balancer ]
        │                                                               │
        │ 1. Client Hello (Supported TLS versions & Ciphers)            │
        ├──────────────────────────────────────────────────────────────►│
        │                                                               │
        │ 2. Server Hello + TLS Certificate (Contains Server Public Key)│
        │◄──────────────────────────────────────────────────────────────┤
        │                                                               │
        │ 3. Browser verifies Certificate signature with Root CA        │
        │    (Locks briefcase using Server's Public Key)                │
        │                                                               │
        │ 4. Client Key Exchange (Sends Encrypted Symmetric Session Key)│
        ├──────────────────────────────────────────────────────────────►│
        │                                                               │ 5. Server decrypts Session Key
        │                                                               │    using its secret Private Key!
        │                                                               │
        │◄══════════════════════════════════════════════════════════════►│
        │ 6. Fast Symmetric AES Encrypted Tunnel Established!            │
        │    All HTTP data, headers, and cookies are encrypted          │
```

1. **Step 1: Client Hello:** The client browser contacts the server on **Port 443** and shares supported ciphers (e.g., TLS 1.3).
2. **Step 2: Server Hello & Certificate:** The server responds with its **Digital Certificate** containing its **Public Key** (the open padlock).
3. **Step 3: Verification:** The browser checks the certificate against built-in operating system Root Certificate Authorities.
4. **Step 4: Session Key Generation:** The browser creates a temporary **Symmetric Session Key**, encrypts it using the server's **Public Key**, and transmits it.
5. **Step 5: Server Decryption:** Only the server possesses the corresponding secret **Private Key**. It unlocks the message and extracts the session key.
6. **Step 6: Secure Channel:** From here on, both sides encrypt all web traffic using fast symmetric AES encryption.

### TLS Termination at the Application Load Balancer (ALB):
- **AWS Certificate Manager (ACM):** Provisions free, auto-renewing SSL/TLS certificates.
- **ALB Handles Encryption:** The Multiplex Chief Manager (ALB) terminates HTTPS on Port 443 at the edge, decrypts the traffic, inspects the URL path (`/tickets` vs `/canteen`), and forwards plain HTTP (Port 80) across private VPC subnets to the backend EC2 fleet.
- **Benefit:** Offloads heavy mathematical cryptographic decryption from backend EC2 servers, preserving 100% of their CPU power for application code!

---

## 🏷️ 8. IP Addressing Comparison: Private IP vs Public IP vs Elastic IP

| Property | Private IPv4 | Public IPv4 | Elastic IP (EIP) |
| :--- | :--- | :--- | :--- |
| **Tollywood Analogy** | **Ticket Seat Number A-15** | **Temporary Bike Parking Token #42** | **Producer's Permanent VIP Fortuner Sticker** |
| **Scope** | Internal within VPC only | Publicly accessible across internet | Publicly accessible across internet |
| **Stop / Start Behavior** | **RETAINED:** Remains unchanged when instance stops and starts. | **LOST & CHANGED:** The public IP is returned to the AWS pool upon stopping. A new random IP is assigned on start! | **PERMANENT:** Remains attached to the instance across stops and starts until manually disassociated. |
| **DNS Implication** | Perfect for internal microservice communication via Route 53 Private Zones. | Dangerous for direct DNS records because the IP changes if the instance is rebooted/stopped. | Ideal for public web servers or NAT Gateways requiring a fixed static public IP. |
| **Pricing** | **100% Free** (No charge) | Standard IPv4 public address charges apply. | Free while attached to a running instance; **hourly idle charge if unattached**! |

---

## ⚖️ 9. Elastic Load Balancing: ALB vs NLB

| Metric | Application Load Balancer (ALB) | Network Load Balancer (NLB) |
| :--- | :--- | :--- |
| **OSI Layer** | **Layer 7 (Application Layer)** | **Layer 4 (Transport Layer)** |
| **Protocols** | HTTP, HTTPS, gRPC, WebSockets | TCP, UDP, TLS |
| **Tollywood Analogy** | **Multiplex Chief Manager:** Reads the ticket menu (URL path `/tickets` vs `/canteen`), inspects cookies, and seats guests in Screen 1 or Screen 2. | **High-Speed Express Ticket Conveyor Belt:** Ultra-fast, does not read passenger details, moves raw TCP packets at light speed. |
| **Throughput & Speed** | High throughput with ~10ms latency. | **Ultra-low sub-millisecond latency; millions of requests per second.** |
| **IP Address Support** | Dynamic IP addresses (Must access via DNS name). | **Static IP addresses** (Provides 1 fixed Elastic IP per AZ). |

---

## 🏢 10. Production 3-Tier Enterprise Web Architecture Pattern

```
                  [ Movie Fans on Public Internet ]
                                 │
                                 ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ PUBLIC SUBNET (AZ-a & AZ-b) · "Front Canteen & Counters"    │
 │  • Internet-Facing Application Load Balancer (ALB)          │
 │  • Theatre Boy (NAT Gateway with Elastic IP in AZ-a)        │
 │  • Route: 0.0.0.0/0 ➔ Internet Gateway                      │
 └───────────────────────────┬─────────────────────────────────┘
                             │  Forward Port 80/443
                             ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ PRIVATE APPLICATION SUBNET · "Operator Desks (EC2 ASG)"     │
 │  • EC2 Auto Scaling Group running Web/API code              │
 │  • Security Group: Inbound Port 80/8080 from ALB SG ONLY    │
 │  • Route: 0.0.0.0/0 ➔ NAT Gateway (Outbound updates only)   │
 └───────────────────────────┬─────────────────────────────────┘
                             │  Forward Port 5432
                             ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ ISOLATED DATABASE SUBNET · "Producer Cash Safe (Galla Pette)│
 │  • Amazon RDS Multi-AZ PostgreSQL Database                  │
 │  • Security Group: Inbound Port 5432 from App EC2 SG ONLY   │
 │  • Route: Local ONLY (10.0.0.0/16) - NO Internet Access     │
 └─────────────────────────────────────────────────────────────┘
```

---
*Created by **Sundeep Hiremat** for TASK Nalgonda Center · Cloud Software Developer Mastery Program (2026).*
