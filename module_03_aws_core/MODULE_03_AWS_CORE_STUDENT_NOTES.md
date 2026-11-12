# Module 03: AWS Core Services & Infrastructure Master Handbook
> **TASK (Telangana Academy for Skill and Knowledge)**  
> **Course:** Cloud Software Developer (AWS EC2-Centric / DVA-C02 Alignment)  
> **Center:** Nalgonda Training Center  
> **Trainer:** Sundeep Hiremath  
> **Format:** Classroom Handbook & Technical Documentation  

---

## 📚 Module Overview & Resource Index

Welcome to **Module 03**! This module transitions from core programming into foundational cloud architecture. Every concept here is explained through our intuitive **Grand Vehicle & Fleet Metaphor** to help you visualize, master, and ace technical interviews.

### Quick Links to Created Artifacts:
- 📊 **PowerPoint Masterclass:** [Module_03_AWS_Core_Services_Masterclass.pptx](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/presentation/Module_03_AWS_Core_Services_Masterclass.pptx)
- 📄 **Printable PDF Guide:** [Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/notes/Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf)
- 📄 **Backup PDF in Notes folder:** [Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/notes/Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf)
- 🛠️ **Hands-on Lab 1 (EC2 & Lifecycle):** [01_ec2_launch_and_lifecycle_lab.md](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/lab_guides/01_ec2_launch_and_lifecycle_lab.md)
- 🛠️ **Hands-on Lab 2 (Storage Triad - EBS, EFS, S3):** [02_storage_ebs_efs_s3_lab.md](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/lab_guides/02_storage_ebs_efs_s3_lab.md)
- 🛠️ **Hands-on Lab 3 (VPC Networking & Security):** [03_vpc_networking_and_security_lab.md](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/lab_guides/03_vpc_networking_and_security_lab.md)

---

## 🚗 1. The Grand Vehicle Metaphor: The Cloud as an Automobile Fleet

| AWS Service | Automobile Component | Everyday Metaphor & Real-World Function |
|---|---|---|
| **Amazon EC2** *(Elastic Compute Cloud)* | **The Car Engine & Chassis** | Instead of buying a vehicle factory, you rent an engine on-demand. Choose horsepower (Instance Type: `t3.micro`), body blueprint (AMI: *Amazon Linux* or *Ubuntu*), and ignition key (Key Pair `.pem`). |
| **Amazon EBS** *(Elastic Block Store)* | **The Car's Personal Trunk** | Hard drive bolted directly to one car chassis in a parking garage (Availability Zone). High speed. When the car turns off, your luggage inside stays safe. |
| **Amazon EFS** *(Elastic File System)* | **The Shared Fleet Roof Cargo** | A shared roof rack that a whole fleet of 100+ cars across multiple garages can access at the same time using standard network ropes (NFS protocol). |
| **Amazon S3** *(Simple Storage Service)* | **The Global Container Shipping Depot** | Not inside any car! An unlimited worldwide warehouse. You place cargo boxes (Objects) into large shipping bays (Buckets). Reachable from anywhere via the national highway (Internet HTTPS URL). 99.999999999% durable. |
| **Amazon VPC** *(Virtual Private Cloud)* | **The Gated Industrial Campus** | Your private corporate compound with secure perimeter walls. Only authorized vehicles enter. |
| **Subnets** | **Zoned Driving Lanes** | Public lane (front showroom connected to national highway) vs. Private lane (underground VIP vault). |
| **Internet Gateway (IGW)** | **The Main Highway Gate** | Two-way highway exit permitting cars to travel out to the world and public visitors to enter. |
| **NAT Gateway** | **The One-Way Security Escort** | Allows private secret cars in the back vault to fetch fuel/software from the internet, but strictly prevents outside internet cars from driving in. |
| **Security Group** | **Car's Personal Bodyguard** | Stateful guard at each car door. If someone is authorized to get in, they can step out freely. |
| **Network ACL (NACL)** | **District Highway Toll Booth** | Stateless barrier across the road. Inspects license plates on entrance AND on exit. |

---

