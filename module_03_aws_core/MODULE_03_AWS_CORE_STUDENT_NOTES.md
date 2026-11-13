# Module 03: AWS Core Services & Infrastructure Master Handbook
> **TASK (Telangana Academy for Skill and Knowledge)**  
> **Course:** Cloud Software Developer (AWS EC2-Centric / DVA-C02 Alignment)  
> **Center:** Nalgonda Training Center  
> **Trainer:** Sundeep Hiremat  
> **Delivery Plan:** 3-Day Technical Deep Dive  

---

## 📚 Module Overview & Resource Index

Welcome to **Module 03**! This module is designed as an end-to-end 3-day deep dive covering foundational cloud infrastructure, compute engines, storage triads, databases, networking, edge security, containers, and infrastructure as code. Every topic is grounded in **The Grand Vehicle Metaphor** and backed by our explicit **Service Requirements & Decision Matrix**.

### Quick Links to Created Artifacts:
- 📊 **PowerPoint Presentation (28 Widescreen Slides with High-Contrast Code Colors):**  
  [Module_03_AWS_Core_Services_Masterclass_v2.pptx](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/presentation/Module_03_AWS_Core_Services_Masterclass_v2.pptx)
- 📄 **Module 03 Theory & Architectural PDF Guide:**  
  [Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/notes/Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf)
- 📄 **Consolidated Hands-on Lab Manual PDF:**  
  [Module_03_Hands_On_Lab_Manual.pdf](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/lab_guides/Module_03_Hands_On_Lab_Manual.pdf)
- 🚀 **Mini Project 1: Cloud Portfolio on Ubuntu 24.04 + Nginx + GitHub:**  
  [PROJECT_01_CLOUD_PORTFOLIO_GUIDE.md](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/mini_projects/project_01_cloud_portfolio/PROJECT_01_CLOUD_PORTFOLIO_GUIDE.md)  
  *(Printable PDF: [Project_01_Cloud_Portfolio_Manual.pdf](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/mini_projects/project_01_cloud_portfolio/Project_01_Cloud_Portfolio_Manual.pdf))*
- 🛠️ **Individual Lab Guides:**
  - Lab 1 (EC2 & Lifecycle): [01_ec2_launch_and_lifecycle_lab.md](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/lab_guides/01_ec2_launch_and_lifecycle_lab.md)
  - Lab 2 (Storage Triad - EBS, EFS, S3): [02_storage_ebs_efs_s3_lab.md](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/lab_guides/02_storage_ebs_efs_s3_lab.md)
  - Lab 3 (VPC Networking & Security): [03_vpc_networking_and_security_lab.md](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/lab_guides/03_vpc_networking_and_security_lab.md)

---

## 🚗 1. The Grand Vehicle Metaphor: The Cloud as an Automobile Fleet

| AWS Service | Automobile Component | Everyday Metaphor & Real-World Function |
|---|---|---|
| **Amazon EC2** *(Compute)* | **The Car Engine & Chassis** | You rent an engine on-demand instead of buying a vehicle factory. Choose horsepower (Instance Type: `t3.micro`), body blueprint (AMI: *Amazon Linux* or *Ubuntu*), and ignition key (Key Pair `.pem`). |
| **Amazon EBS** *(Block Storage)* | **The Car's Personal Trunk** | Hard drive bolted directly to 1 car chassis in a parking garage (AZ). High speed. When the car turns off, your luggage inside stays safe. |
| **Amazon EFS** *(File Storage)* | **The Shared Fleet Roof Cargo** | Shared roof rack that a whole fleet of 100+ cars across multiple garages can access at the same time using standard network ropes (NFS protocol). |
| **Amazon S3** *(Object Storage)* | **The Global Container Shipping Depot** | Unlimited worldwide warehouse outside the vehicle. Store cargo boxes (Objects) in shipping bays (Buckets). Reachable from anywhere via the national highway (HTTPS URL). 99.999999999% durable. |
| **Amazon VPC** *(Networking)* | **The Gated Industrial Campus** | Your private corporate compound with secure perimeter walls. Only authorized vehicles enter. |
| **Public Subnet** | **Front Showroom Lane** | Connected directly to the national highway via the **Internet Gateway (IGW)**. |
| **Private Subnet** | **Underground VIP Vault** | Hidden back garage with no direct highway access; only connects outbound via a **NAT Gateway**. |
| **Security Group** | **Car's Personal Bodyguard** | **Stateful:** If a visitor is allowed inside the car, they are automatically allowed to step back out. |
| **Network ACL (NACL)** | **District Highway Toll Barrier** | **Stateless:** Checks license plates on entry AND explicitly checks license plates on exit. |

