# Lab 3: Amazon VPC Networking, Subnet Isolation & Defense-in-Depth
> **Program:** TASK Telangana · Cloud Software Developer  
> **Module 03:** AWS Core Services & Infrastructure  
> **Trainer:** Sundeep Hiremat | Nalgonda Training Center  
> **Analogy:** *The Gated Highway, Public Showrooms, VIP Vaults & Checkpoint Barriers*

---

## 🎯 Lab Objectives
By the end of this hands-on lab, every student will be able to:
1. Explain why **Virtual Private Cloud (VPC)** is the cornerstone of cloud security and isolation.
2. Calculate and configure IPv4 CIDR blocks (e.g. `10.0.0.0/16` and `/24` subnets).
3. Architect and build both a **Public Subnet** and a **Private Subnet** from scratch.
4. Provision and attach an **Internet Gateway (IGW)** and configure custom **Route Tables**.
5. Demystify why a subnet is public or private: **It is the Route Table, NOT the subnet itself, that decides!**
6. Compare and test **Security Groups (Stateful)** vs. **Network ACLs (Stateless)**.
7. Understand the classic enterprise **3-Tier Architecture pattern** (ALB ➔ EC2 ➔ Database).

---

## 🚗 The Highway & Gated Estate Metaphor

```
                                  [ THE PUBLIC INTERNET ]
                                             |
                                             v  (Public Traffic)
+-----------------------------------------------------------------------------------------+
| AMAZON VPC: 10.0.0.0/16 (Private Gated Business Park)                                   |
|                                                                                         |
|  [ Internet Gateway (IGW) ] <--- The Main 2-Way Gate to the National Highway             |
|             |                                                                           |
|             v                                                                           |
|  +-------------------------------------+       +-------------------------------------+  |
|  | PUBLIC SUBNET (10.0.1.0/24)        |       | PRIVATE SUBNET (10.0.2.0/24)        |  |
|  | The Front Showroom & Visitor Lane  |       | The VIP Underground Vault           |  |
|  | Route: 0.0.0.0/0 ---> IGW          |       | Route: 10.0.0.0/16 ---> Local only  |  |
|  |                                     |       | (NO direct route to the Internet!)  |  |
|  |   [ Load Balancers / Bastion ]      |       |                                     |  |
|  |                 |                   |       |   [ Secret Database / RDS ]         |  |
|  |                 +-------------------+------>|   [ Internal Microservices ]        |  |
|  +-------------------------------------+       +-------------------------------------+  |
|                                                                                         |
|  [ Security Group ] = Guard at car door (Stateful: lets visitors return automatically)  |
|  [ Network ACL ]    = Road toll barrier (Stateless: inspects both entry and exit)       |
+-----------------------------------------------------------------------------------------+
```

---

## 🛠️ Step-by-Step Hands-on Lab

### Step 1: Create a Custom VPC
1. In the AWS Management Console, search for **VPC** and open the VPC Dashboard.
2. Click the orange **Create VPC** button.
3. Select **VPC only** (to learn each foundational component manually rather than using auto-wizards).
4. **Name tag:** `task-nalgonda-vpc`
5. **IPv4 CIDR block:** Select *IPv4 CIDR manual input*.
6. **IPv4 CIDR:** Enter `10.0.0.0/16`  
   *(This allocates 65,536 private IP addresses ranging from 10.0.0.0 to 10.0.255.255).*
7. **Tenancy:** Leave as `Default`.
8. Click **Create VPC**.

---

### Step 2: Enable DNS Hostnames
1. Select your new `task-nalgonda-vpc` in the VPC list.
2. Click **Actions** ➔ **Edit VPC settings**.
3. Under *DNS settings*, check **Enable DNS hostnames**.
4. Click **Save changes**.

---

### Step 3: Create Public and Private Subnets