## ⚡ 2. Amazon EC2 Core Compute

### 2.1 The 5 Pillars of an EC2 Instance
1. **AMI (Amazon Machine Image):** Pre-packaged OS template. (e.g. Amazon Linux 2023, Ubuntu 24.04).
2. **Instance Type:** Defines vCPU and RAM. E.g. `t3.micro` (1 vCPU, 1 GiB RAM).
3. **Key Pair (`.pem` / `.ppk`):** Asymmetric cryptography used to authenticate SSH sessions. AWS retains the public key; you download the private key.
4. **Security Group:** Virtual firewall attached to the network interface. Default: Inbound blocked, Outbound open.
5. **Root EBS Volume:** Primary OS disk where the Linux root `/` filesystem is mounted.

### 2.2 EC2 Lifecycle & Billing State Machine

```
   [ Launch ]
       |
       v
  [ Pending ]  ---> Provisioning virtual hardware
       |
       v
  [ Running ]  <----------------------------+
       |                                    |
   (Stop call)                         (Start call)
       v                                    |
  [ Stopping ] ---> Flushing OS cache       |
       |                                    |
       v                                    |
  [ Stopped ]  -----------------------------+
   (Compute = $0/hr, EBS storage billed, Public IP released)
       |
  (Terminate call)
       v
 [ Shutting-Down ]
       |
       v
 [ Terminated ] (Permanently destroyed, billing ceases completely)
```

---

## 📦 3. Storage Triad: EBS vs EFS vs S3 Shootout

```
+-------------------+-------------------------------+-----------------------------------+-----------------------------------+
| Feature           | Amazon EBS (Block)            | Amazon EFS (File)                 | Amazon S3 (Object)                |
+-------------------+-------------------------------+-----------------------------------+-----------------------------------+
| Metaphor          | Built-in Car Trunk            | Shared Fleet Roof Cargo           | Global Shipping Container Depot   |
| Access Type       | Direct disk blocks (NVMe/SCSI)| Network File System (NFSv4)       | REST API (HTTP/HTTPS GET/PUT)     |
| Scope             | Bound to 1 Availability Zone  | Regional (Multi-AZ)               | Global URL endpoints              |
| Concurrency       | 1 EC2 Instance only           | 1,000s of EC2s simultaneously     | Unlimited HTTP concurrent users   |
| Primary Use Case  | OS boot drives, DB storage    | Shared WordPress uploads, CMS     | Images, videos, backups, datasets |
| Durability        | 99.8% - 99.999%               | 99.999999999% (11 9's)            | 99.999999999% (11 9's)            |
+-------------------+-------------------------------+-----------------------------------+-----------------------------------+
```

---

## 🌐 4. Amazon VPC Networking & Defense-in-Depth

### Why the Route Table Decides Everything:
- A Subnet is **NEVER** intrinsically "public" or "private" by itself.
- A Subnet is defined as **Public** if and only if its associated Route Table contains an entry pointing `0.0.0.0/0` to an **Internet Gateway (`igw-xxxx`)**.
- If a Subnet's route table does **not** point to an IGW, it is **Private**.

### Security Groups vs Network ACLs:
- **Security Groups (Stateful):** If inbound Port 80 is allowed, response packets leaving the instance are automatically allowed out, regardless of outbound rules.
- **Network ACLs (Stateless):** Operates at the subnet border. If you allow inbound traffic on Port 80, you **must explicitly allow ephemeral outbound return traffic (ports 1024–65535)**!

---

## 🛡️ 5. Zero-Dollar Student Hygiene (Daily Sunset Rule)

To protect your personal AWS Free Tier account from unexpected charges:
1. **Stop or Terminate** all practice EC2 instances at the end of each session.
2. Check the **EBS Volumes** tab in EC2 Console to ensure no orphan volumes are lingering in `available` state.
3. Release unused **Elastic IPs** immediately.
4. Keep S3 bucket sizes within the 5 GB free tier storage limit.
5. Set an **AWS Billing Alarm** at $0.01 to get notified via email of any non-free tier activity.
