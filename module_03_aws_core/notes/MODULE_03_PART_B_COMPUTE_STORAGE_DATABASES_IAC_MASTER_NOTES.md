# Module 03 · Part B: AWS Compute, Storage Triad, Databases & IaC Master Guide
> **TASK (Telangana Academy for Skill and Knowledge) · Nalgonda Center**  
> **Course:** Cloud Software Developer (AWS EC2-Centric / DVA-C02 Alignment)  
> **Trainer:** Sundeep Hiremat  
> **PDF Guide:** [Module_03_Part_B_Compute_Storage_Databases_IaC_Master_Guide.pdf](file:///e:/trainer/task/notes/Module_03_Part_B_Compute_Storage_Databases_IaC_Master_Guide.pdf)

---

## 🎬 1. AWS Compute: Amazon EC2 Deep Dive

### What is EC2 and Why Do We Use It?
**Amazon Elastic Compute Cloud (EC2)** provides resizable virtual machine compute capacity in the cloud.  
- **Why not just use Serverless (Lambda) for everything?**
  - **Full Root / Administrative Control:** You control the operating system kernel, system libraries, configuration files, and network interfaces.
  - **Persistent Background Daemons:** Long-running processes, WebSocket servers, microservice backends, and databases that cannot run on a 15-minute Lambda timeout.
  - **Legacy & Custom Software:** Any software that runs on traditional Linux or Windows servers runs natively on EC2 without refactoring.

---

### EC2 Instance Types & Families (The Tollywood Transport Fleet)

![EC2 Instance Types](file:///e:/trainer/task/module_03_aws_core/notes/diagrams/03_ec2_instance_types.png)

AWS provides hundreds of EC2 instance types grouped into 5 primary families. Use our **Tollywood Movie Shooting Fleet Metaphor** to remember them:

| Instance Family | Tollywood Transport Fleet Analogy | Hardware Architecture & Balance | Primary Use Cases |
| :--- | :--- | :--- | :--- |
| **General Purpose (`t3`, `t4g`, `m5`, `m6i`)** | **The Hero's Everyday City Swift Dzire / Auto** | Balanced CPU-to-memory ratio. `t3.micro` offers burstable CPU credits for Free Tier development. | Web servers, dev/test environments, small code repositories, backend business logic. |
| **Compute Optimized (`c5`, `c6g`, `c7i`)** | **The Action Chase Formula 1 Sports Car** | High CPU-to-memory ratio. Maximum compute power per dollar spent for pure number-crunching. | Media transcoding, scientific batch modeling, high-traffic gaming servers, dedicated compute jobs. |
| **Memory Optimized (`r5`, `r6g`, `x2gd`)** | **The 100-Member Lavish Wedding Dance Troupe Bus** | Huge RAM capacity per vCPU. Fast data processing in volatile memory without disk bottlenecks. | In-memory caches (**Redis**, Memcached), SAP HANA enterprise databases, real-time analytics. |
| **Storage Optimized (`i3en`, `i4i`, `d3`)** | **The 10-Ton Heavy Freight Goods Lorry** | Massive local high-IOPS NVMe SSD storage with direct motherboard bus throughput. | Data warehousing, distributed filesystems, NoSQL datastores (**Cassandra**, **Elasticsearch**). |
| **Accelerated / GPU (`p4d`, `g5`, `trn1`)** | **The Bahubali / RRR VFX Rendering Supercomputer** | Hardware GPU accelerators and machine learning silicon (AWS Trainium/Inferentia). | Deep learning LLM training, generative AI model inference, 3D computer graphics CGI rendering. |

---

### EC2 Purchasing & Pricing Models: The Box Office Ticket Counter

```
                        [ EC2 PRICING SPECTRUM ]
    Highest Flexibility                                  Maximum Cost Savings
    (Full Price / No Commitment)                         (Up to 90% Discount)
    ┌──────────────┬──────────────────┬─────────────────┬────────────────────┐
    │  On-Demand   │   Savings Plan   │    Reserved     │   Spot Instances   │
    │  (Per Sec)   │   ($/hr spend)   │  (1 or 3 Years) │   (Unused Capacity)│
    └──────────────┴──────────────────┴─────────────────┴────────────────────┘
```

| Purchasing Option | Tollywood Box Office Analogy | Discount Level | Commitment & Rules | Best Workload Fit |
| :--- | :--- | :--- | :--- | :--- |
| **On-Demand** | **Regular 11 AM Counter Ticket** | 0% (Full Price) | Pay strictly by the second with zero upfront and zero commitment. Stop anytime. | Unpredictable, short-term, or bursty workloads; initial dev/testing. |
| **Spot Instances** | **Current Counter Tatkal Ticket** | **Up to 90% OFF!** | Bid on excess spare cloud capacity. **AWS can reclaim the instance with a 2-minute warning!** | Stateless batch processing, video rendering, CI/CD runners, containerized workers. |
| **Reserved Instances (RI)** | **1-Year or 3-Year Season Pass** | **Up to 72% OFF** | Commit to a 1-year or 3-year term. **Standard RI** (locked family) vs **Convertible RI** (change OS/family). | Steady-state production workloads (e.g. 24/7 core relational databases). |
| **Savings Plans** | **Monthly Cinema & Canteen Pass** | **Up to 72% OFF** | Commit to a steady hourly spend (e.g. \$10/hr) across EC2, Fargate, and Lambda automatically. | Modern cloud workloads blending containers, serverless, and VMs. |
| **Dedicated Hosts** | **Booking the Entire Multiplex Screen** | Custom | Physical bare-metal server dedicated to 1 AWS account. Full socket & physical core visibility. | Strict regulatory compliance or Bring-Your-Own-License (BYOL) software (Windows Server, Oracle). |

---

### Key Pairs (`.pem` / `.ppk`): The Master Lock & Key Analogy
- **How it works:** AWS uses **asymmetric public-key cryptography**.
  - **Public Key:** AWS welds the public key into the server's `~/.ssh/authorized_keys` file when launching. (The Master Padlock on the server door).
  - **Private Key (`.pem`):** You download this file once during creation and save it on your laptop. (The physical key in your pocket).
- **Security Rule:** Linux SSH clients strictly reject keys with overly open permissions. You **MUST** restrict permissions before connecting:
  ```bash
  chmod 400 my-aws-key.pem
  ssh -i my-aws-key.pem ec2-user@<PUBLIC-IP>
  ```

### User Data (First-Boot Automation)
User Data is a shell script executed automatically with **root privileges** during the instance's very first startup:
```bash
#!/bin/bash
# Automatically install Nginx and start web server
yum update -y
yum install -y nginx
systemctl start nginx
systemctl enable nginx
echo "<h1>Hello from TASK Nalgonda Cloud Server!</h1>" > /usr/share/nginx/html/index.html
```

---

## 💾 2. The AWS Storage Triad: Pocket (EBS) vs Biryani Thali (EFS) vs D-Mart (S3)

![Storage Triad Comparison](file:///e:/trainer/task/module_03_aws_core/notes/diagrams/04_storage_triad_comparison.png)

### The Core Intuition & Everyday Metaphors:
- **Amazon EBS = Your Personal Jeans Pocket / School Bag:**  
  Bolted directly into one computer in one room (AZ). Raw blocks, maximum speed.
- **Amazon EFS = The Shared Family Biryani Thali / Wedding Buffet Table:**  
  A centralized file server that 100+ servers across multiple rooms (AZs) open, read, and write to simultaneously over the local network.
- **Amazon S3 = The Giant D-Mart Central Godown in Shamshabad:**  
  Store cargo boxes of any size via HTTP web URLs. Accessible anywhere on Earth, virtually indestructible (11 9's durability).

---

### Deep Dive: EBS (Block) vs EFS (File) — The 4 Crucial Differences

#### 1. How Data is Stored and Modified
- **EBS (Block-Level Storage):** The storage service sees your data **only as raw, unformatted chunks called blocks**, each assigned a unique sector address.  
  > 💡 **The "Aha!" Classroom Moment:**  
  > When you edit a single word in a 1 GB video file or a massive SQL database table, the operating system **only rewrites the tiny 4 KB block** containing that changed word! It does NOT re-upload or touch the remaining 999.99 MB.
- **EFS (File-Level Storage):** The storage system manages the entire directory tree of folders, files, and metadata (file names, owner permissions, access times). Every read or write must follow network POSIX file-locking semantics.

#### 2. Who Controls the File System?
- **EBS (The Student is in charge):** AWS gives you a blank, unformatted block device (e.g. `/dev/xvdf`). You must choose and format it with an OS filesystem (`mkfs -t ext4` or `xfs` in Linux, `NTFS` in Windows) before creating directories.
- **EFS (AWS is in charge):** AWS provides a fully managed, pre-formatted Linux Network File System (NFSv4). You simply mount it (`sudo mount -t efs fs-xxxx:/ /mnt/shared`), and it is immediately ready to store files. *(Note: EFS is Linux POSIX compliant; it does not natively support Windows EC2 instances).*

#### 3. Speed vs Network Overhead
- **EBS (Ultra-Low Latency):** Connects to the EC2 hypervisor via dedicated high-speed storage buses with **sub-millisecond (< 1 ms)** latency. This makes EBS mandatory for high-IOPS transactional databases (PostgreSQL, MySQL, MongoDB).
- **EFS (Network File Locking Overhead):** Because multiple EC2 servers access the exact same files simultaneously, EFS must coordinate distributed file locks to prevent race conditions. This network synchronization adds a slight overhead (**~3–5 ms latency**).

#### 4. Capacity & Pricing Model
- **EBS (Pre-Allocated Fixed Disk):** You choose a fixed volume size (e.g., 100 GB `gp3`). **You pay for all 100 GB every month**, even if you only store 5 GB of actual files!
- **EFS (Elastic Pay-as-you-Go):** Truly elastic. You do not pre-allocate size. If you store 5 GB today, you pay for 5 GB. If your users upload 500 GB tomorrow, it expands automatically, and when files are deleted, your bill shrinks immediately.

---

### 🏢 Real-World Architecture: How EBS, EFS & S3 Work Together
#### Example: High-Availability Multi-AZ WordPress Fleet

```
                        [ Internet Traffic via Route 53 ]
                                       │
                                       ▼
                       [ Application Load Balancer (ALB) ]
                                       │
             ┌─────────────────────────┴─────────────────────────┐
             ▼                                                   ▼
┌─────────────────────────┐                         ┌─────────────────────────┐
│ EC2 Instance 1 (AZ-1)   │                         │ EC2 Instance 2 (AZ-2)   │
│ ┌─────────────────────┐ │                         │ ┌─────────────────────┐ │
│ │  EBS Root Volume    │ │                         │ │  EBS Root Volume    │ │
│ │  (OS & Nginx / PHP) │ │                         │ │  (OS & Nginx / PHP) │ │
│ └─────────────────────┘ │                         │ └─────────────────────┘ │
└────────────┬────────────┘                         └────────────┬────────────┘
             │                                                   │
             │           Mounted Concurrently via NFS            │
             └─────────────────────────┬─────────────────────────┘
                                       ▼
                      ┌─────────────────────────────────┐
                      │    Amazon EFS Shared Storage    │
                      │  (/var/www/html/wp-content/     │
                      │   uploads - Images & Media)     │
                      └─────────────────────────────────┘
                                       │
                                       ▼
                      ┌─────────────────────────────────┐
                      │   Amazon RDS Multi-AZ Database  │
                      │   (Stores Blog Posts & Users)   │
                      └─────────────────────────────────┘
                                       │
                                       ▼
                      ┌─────────────────────────────────┐
                      │     Amazon S3 Object Bucket     │
                      │   (Daily Backups & CloudFront)  │
                      └─────────────────────────────────┘
```

1. **Amazon EBS:** Attached to each EC2 instance as the private root volume (`/dev/xvda`). Houses the Ubuntu OS, Nginx binaries, and PHP-FPM runtime. Fast, local, private.
2. **Amazon EFS:** Mounted across both EC2 instances simultaneously at `/var/www/html/wp-content/uploads`. When a visitor in AZ-1 uploads an image, the image is immediately readable by AZ-2!
3. **Amazon RDS:** Houses the relational database tables (blog articles, user logins, comments) with automatic Multi-AZ failover.
4. **Amazon S3:** Serves as the backup destination for nightly database snapshots and archives static CSS/JS assets distributed globally via Amazon CloudFront CDN.

---

## 🪣 3. Amazon S3 Storage Tiers Deep Dive: When to Use Which One

Amazon S3 offers **7 specialized storage tiers** engineered to balance access speed, retrieval costs, and storage price per gigabyte:

```
    Frequent Access                                           Archive & Compliance
    (Higher Storage Cost / $0 Retrieval Fee)                 (Lowest Storage Cost / Retrieval Fee)
    ┌──────────────┬──────────────────┬──────────────┬──────────────┬──────────────────┬──────────────┐
    │ S3 Standard  │ Intelligent-Tier │ Standard-IA  │ One Zone-IA  │ Glacier Instant  │ Deep Archive │
    │ (Hot Data)   │ (Auto-Pilot AI)  │ (Warm Data)  │ (2nd Backup) │ (Quarterly Pull) │ (7-10 Years) │
    └──────────────┴──────────────────┴──────────────┴──────────────┴──────────────────┴──────────────┘
```

| Storage Class | Everyday Metaphor | Min Duration | Retrieval Speed | Best Use Cases & Decision Trigger |
| :--- | :--- | :--- | :--- | :--- |
| **S3 Standard** | **Current Movie Posters on Hall Facade** | None | **Milliseconds** (Instant) | **Hot, frequently accessed data:** Active website assets, dynamic application files, user profile pictures. No retrieval fee. |
| **S3 Intelligent-Tiering** | **Smart AI Hall Manager** | 30 Days | **Milliseconds** (Instant) | **Unknown or unpredictable access patterns.** Automatically moves objects between Frequent, Infrequent, and Archive tiers based on usage with **zero retrieval fees**! |
| **S3 Standard-IA** *(Infrequent Access)* | **Theatre Storeroom Shelf** | 30 Days | **Milliseconds** (Instant) | **Warm data accessed less than once a month:** Disaster recovery backups, older customer receipts. Lower storage fee (\$0.0125/GB), but carries a small retrieval fee per GB. |
| **S3 One Zone-IA** | **Roadside Tin Shed** | 30 Days | **Milliseconds** (Instant) | **Secondary reproducible copies:** Stored in only 1 AZ (20% cheaper than Standard-IA). If the AZ is destroyed, data is lost. Ideal for image thumbnails or secondary offsite backups. |
| **S3 Glacier Instant Retrieval** | **Glass Trophy Showcase** | 90 Days | **Milliseconds** (Instant) | **Rarely accessed archive data requiring immediate millisecond viewing:** Medical records, quarterly compliance reports. 68% cheaper than Standard-IA. |
| **S3 Glacier Flexible Retrieval** | **Regional Film Archive Vault** | 90 Days | **Expedited: 1–5 min<br/>Standard: 3–5 hours<br/>Bulk: 5–12 hours** | **Traditional cold archives:** Historical database dumps, raw log files, legacy backups accessed 1–2 times per year. |
| **S3 Glacier Deep Archive** | **Deep Salt Mine Vault** | 180 Days | **Standard: 12 hours<br/>Bulk: 48 hours** | **The lowest-cost cloud storage on Earth (\$0.00099/GB/month - Rs. 80 / TB / mo):** Long-term regulatory compliance (7–10 year financial or healthcare retention). Retaining 1 TB costs just \$1.00 per month! |

### S3 Lifecycle Rules: Automatic Cost Optimization Pipeline
$$\text{Day 0: S3 Standard} \xrightarrow{\text{30 Days}} \text{S3 Standard-IA} \xrightarrow{\text{90 Days}} \text{S3 Glacier Flexible} \xrightarrow{\text{365 Days}} \text{S3 Glacier Deep Archive} \xrightarrow{\text{7 Years}} \text{Expire/Delete}$$

---

## 🗄️ 4. AWS Databases & In-Memory Caching: The Kirana Shop & Box Office Models

![Database Decision Matrix](file:///e:/trainer/task/module_03_aws_core/notes/diagrams/05_database_decision_matrix.png)

```
                     [ CHOOSE YOUR DATABASE ENGINE ]
                                    │
           Is your data relational (SQL with schema & JOINs)?
                      ├── YES ──► Need extreme throughput & cloud-native scale?
                      │             ├── YES ──► Amazon Aurora (5x MySQL, 6-way sync)
                      │             └── NO  ──► Amazon RDS (Postgres, MySQL, Multi-AZ)
                      │
                      └── NO  ──► Need single-digit millisecond NoSQL at any scale?
                                    ├── YES ──► Amazon DynamoDB (Serverless Key-Value)
                                    └── Need microsecond caching in RAM?
                                          └── YES ──► Amazon ElastiCache (Redis)
```

| Service | Kirana / Box Office Metaphor | Data Paradigm | Latency Profile | When to Choose This Service |
| :--- | :--- | :--- | :--- | :--- |
| **Amazon RDS** | **Traditional Baddi Khatavahi Ledger Book** | Relational SQL (Postgres, MySQL, MariaDB, Oracle, SQL Server) | Single-digit milliseconds | Traditional business ERP, financial ledgers, strict schemas, complex multi-table JOINs, ACID guarantees. Multi-AZ is a duplicate carbon-copy ledger kept at home! |
| **Amazon Aurora** | **High-Speed Barcode Billing System at D-Mart** | Cloud-native SQL (MySQL & Postgres compatible) | **5x faster than MySQL, 3x faster than Postgres** | Enterprise high-traffic SaaS, mission-critical banking, automatic storage auto-scaling up to 128 TiB without maintenance windows. Replicates 6 copies across 3 AZs! |
| **Amazon DynamoDB** | **Swiggy / Zomato Live Order Token Counter** | Serverless NoSQL (Key-Value & Document) | **Single-digit millisecond latency at any scale** | User shopping carts, real-time gaming state, IoT sensor telemetry, clickstreams. Handles 10 lakh hungry fans ordering simultaneously during an IPL final! |
| **Amazon ElastiCache** | **Kirana Counter Small Chillar Box & Front Tray** | In-Memory Data Store (Redis & Memcached) | **Sub-millisecond microsecond latency** (reads from RAM) | Sits in front of RDS/DynamoDB (**Cache-Aside pattern**) to eliminate slow database query repeats and store user auth sessions. |

---

## 🏗️ 5. Bridge to Module 04: Infrastructure as Code (IaC) with CloudFormation

### The Mahishmati Palace Blueprint Analogy:
- **ClickOps (Manual Console):** The director shouting at 50 carpenters on the spot: *"Put a pillar here, paint that wall yellow, move that light!"* If you want to recreate the set in Nalgonda tomorrow, nobody remembers how it was built!
- **CloudFormation (IaC):** The **Architectural Blueprints & CAD Model** of the Bahubali Mahishmati Palace set. You write the blueprint in YAML. Click one button, and AWS builds the entire palace in 5 minutes!

### Anatomy of an AWS CloudFormation Template (YAML):
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'TASK Nalgonda - Production CloudFormation Stack'

Parameters:
  InstanceType:
    Type: String
    Default: 't3.micro'
    Description: 'EC2 instance compute size'

Resources:
  MyWebServerSG:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
      GroupDescription: 'Allow HTTP Port 80'
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0

  MyWebServer:
    Type: 'AWS::EC2::Instance'
    Properties:
      InstanceType: !Ref InstanceType
      ImageId: 'ami-0c55b159cbfafe1f0' # Amazon Linux 2023
      SecurityGroupIds:
        - !Ref MyWebServerSG

Outputs:
  ServerPublicIP:
    Description: 'Public IP of the deployed EC2 server'
    Value: !GetAtt MyWebServer.PublicIp
```

### CloudFormation Drift Detection & Remediation
- **What is Drift?** At midnight, an assistant director sneaks into the film set and paints Pillar #4 red without updating the blueprint!
- **How to Detect Drift:**
  1. Open CloudFormation Console $\rightarrow$ Select Stack $\rightarrow$ **Stack actions** $\rightarrow$ **Detect drift**.
  2. The scanner alarms: **Pillar #4 DRIFTED! Expected: Gold, Actual: Red!**
- **How to Remediate Drift:**
  - **Option 1 (Rollback):** Repaint the pillar gold to match the blueprint.
  - **Option 2 (Update Code):** Update the CloudFormation YAML template to accept the new red color and deploy using a **Change Set**.

---

## 🛡️ 6. Student Zero-Dollar Sunset Checklist

Every student must complete this checklist before closing their AWS console:
1. **Stop or Terminate** all practice EC2 instances.
2. In the EC2 console, go to **Elastic Block Store $\rightarrow$ Volumes** and delete any detached volumes in `available` state.
3. Delete custom **CloudFormation stacks** to cleanly terminate all child resources.
4. Release any unattached **Elastic IPs (EIPs)**.
5. Review the **AWS Billing Dashboard** to confirm a \$0.00 balance.

---
*Created by **Sundeep Hiremat** for TASK Nalgonda Center · Cloud Software Developer Mastery Program (2026).*