---

## 🎯 2. Service Requirements & Decision Matrix: What is Required & When to Use Which Service

To succeed as a professional cloud engineer, you must know not just *what* a service does, but **what is required to configure it** and **the exact decision triggers** for when to choose it over alternatives:

### 1. Compute & Containers

#### **Amazon EC2 (Elastic Compute Cloud)**
- **What is Required to Launch:**
  1. **AMI (Amazon Machine Image):** Base OS template (e.g. Amazon Linux 2023, Ubuntu 24.04 LTS).
  2. **Instance Type:** CPU & RAM sizing (e.g. `t2.micro` or `t3.micro` for Free Tier).
  3. **VPC Subnet:** Placement in an Availability Zone.
  4. **Key Pair (`.pem` / `.ppk`):** Cryptographic SSH key for administrative login.
  5. **Security Group:** Inbound firewall rule (e.g. Port 22 SSH from My IP, Port 80 HTTP from anywhere).
  6. **Root EBS Volume:** Operating system disk (8–30 GB gp3).
- **When to Use It:**
  - When you need full administrative control (root access) over the operating system.
  - When running legacy monolithic applications, custom software daemons, or specialized network configurations.
- **When NOT to Use It:**
  - Event-driven short tasks (use **AWS Lambda**).
  - Microservices where you don't want to manage OS patches (use **AWS Fargate**).

#### **Amazon ECS (Elastic Container Service) with AWS Fargate**
- **What is Required:**
  1. **Docker Container Image:** Packaged and pushed to Amazon ECR.
  2. **Task Definition:** CPU, memory, container port mappings, and environment variables.
  3. **VPC Subnets & Security Group:** Network placement for the task's Elastic Network Interface (ENI).
  4. **IAM Task Execution Role:** Grants ECS permission to pull from ECR and send logs to CloudWatch.
- **When to Use It:**
  - Deploying Docker containers that run continuously (web servers, background worker queues) without managing underlying EC2 virtual machines.
- **When NOT to Use It:**
  - Bursty, sporadic tasks that execute for less than 15 minutes (use **AWS Lambda**).

#### **AWS Lambda vs Amazon ECS Showdown**
| Metric | Amazon ECS (Fargate) | AWS Lambda |
|---|---|---|
| **Max Execution Duration** | **Unlimited / Continuous (24/7/365)** | **Strict 15-Minute Timeout** |
| **Execution Trigger** | Continuous service or scheduled batch | Event-driven (S3 upload, API Gateway HTTP, DynamoDB stream) |
| **Cost Model** | Pay per second of allocated vCPU/RAM | Pay per millisecond of execution; **$0 when idle (scale-to-zero)** |
| **Best For** | Full web apps, real-time APIs, worker daemons | Image processing on upload, webhooks, lightweight cron ETL |

---

### 2. Storage Triad: Block vs File vs Object

#### **Amazon EBS (Elastic Block Store)**
- **What is Required:** Must reside in the **exact same Availability Zone** as the target EC2 instance. Inside Linux, it must be formatted (`sudo mkfs -t ext4 /dev/xvdf`) and mounted (`sudo mount /dev/xvdf /mnt/data`).
- **When to Use:** OS boot drives, local databases requiring ultra-low latency (<1ms) block I/O.
- **When NOT to Use:** Shared storage across multiple instances (use **EFS**) or large media files (use **S3**).

#### **Amazon EFS (Elastic File System)**
- **What is Required:** Target VPC, Mount Targets in each AZ, Security Group allowing **Inbound NFS (Port 2049)** from EC2 instances.
- **When to Use:** Multiple EC2 instances (100+) need concurrent read/write access to a shared directory (e.g. WordPress uploads, CMS media, shared home directories).
- **When NOT to Use:** Relational database data files (use **EBS**) or static website hosting (use **S3**).

#### **Amazon S3 (Simple Storage Service)**
- **What is Required:** Globally unique bucket name (3–63 chars, lowercase, no underscores), AWS Region, Block Public Access enabled by default.
- **When to Use:** Unlimited media assets (images, videos), document storage, data lake backups, static web hosting. 99.999999999% durability.
- **When NOT to Use:** Block-level file modifications (S3 is object-based; updating a single byte requires replacing the entire object).

---

### 3. Databases: Relational vs NoSQL vs In-Memory

