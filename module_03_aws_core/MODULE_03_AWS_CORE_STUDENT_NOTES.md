# Module 03: AWS Core Services & Infrastructure Master Handbook
> **TASK (Telangana Academy for Skill and Knowledge)**  
> **Course:** Cloud Software Developer (AWS EC2-Centric / DVA-C02 Alignment)  
> **Center:** Nalgonda Training Center  
> **Trainer:** Sundeep Hiremath  
> **Delivery Plan:** 3-Day Technical Deep Dive  

---

## 📚 Module Overview & Resource Index

Welcome to **Module 03**! This module is designed as an end-to-end 3-day deep dive covering foundational cloud infrastructure, compute engines, storage triads, databases, networking, edge security, containers, and infrastructure as code. Every topic is explained using our intuitive **Grand Vehicle & Fleet Metaphor**.

### Quick Links to Created Artifacts:
- 📊 **PowerPoint Presentation (28 Widescreen Slides with Fixed High-Contrast Code Colors):**  
  [Module_03_AWS_Core_Services_Masterclass_v2.pptx](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/presentation/Module_03_AWS_Core_Services_Masterclass_v2.pptx)
- 📄 **Expanded 3-Day Printable PDF Guide:**  
  [Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/notes/Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf)
- 📄 **Backup PDF in Notes folder:**  
  [Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/notes/Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf)