#### Subnet 1: Public Subnet (The Front Lane)
1. In the left navigation menu, click **Subnets**.
2. Click **Create subnet**.
3. **VPC ID:** Select `task-nalgonda-vpc`.
4. **Subnet name:** `task-public-subnet-1a`
5. **Availability Zone:** Select `ap-south-1a`.
6. **IPv4 subnet CIDR block:** Enter `10.0.1.0/24` (Provides 251 usable IP addresses; AWS reserves 5).
7. Click **Create subnet**.
8. Select `task-public-subnet-1a` ➔ **Actions** ➔ **Edit subnet settings** ➔ Check **Enable auto-assign public IPv4 address** ➔ **Save**.

#### Subnet 2: Private Subnet (The Vault)
1. Click **Create subnet** again.
2. **VPC ID:** Select `task-nalgonda-vpc`.
3. **Subnet name:** `task-private-subnet-1b`
4. **Availability Zone:** Select `ap-south-1b`.
5. **IPv4 subnet CIDR block:** Enter `10.0.2.0/24`.
6. Click **Create subnet**. *(Do NOT enable auto-assign public IP here!)*

---

### Step 4: Create and Attach Internet Gateway (IGW)
1. On the left navigation menu, click **Internet gateways**.
2. Click **Create internet gateway**.
3. **Name tag:** `task-igw`
4. Click **Create internet gateway**.
5. Once created, click **Actions** ➔ **Attach to VPC**.
6. Select `task-nalgonda-vpc` and click **Attach internet gateway**.

---

### Step 5: Configure Custom Route Tables

A subnet is **Public** only if its route table points `0.0.0.0/0` to an Internet Gateway!

1. On the left menu, click **Route tables**.
2. Click **Create route table**.
3. **Name:** `task-public-rt`
4. **VPC:** Select `task-nalgonda-vpc`.
5. Click **Create route table**.

#### Add Route to Internet Gateway:
1. With `task-public-rt` selected, click the **Routes** tab below.
2. Click **Edit routes** ➔ Click **Add route**.
3. **Destination:** Enter `0.0.0.0/0` (Represents all traffic outside your VPC).
4. **Target:** Select **Internet Gateway** ➔ Choose `task-igw`.
5. Click **Save changes**.

#### Associate with Public Subnet:
1. Click the **Subnet associations** tab.
2. Click **Edit subnet associations**.
3. Check `task-public-subnet-1a`.
4. Click **Save associations**.

> 💡 **Notice:** `task-private-subnet-1b` remains associated with the Main Route Table, which has NO route to the Internet Gateway. It is completely isolated from the internet!

---

### Step 6: Stateful vs Stateless Security Testing

#### 1. Security Groups (Stateful Personal Guard)
- When an EC2 instance in `task-public-subnet-1a` allows incoming Port 80 (HTTP), any response generated by the server is **automatically permitted out**, without adding an outbound rule!
- Security Groups track active TCP handshake connections.

#### 2. Network ACLs (Stateless Highway Gate)
- If you block Port 80 on inbound NACL, traffic is dropped at the subnet border before ever reaching the EC2 instance.
- Because NACLs are **stateless**, if you open inbound port 80, you **must also explicitly open ephemeral outbound ports (1024–65535)** for return traffic!

---

## 🏛️ Enterprise 3-Tier Architecture Pattern

In enterprise environments, systems are structured in three distinct tiers:

```
[ User Request ]
       |
       v
[ Tier 1: Public Subnet ]    ---> Application Load Balancer (ALB)
       |                          Security Group: Allow 80/443 from 0.0.0.0/0
       v
[ Tier 2: Private App Subnet ] --> EC2 Auto Scaling App Cluster
       |                          Security Group: Allow Port 8000 ONLY from ALB SG
       v
[ Tier 3: Isolated DB Subnet ] --> Amazon RDS Multi-AZ Database
                                  Security Group: Allow Port 5432/3306 ONLY from App SG
```

**Security Benefit:** Hackers on the internet cannot even attempt to attack your application servers or database, because they have NO public IP addresses and NO internet route!

---

## 🧹 Cleanup Instructions

When finishing the VPC lab:
1. Delete any EC2 instances launched inside the VPC.
2. Detach and delete the `task-igw` Internet Gateway.
3. Delete the `task-nalgonda-vpc` (AWS will automatically remove the subnets and route tables).

