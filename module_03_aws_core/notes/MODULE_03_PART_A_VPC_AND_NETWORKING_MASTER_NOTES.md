# Module 03 · Part A: AWS VPC & Cloud Networking Master Guide
> **TASK (Telangana Academy for Skill and Knowledge) · Nalgonda Center**  
> **Course:** Cloud Software Developer (AWS EC2-Centric / DVA-C02 Alignment)  
> **Trainer:** Sundeep Hiremat  
> **PDF Guide:** [Module_03_Part_A_VPC_and_Networking_Master_Guide.pdf](file:///e:/trainer/task/notes/Module_03_Part_A_VPC_and_Networking_Master_Guide.pdf)

---

## 🗺️ Visual Architecture Diagram

![AWS VPC Architecture](file:///e:/trainer/task/module_03_aws_core/notes/diagrams/01_vpc_networking_architecture.png)

---

## 🏛️ 1. The Master Analogy: The "Cyberabad Ultra-Secure Smart City"

When students learn cloud networking, terms like *CIDR, subnets, route tables, IGW, NAT, and security groups* feel like abstract invisible layers. To make them permanently stick in memory, think of an AWS VPC as **an ultra-modern, high-security corporate gated township built outside Hyderabad ("Cyberabad Smart City")**:

| AWS Networking Component | Smart City Gated Township Analogy | What It Actually Does in AWS |
| :--- | :--- | :--- |
| **Amazon VPC** | **The Gated Township Boundary Wall** | A logically isolated virtual network dedicated to your AWS account. You control the IP range, subnets, routing, and network gateways. |
| **CIDR Block (`10.0.0.0/16`)** | **Township Postal Code & Land Plot Allocation** | Defines the total pool of internal private IP addresses (e.g. `10.0.0.0/16` gives 65,536 private IP addresses). |
| **Public Subnet (`10.0.1.0/24`)** | **Front Commercial Showroom Lane** | A subnet whose route table directs default internet traffic (`0.0.0.0/0`) directly to the **Internet Gateway**. Hosts public load balancers and bastion hosts. |
| **Private Subnet (`10.0.2.0/24`)** | **High-Security Residential Colony / Underground Bank Vault** | A subnet with NO direct route to the Internet Gateway. Houses application backend servers and databases, shielded from external internet scans. |
| **Internet Gateway (IGW)** | **The Main Highway Boulevard Gate (2-Way Entrance)** | A horizontally scaled, redundant, highly available VPC component that enables communication between your VPC and the public internet. Performs 1-to-1 NAT for public IPv4 addresses. |
| **NAT Gateway** | **The One-Way Diplomatic Security Courier Escort** | Deployed in a Public Subnet with an Elastic IP. Allows private instances to fetch software updates (Linux patches, Python packages) from the internet without letting internet hackers see or reach them. |
| **Route Table** | **Township Traffic GPS Navigation & Direction Signs** | A set of routing rules that determine where network packets are directed (e.g., local traffic stays within the township; unknown traffic goes to the IGW or NAT). |
| **Security Group (SG)** | **Personal Apartment Bouncer / Bodyguard** | **Stateful firewall** operating at the individual instance / Elastic Network Interface (ENI) level. If inbound traffic is allowed, return traffic is automatically allowed. |
| **Network ACL (NACL)** | **Subnet Border Police Checkpoint / Tollbooth** | **Stateless firewall** operating at the subnet boundary. Evaluates rules in strict numerical order (100, 200, *). Must explicitly permit both inbound and outbound traffic. |
| **Route 53 Resolver (`10.0.0.2`)** | **The Township Directory & Information Desk** | Internal recursive DNS server at VPC Base + 2. Resolves private domains (e.g. `db.internal`) and public domain lookups. |

---

## 🔢 2. The 5 AWS Reserved IP Addresses in Every Subnet

> [!IMPORTANT]
> In traditional on-premises networking, only **2 IP addresses** are reserved per subnet (Network Address `.0` and Broadcast Address `.255`).  
> **In AWS, exactly 5 IP addresses are ALWAYS reserved** in every CIDR block!  
> For a `/24` subnet ($2^8 = 256$ total addresses), **only 251 IP addresses are usable**.

### Formula:
$$\text{Usable IPs} = 2^{(32 - \text{Prefix})} - 5$$

For `10.0.1.0/24`:
$$2^{(32 - 24)} - 5 = 256 - 5 = 251 \text{ usable IPs}$$

### Tabular Breakdown of the 5 Reserved IPs:

| IP Address | AWS Reservation Name | Everyday Township Metaphor & Real Function |
| :--- | :--- | :--- |
| **`10.0.1.0`** | **Network Address** | **The Township Boundary Marker:** Identifies the network block itself. Cannot be assigned to any EC2 instance or ENI. |
| **`10.0.1.1`** | **VPC Router** | **The Local Security Office & Default Gateway:** The internal router that handles traffic routing between subnets and out of the VPC. |
| **`10.0.1.2`** | **Amazon-Provided DNS (Route 53 Resolver)** | **The Central Directory Desk:** Internal DNS server that resolves internal and public domain names. Always calculated as `VPC CIDR Base + 2`. |
| **`10.0.1.3`** | **Future Use** | **Reserved Plot:** Reserved by AWS for future internal networking capabilities. |
| **`10.0.1.255`** | **Network Broadcast** | **Township Megaphone:** Reserved broadcast address. *Note: AWS VPC networking does not support IP broadcast or multicast, but the address remains reserved.* |

---

## 🚪 3. Traffic Routing: Internet Gateway (IGW) vs NAT Gateway

```
[ Public Internet: 0.0.0.0/0 ]
            │ ▲
            │ │  (Two-Way Direct Traffic)
            ▼ │
    [ Internet Gateway (IGW) ]
            │ ▲
            ▼ │
┌─────────────────────────────────────────────────────────────┐
│ PUBLIC SUBNET (10.0.1.0/24)                                 │
│  • Route Table: 0.0.0.0/0 ➔ igw-xxxx                        │
│  • Hosts: Application Load Balancer & NAT Gateway (EIP)     │
└─────────────────────────────────────────────────────────────┘
            │ ▲
            │ │  (Outbound ONLY via NAT)
            ▼ │
┌─────────────────────────────────────────────────────────────┐
│ PRIVATE SUBNET (10.0.2.0/24)                                │
│  • Route Table: 0.0.0.0/0 ➔ nat-xxxx                        │
│  • Hosts: EC2 App Servers & RDS Databases                   │
│  • Inbound Internet Access: 100% BLOCKED                    │
└─────────────────────────────────────────────────────────────┘
```

### 1. Internet Gateway (IGW)
- **What is it?** A horizontally scaled, redundant, highly available software component attached to the VPC.
- **Why use it?** Enables instances with public IPs in public subnets to connect directly to the internet, and internet clients to access public web applications.
- **Requirements:**
  1. Must be created and **attached to the VPC**.
  2. Public Subnet's Route Table must contain: `Destination: 0.0.0.0/0` ➔ `Target: igw-xxxx`.
  3. The EC2 instance must have a **Public IPv4 address** or an **Elastic IP**.

### 2. NAT Gateway (Network Address Translation)
- **What is it?** A managed AWS service that translates private IP addresses to a single public IP for outbound internet access.
- **Why use it?** Enables backend EC2 servers in private subnets to download software patches (`apt update`, `yum update`, `pip install`) or call external APIs (Stripe, Twilio) **without exposing them to incoming internet attacks**.
- **Crucial Architecture Rules:**
  1. **Placement:** NAT Gateway **MUST be created inside a Public Subnet** (because it needs direct internet access).
  2. **Elastic IP:** NAT Gateway **MUST be allocated an Elastic IP (EIP)**.
  3. **Routing:** The Route Table of the **Private Subnet** must contain: `Destination: 0.0.0.0/0` ➔ `Target: nat-xxxx`.

---

## 🛡️ 4. Firewalls: Security Groups (Stateful) vs Network ACLs (Stateless)

```
Incoming Packet
       │
       ▼
 [ Network ACL ]  <─── Subnet Level (Stateless Checkpoint)
       │
       ▼
 [ Security Group ]  <─── Instance / ENI Level (Stateful Bodyguard)
       │
       ▼
  [ EC2 Instance ]
```

| Feature / Metric | Security Group (Stateful Personal Guard) | Network ACL (Stateless Subnet Tollbooth) |
| :--- | :--- | :--- |
| **Operating Level** | Instance / ENI (Elastic Network Interface) | Subnet boundary (protects all instances in subnet) |
| **State Tracking** | **Stateful:** If traffic is permitted inbound, the return traffic is automatically allowed regardless of outbound rules! | **Stateless:** Return traffic must be explicitly allowed in the outbound rules (ephemeral ports 1024–65535). |
| **Rule Types** | **Allow rules ONLY.** Everything else is denied by default (implicit deny). | **Allow AND Deny rules** are both supported. |
| **Evaluation Order** | All rules are evaluated simultaneously before granting access. | Rules are evaluated in strict **ascending numerical order** (e.g. 100, 200, *). The first rule that matches is applied! |
| **Default Configuration** | Default SG: Allows all outbound, denies all inbound. Custom SG: Denies all inbound until rules added. | Default NACL: Allows all inbound and outbound. Custom NACL: Denies all inbound and outbound until rules added. |
| **Primary Use Case** | Primary day-to-day security: Opening port 80/443 for web, port 22 for SSH, port 5432 for Postgres. | Subnet-wide security policies: Blacklisting specific malicious IP addresses or blocking compromised CIDR ranges. |

---

## 📖 5. How the Amazon VPC DNS Resolver Works

![DNS Resolution Flow](file:///e:/trainer/task/module_03_aws_core/notes/diagrams/02_dns_resolver_flow.png)

Students often struggle to understand how an EC2 instance resolves domain names inside a private network. Here is the step-by-step breakdown:

### A. The Reserved IP Address (`VPC Base + 2`)
Every AWS VPC provides a managed internal DNS service known as **AmazonProvidedDNS** (or the **Route 53 Resolver**).
The resolver IP is **always located at the 2nd usable IP of the VPC CIDR base**:
- For VPC `10.0.0.0/16` $\rightarrow$ Resolver IP is **`10.0.0.2`**
- For VPC `172.16.0.0/16` $\rightarrow$ Resolver IP is **`172.16.0.2`**
- For VPC `192.168.0.0/16` $\rightarrow$ Resolver IP is **`192.168.0.2`**

### B. Step-by-Step Resolution Flow:
1. **The Application Query:** An application running on an EC2 instance (e.g., `10.0.2.15`) makes a DNS query for `db.internal` (an internal database) or `api.github.com` (a public API).
2. **Local Resolver Forwarding:** The operating system's DNS resolver configuration (`/etc/resolv.conf` on Linux) points to nameserver `10.0.0.2`.
3. **Route 53 Private Hosted Zone Check:**
   - The Route 53 Resolver first checks if the requested domain exists in a **Private Hosted Zone** associated with this VPC.
   - If found (e.g. `db.internal ➔ 10.0.3.50`), it immediately returns the private IP address within microseconds.
4. **Recursive Internet Resolution:**
   - If the domain is not in a private zone, the resolver acts as a recursive DNS server.
   - It sends queries out across the Internet Gateway or NAT Gateway to external authoritative root nameservers and returns the public IP (e.g. `140.82.121.6`).
5. **Two Mandatory VPC DNS Settings:**
   - `enableDnsSupport`: When set to `true`, queries to `10.0.0.2` will succeed.
   - `enableDnsHostnames`: When set to `true`, EC2 instances with public IPs receive a corresponding public DNS hostname (e.g. `ec2-54-xx-xx-xx.compute-1.amazonaws.com`).

---

## 🌐 6. Public DNS vs Private DNS in Route 53

Students frequently ask: *"Sir, what is the exact difference between a Public Hosted Zone and a Private Hosted Zone in Route 53?"*

| Metric | Public Hosted Zone (Route 53) | Private Hosted Zone (Route 53) |
| :--- | :--- | :--- |
| **Everyday Metaphor** | **The Global Public Yellow Pages Telephone Directory** | **The Company's Internal Confidential Intercom Directory** |
| **Accessibility** | Accessible by **anyone on the global internet** worldwide. | Accessible **ONLY by resources inside the VPCs** linked to the zone. |
| **Resolution Target** | Public domain names (e.g. `mycompany.com`, `api.mycompany.com`). | Internal private names (e.g. `db.internal`, `auth.vpc.local`). |
| **Resolved IP Type** | Resolves to **Public IPv4/IPv6 addresses**, CloudFront CDN distributions, or ALBs. | Resolves to **Private RFC 1918 IPs** (e.g. `10.0.2.50`, `10.0.3.100`). |
| **Visibility / Privacy** | DNS query results are public and visible to hackers running `dig` or `nslookup`. | **100% Invisible to the outside internet.** External queries return `NXDOMAIN` (non-existent domain). |
| **Use Case** | Serving public end-users visiting your website or mobile application. | Internal microservice-to-microservice communication and database connections without hardcoding private IPs. |

---

## 🔒 7. How HTTPS Works Under the Hood (The Titanium Security Briefcase)

### The Analogy:
- **Plain HTTP (Port 80):** Like sending a postcard through the mail. Every postal worker, delivery boy, and bystander on coffee shop Wi-Fi can read your passwords, credit cards, and session cookies in clear text!
- **HTTPS (Port 443):** Like locking your letter inside a **tamper-proof titanium security briefcase** with a dual-key cryptographic lock. Even if an attacker intercepts the briefcase, all they see is scrambled gibberish!

### The SSL/TLS Handshake Step-by-Step:

```
[ Browser / Client ]                                   [ AWS ALB / Web Server ]
         │                                                        │
         │ 1. Client Hello (Supported TLS versions & Ciphers)    │
         ├───────────────────────────────────────────────────────►│
         │                                                        │
         │ 2. Server Hello + TLS Certificate (Contains Public Key)│
         │◄───────────────────────────────────────────────────────┤
         │                                                        │
         │ 3. Browser verifies Certificate with Trusted Root CA  │
         │    (Locks briefcase using Server's Public Key)         │
         │                                                        │
         │ 4. Client Key Exchange: Sends Encrypted Session Key    │
         ├───────────────────────────────────────────────────────►│
         │                                                        │ 5. Server decrypts Session Key
         │                                                        │    using its secret Private Key!
         │                                                        │
         │◄══════════════════════════════════════════════════════►│
         │ 6. Fast Symmetric AES Encryption Established!         │
         │    All HTTP payloads, headers & cookies are encrypted  │
```

1. **Step 1: Client Hello:** The client browser contacts the server on **Port 443** and shares supported cryptographic standards (e.g., TLS 1.3, AES-GCM).
2. **Step 2: Server Hello & Certificate:** The server responds with its chosen cipher and its **Digital Certificate** (issued by a trusted Certificate Authority like AWS Certificate Manager or Let's Encrypt). This certificate contains the server's **Public Key**.
3. **Step 3: Verification:** The browser verifies the CA digital signature against its built-in operating system trust store. If valid, the padlock icon appears green.
4. **Step 4: Session Key Generation & Exchange:** The browser generates a unique, temporary **Symmetric Session Key** (for fast data encryption). It encrypts this key using the server's **Public Key** and transmits it.
5. **Step 5: Server Decryption:** Only the server possesses the corresponding secret **Private Key**. It decrypts the message and extracts the session key.
6. **Step 6: Secure Channel:** Now both sides share the secret session key. All further communication is encrypted using ultra-fast symmetric encryption.

### TLS Termination at the Application Load Balancer (ALB):
In AWS production architectures, we do **TLS Termination** at the ALB:
- **AWS Certificate Manager (ACM):** Provisions free, auto-renewing SSL/TLS certificates.
- **ALB Handles Encryption:** The ALB terminates HTTPS on Port 443, decrypts the traffic, inspects HTTP URL path routing rules, and forwards plain HTTP (Port 80) across the private VPC subnets to the backend EC2 fleet.
- **Benefit:** Removes heavy cryptographic encryption/decryption overhead from backend EC2 servers, allowing 100% of their CPU to serve business application code!

---

## 🏷️ 8. IP Addressing Comparison: Private IP vs Public IP vs Elastic IP

| Property | Private IPv4 | Public IPv4 | Elastic IP (EIP) |
| :--- | :--- | :--- | :--- |
| **Analogy** | **Internal Intercom Extension** (Room 204) | **Temporary Rental Car Day Pass** | **Permanent Registered VIP License Plate** |
| **Scope** | Internal within VPC only | Publicly accessible across the internet | Publicly accessible across the internet |
| **Stop / Start Behavior** | **RETAINED:** Remains unchanged when instance stops and starts. | **LOST & CHANGED:** The public IP is returned to the AWS pool upon stopping. A new random IP is assigned on start! | **PERMANENT:** Remains attached to the instance across stops and starts until manually disassociated. |
| **DNS Implication** | Perfect for internal microservice communication via Route 53 Private Zones. | Dangerous for direct DNS records because the IP changes if the instance is rebooted/stopped. | Ideal for public web servers or NAT Gateways requiring a fixed static public IP. |
| **Pricing** | **100% Free** (No charge) | Standard IPv4 public address charges apply. | Free while attached to a running instance; **hourly idle charge if unattached**! |

---

## ⚖️ 9. Elastic Load Balancing: ALB vs NLB

| Metric | Application Load Balancer (ALB) | Network Load Balancer (NLB) |
| :--- | :--- | :--- |
| **OSI Layer** | **Layer 7 (Application Layer)** | **Layer 4 (Transport Layer)** |
| **Protocols** | HTTP, HTTPS, gRPC, WebSockets | TCP, UDP, TLS |
| **Analogy** | **Smart Head Waiter / Concierge:** Reads the food order menu (URL path `/api` vs `/static`), checks tickets (cookies/headers), and seats guests. | **High-Speed Bullet Train Baggage Handler:** Ultra-fast, does not read passenger tickets, moves raw cargo at light speed. |
| **Routing Capability** | Path-based (`/orders`), Host-based (`api.example.com`), Query parameters, HTTP headers. | IP address, TCP/UDP port routing only. |
| **Throughput & Speed** | High throughput with ~10ms latency. | **Ultra-low sub-millisecond latency; millions of requests per second.** |
| **IP Address Support** | Dynamic IP addresses (Must access via DNS name). | **Static IP addresses** (Provides 1 fixed Elastic IP per AZ). |

---

## 🏢 10. Production 3-Tier Enterprise Web Architecture Pattern

```
                  [ Public Internet Users ]
                             │
                             ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ PUBLIC SUBNET (AZ-a & AZ-b)                                 │
 │  • Internet-Facing Application Load Balancer (ALB)          │
 │  • NAT Gateway (AZ-a) with Elastic IP                       │
 │  • Route: 0.0.0.0/0 ➔ Internet Gateway                      │
 └───────────────────────────┬─────────────────────────────────┘
                             │  Forward Port 80/443
                             ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ PRIVATE APPLICATION SUBNET (AZ-a & AZ-b)                    │
 │  • EC2 Auto Scaling Group (App Servers)                     │
 │  • Security Group: Inbound Port 80/8080 from ALB SG ONLY    │
 │  • Route: 0.0.0.0/0 ➔ NAT Gateway (Outbound updates only)   │
 └───────────────────────────┬─────────────────────────────────┘
                             │  Forward Port 5432
                             ▼
 ┌─────────────────────────────────────────────────────────────┐
 │ ISOLATED DATABASE SUBNET (AZ-a & AZ-b)                      │
 │  • Amazon RDS Multi-AZ PostgreSQL Database                  │
 │  • Security Group: Inbound Port 5432 from App EC2 SG ONLY   │
 │  • Route: Local ONLY (10.0.0.0/16) - NO Internet Access     │
 └─────────────────────────────────────────────────────────────┘
```

---
*Created by **Sundeep Hiremat** for TASK Nalgonda Center · Cloud Software Developer Mastery Program (2026).*