- 🛠️ **Hands-on Lab 1 (EC2 & Lifecycle):** [01_ec2_launch_and_lifecycle_lab.md](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/lab_guides/01_ec2_launch_and_lifecycle_lab.md)
- 🛠️ **Hands-on Lab 2 (Storage Triad - EBS, EFS, S3):** [02_storage_ebs_efs_s3_lab.md](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/lab_guides/02_storage_ebs_efs_s3_lab.md)
- 🛠️ **Hands-on Lab 3 (VPC Networking & Security):** [03_vpc_networking_and_security_lab.md](file:///F:/Task(%20Telangana%20)/Nalgonda/Projects/task/module_03_aws_core/lab_guides/03_vpc_networking_and_security_lab.md)

---

## 📅 3-Day Delivery Architecture

```
   +-----------------------------------------------------------------------------------------+
   |                     MODULE 03: 3-DAY AWS CORE SERVICES ROADMAP                          |
   +-----------------------------------------------------------------------------------------+
   |  DAY 1: COMPUTE & STORAGE TRIAD                                                         |
   |  • Global Infrastructure: Regions vs Availability Zones vs Edge Locations               |
   |  • High Availability: What is Multi-AZ vs Multi-Region (Disaster Recovery)              |
   |  • Amazon EC2: AMI Chassis, Instance Types, Key Pairs (.pem), Security Groups           |
   |  • EC2 Automation: Bootstrapping with User Data shell scripts (IMDSv2)                   |
   |  • Custom AMIs (Golden Images) & EC2 Lifecycle Billing State Machine                    |
   |  • Storage Shootout: Block (EBS) vs File (EFS) vs Object (S3)                           |
   |  • Amazon S3 Security: Block Public Access (BPA) & HTTPS-only JSON Bucket Policies      |
   +-----------------------------------------------------------------------------------------+
   |  DAY 2: DATABASES, NETWORKING & EDGE ACCELERATION                                       |
   |  • Databases: Amazon RDS (Multi-AZ Standby vs Read Replicas) vs Amazon Aurora           |
   |  • NoSQL & In-Memory: Amazon DynamoDB (Single-digit ms) vs ElastiCache (Redis)          |
   |  • Amazon VPC: Gated Highway Architecture (CIDR 10.0.0.0/16, reserved IPs)              |
   |  • Subnets: Public (0.0.0.0/0 -> IGW) vs Private (Route -> NAT Gateway)                 |
   |  • Security: Stateful Security Groups (Bodyguard) vs Stateless NACLs (Toll Barrier)     |
   |  • Load Balancing & Edge: ALB (Layer 7) vs NLB (Layer 4) + CloudFront CDN + AWS WAF     |
   |  • Architecture Pattern: Enterprise 3-Tier Defense in Depth (ALB -> EC2 -> RDS)         |
   +-----------------------------------------------------------------------------------------+
   |  DAY 3: CONTAINERS, SERVERLESS & INFRASTRUCTURE AS CODE (IaC)                           |
   |  • Containers 101: Virtual Machines vs Docker Containers (Kernel Sharing)               |
   |  • Amazon ECR: Authenticate, tag, build, and push Docker images via AWS CLI             |
   |  • Amazon ECS: EC2 Launch Type vs AWS Fargate (Serverless Containers)                   |
   |  • Architecture Showdown: Amazon ECS Containers vs AWS Lambda Container Images          |
   |  • Infrastructure as Code: Why AWS CloudFormation beats manual console clicking        |
   |  • Template Anatomy: Parameters -> Resources -> Outputs & Intrinsic Functions           |
   |  • CloudFormation Drift Detection: Detecting & Remediating out-of-band console edits    |
   |  • Zero-Dollar Student Hygiene: Complete Lab Teardown & Billing Protection              |
   +-----------------------------------------------------------------------------------------+
```

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

## ⚡ 2. Global Infrastructure: Regions, AZs & Multi-AZ

### How to Select an AWS Region:
1. **Latency:** Select the region physically closest to your end users (e.g. `ap-south-1` Mumbai for India).
2. **Data Sovereignty & Compliance:** Indian customer data must reside in Indian soil.
3. **Service Availability:** Cutting-edge services frequently launch in `us-east-1` (N. Virginia) first.
4. **Cost:** Minor tax and power tariff differences exist across regions.

### Multi-AZ vs Multi-Region:
- **Multi-AZ (High Availability):** Synchronous data replication across distinct data centers in the same city. If data center A experiences a power failure, automated health checks shift database traffic to the standby instance in data center B with zero data loss (99.99% availability).
- **Multi-Region (Disaster Recovery):** Asynchronous replication across different continents (e.g. Mumbai + Frankfurt) for extreme disaster recovery and geographic latency optimization.

---

## 🗄️ 3. Databases: Relational vs NoSQL vs In-Memory

```
+-------------------+-------------------------------+-------------------------------+-------------------------------+
| Database Service  | Engine / Model                | High Availability Pattern     | Best Architectural Fit        |
+-------------------+-------------------------------+-------------------------------+-------------------------------+
| **Amazon RDS**    | Relational SQL (Postgres/MySQL)| Multi-AZ Synchronous Standby  | Financial ERP, SQL schemas    |
| **Amazon Aurora** | Cloud-native SQL (Postgres/MySQL)| 6-Way Storage across 3 AZs  | High-throughput auto-scaling  |
| **DynamoDB**      | Serverless NoSQL (Key-Value)  | Single-digit ms, Global Tables| Shopping carts, gaming leader |
| **ElastiCache**   | In-Memory Caching (Redis)     | In-memory cluster in RAM      | Session store, query offload  |
+-------------------+-------------------------------+-------------------------------+-------------------------------+
```

---

## 🐳 4. Containers: Docker, Amazon ECR & Amazon ECS vs Lambda

### 4.1 Step-by-Step ECR Push Commands via AWS CLI:
```bash
# 1. Authenticate Docker client to Amazon ECR
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.ap-south-1.amazonaws.com

# 2. Build local Docker image
docker build -t task-cloud-app:latest .

# 3. Tag image with Amazon ECR repository URI
docker tag task-cloud-app:latest 123456789012.dkr.ecr.ap-south-1.amazonaws.com/task-cloud-app:latest

# 4. Push image to Amazon ECR
docker push 123456789012.dkr.ecr.ap-south-1.amazonaws.com/task-cloud-app:latest
```

### 4.2 Architectural Showdown: Amazon ECS vs AWS Lambda Containers:
| Dimension | Amazon ECS (Fargate / EC2) | AWS Lambda Container Images |
|---|---|---|
| **Max Execution Time** | **Unlimited / Continuous** (Runs 24/7/365) | **Strict 15-Minute Maximum** |
| **Operational Model** | Persistent web APIs, worker services | Event-driven serverless (Scale-to-zero) |
| **Max Image Size** | Dozens of Gigabytes | Max 10 GB container image |
| **Cost Model** | Billed per-second of allocated vCPU/RAM | Billed per-millisecond of runtime ($0 if idle) |
| **Best For** | Heavy web apps, background queue processing | S3 file processing, webhooks, cron ETL |

---

## 📜 5. Infrastructure as Code (IaC) & CloudFormation Drift Detection

### Why CloudFormation Beats "ClickOps":
- **Repeatable & Automated:** Deploy complete multi-tier infrastructures in 5 minutes.
- **Git Versioned:** Reviewed through Pull Requests, preventing undocumented manual changes.
- **Atomic Deletions:** Deleting a stack deletes all child resources cleanly without orphan billing.

### What is Drift & How to Catch It?
1. **Drift Definition:** When an engineer logs into the AWS Management Console and manually alters a resource (e.g. resizes an EC2 instance or opens Port 22 in a Security Group) without modifying the CloudFormation template.
2. **Detection:** Run **Detect stack drift** in the AWS Console (or CLI: `aws cloudformation detect-stack-drift`).
3. **Remediation:**
   - **Option A:** Revert the manual console change back to match the template.
   - **Option B:** Update the CloudFormation YAML template to match the desired change, and apply it through a CloudFormation **Change Set**.

---

## 🛡️ 6. Zero-Dollar Student Hygiene (Daily Sunset Rule)

1. **Stop or Terminate** all practice EC2 instances at the end of each session.
2. Delete unattached EBS volumes in `available` state.
3. Delete custom CloudFormation stacks once practical labs conclude.
4. Release allocated Elastic IPs (EIPs).
5. Verify an AWS Billing Alarm is active at $0.01.