```
+-------------------+-------------------------------+-----------------------------------+-----------------------------------+
| Database Service  | Engine / Model                | What is Required                  | When to Choose It                 |
+-------------------+-------------------------------+-----------------------------------+-----------------------------------+
| **Amazon RDS**    | Relational SQL (Postgres/MySQL)| DB Subnet Group (2+ AZs), SG Port | Transactional ERP, complex JOINs, |
|                   |                               | (5432/3306), Admin credentials    | automated Multi-AZ failover.      |
+-------------------+-------------------------------+-----------------------------------+-----------------------------------+
| **Amazon Aurora** | Cloud-native SQL (Postgres/MySQL)| DB Subnet Group, Cluster endpoint| High-throughput enterprise SQL,   |
|                   |                               |                                   | 5x faster, Serverless v2 scaling. |
+-------------------+-------------------------------+-----------------------------------+-----------------------------------+
| **DynamoDB**      | Serverless NoSQL (Key-Value)  | Table name, Partition Key (PK),   | Single-digit ms latency at scale, |
|                   |                               | Capacity mode (On-Demand)         | shopping carts, gaming, IoT.      |
+-------------------+-------------------------------+-----------------------------------+-----------------------------------+
| **ElastiCache**   | In-Memory Cache (Redis)       | Cache Subnet Group, SG Port 6379  | Sub-millisecond read offload,     |
|                   |                               |                                   | user session state, leaderboards. |
+-------------------+-------------------------------+-----------------------------------+-----------------------------------+
```

---

### 4. VPC Networking, Edge Delivery & Security

#### **Virtual Private Cloud (VPC)**
- **What is Required:** IPv4 CIDR Block (Standard: `10.0.0.0/16` = 65,536 private IPs).
- **When to Use:** Every enterprise deployment to create a private, isolated network perimeter.

#### **Internet Gateway (IGW) vs NAT Gateway**
- **Internet Gateway (IGW):**
  - *What is Required:* Must be attached to VPC; Route Table must point `0.0.0.0/0` ➔ `igw-xxxx`.
  - *When to Use:* Front-facing web servers, Application Load Balancers, or Bastion hosts that need **two-way direct communication** with public internet visitors.
- **NAT Gateway:**
  - *What is Required:* Must be placed in a **Public Subnet** with an **Elastic IP (EIP)** allocated; Private Route Table points `0.0.0.0/0` ➔ `nat-xxxx`.
  - *When to Use:* Backend databases and private app servers that need **outbound-only access** (to download Linux OS patches, Python packages) while remaining **completely hidden and unreachable** from incoming internet attacks.

#### **Security Groups (Stateful) vs Network ACLs (Stateless)**
- **Security Groups (Stateful Personal Guard):** Operates at the network interface (instance) level. Allow rules only. Tracks connection state—if inbound is allowed, return traffic is automatically allowed. **Use as your primary application firewall.**
- **Network ACLs (Stateless Toll Barrier):** Operates at the subnet boundary. Supports Allow and Deny rules evaluated in strict numerical order. Must explicitly permit both inbound and outbound traffic. **Use for subnet-level blacklisting (e.g. blocking specific malicious IP ranges).**

#### **Application Load Balancer (ALB) vs CloudFront CDN**
- **ALB (Layer 7):** Distributes incoming traffic across multiple EC2/ECS targets within a single region based on HTTP URL path routing (`/api` vs `/app`).
- **CloudFront CDN:** Caches static and dynamic content globally across 600+ Edge Locations closer to users, lowering latency worldwide and absorbing DDoS attacks.

---

### 5. Infrastructure as Code (IaC) with AWS CloudFormation

- **What is Required:** Declarative YAML or JSON template containing at minimum a `Resources` block.
- **Why IaC beats "ClickOps":**
  1. **Speed & Consistency:** Reproduce complex multi-tier environments across regions in 5 minutes.
  2. **Auditability:** Stored in Git and reviewed via Pull Requests.
  3. **Atomic Deletion:** Deleting a stack deletes all child resources cleanly with zero lingering orphan costs.
- **CloudFormation Drift Detection:**
  - *What is Drift?* Occurs when an engineer bypasses the template and manually edits a resource in the AWS Console.
  - *How to Detect:* In AWS Console, select Stack ➔ **Stack actions ➔ Detect drift**.
  - *How to Remediate:* Revert manual console changes to match the template, OR update the YAML template to adopt the change via a **Change Set**.

---

## 🛡️ 3. Student Zero-Dollar Sunset Checklist

Every student must execute this 5-step checklist before leaving the college lab:
1. **Stop or Terminate** all practice EC2 instances.
2. Go to **EBS Volumes** and delete any unattached volumes in `available` state.
3. Delete custom **CloudFormation stacks** to cleanly terminate all child resources.
4. Release any allocated **Elastic IPs (EIPs)**.
5. Check the **AWS Billing Dashboard** to confirm $0.00 active charges.
