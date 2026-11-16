# Module 03 · Part B: AWS Compute, Storage Triad, Databases & IaC Master Guide
> **TASK (Telangana Academy for Skill and Knowledge) · Nalgonda Center**  
> **Course:** Cloud Software Developer (AWS EC2-Centric / DVA-C02 Alignment)  
> **Trainer:** Sundeep Hiremat  
> **PDF Guide:** [Module_03_Part_B_Compute_Storage_Databases_IaC_Master_Guide.pdf](file:///e:/trainer/task/notes/Module_03_Part_B_Compute_Storage_Databases_IaC_Master_Guide.pdf)

---

## 🚗 1. AWS Compute: Amazon EC2 Deep Dive

### What is EC2 and Why Do We Use It?
**Amazon Elastic Compute Cloud (EC2)** provides resizable, secure compute capacity in the cloud.  
- **Why not just use Serverless (Lambda) for everything?**
  - **Full Root / Administrative Control:** You control the operating system kernel, system libraries, configuration files, and network interfaces.
  - **Persistent Background Daemons:** Long-running processes, WebSocket servers, microservice backends, and databases that cannot run on a 15-minute Lambda timeout.
  - **Legacy & Custom Software:** Any software that runs on traditional Linux or Windows servers runs natively on EC2 without refactoring.

---

### EC2 Instance Types & Families (The Vehicle Metaphors)

![EC2 Instance Types](file:///e:/trainer/task/module_03_aws_core/notes/diagrams/03_ec2_instance_types.png)

AWS provides hundreds of EC2 instance types grouped into 5 primary families. Use our **Automobile Fleet Metaphor** to remember them:

| Instance Family | Vehicle Metaphor | Hardware Architecture & Balance | Primary Use Cases |
| :--- | :--- | :--- | :--- |
| **General Purpose (`t3`, `t4g`, `m5`, `m6i`)** | **The Family Sedan / Hatchback** | Balanced CPU-to-memory ratio. `t3.micro` offers burstable CPU credits for Free Tier development. | Web servers, dev/test environments, small code repositories, backend business logic. |
| **Compute Optimized (`c5`, `c6g`, `c7i`)** | **The Formula 1 Sports Car** | High CPU-to-memory ratio. Maximum compute power per dollar spent. | Media encoding, scientific batch modeling, high-traffic gaming servers, dedicated compute jobs. |
| **Memory Optimized (`r5`, `r6g`, `x2gd`)** | **The Luxury Double-Decker Tour Bus** | Huge RAM capacity per vCPU. Fast data processing in volatile memory. | In-memory caches (**Redis**, Memcached), SAP HANA enterprise databases, real-time analytics. |
| **Storage Optimized (`i3en`, `i4i`, `d3`)** | **The Heavy Freight Cargo Truck** | Massive local high-IOPS NVMe SSD storage with direct bus throughput. | Data warehousing, distributed filesystems, NoSQL datastores (**Cassandra**, **Elasticsearch**). |
| **Accelerated / GPU (`p4d`, `g5`, `trn1`)** | **The Supersonic Jet Rocket Engine** | Hardware GPU accelerators and machine learning silicon (AWS Trainium/Inferentia). | Deep learning LLM training, generative AI model inference, 3D computer graphics rendering. |

---

### EC2 Purchasing & Pricing Models

```
                        [ EC2 PRICING SPECTRUM ]
    Highest Flexibility                                  Maximum Cost Savings
    (Full Price / No Commitment)                         (Up to 90% Discount)
    ┌──────────────┬──────────────────┬─────────────────┬────────────────────┐
    │  On-Demand   │   Savings Plan   │    Reserved     │   Spot Instances   │
    │  (Per Sec)   │   ($/hr spend)   │  (1 or 3 Years) │   (Unused Capacity)│
    └──────────────┴──────────────────┴─────────────────┴────────────────────┘
```

| Purchasing Option | Everyday Analogy | Discount Level | Commitment & Rules | Best Workload Fit |
| :--- | :--- | :--- | :--- | :--- |
| **On-Demand** | **Uber / Metered Taxi Ride** | 0% (Full Price) | Pay strictly by the second with zero upfront and zero commitment. Stop anytime. | Unpredictable, short-term, or bursty workloads; initial dev/testing. |
| **Spot Instances** | **Standby Flight Ticket** | **Up to 90% OFF!** | Bid on excess spare cloud capacity. **AWS can reclaim the instance with a 2-minute termination notice!** | Stateless batch processing, video rendering, CI/CD runners, containerized workers. |
| **Reserved Instances (RI)** | **1-Year or 3-Year Rental Lease** | **Up to 72% OFF** | Commit to a 1-year or 3-year term. **Standard RI** (locked family) vs **Convertible RI** (change OS/family). | Steady-state production workloads (e.g. 24/7 core relational databases). |
| **Savings Plans** | **Flexible Monthly Transit Pass** | **Up to 72% OFF** | Commit to a steady hourly spend (e.g. \$10/hr) across EC2, Fargate, and Lambda automatically. | Modern cloud workloads blending containers, serverless, and VMs. |
| **Dedicated Hosts** | **Booking the Entire Hotel Wing** | Custom | Physical bare-metal server dedicated to 1 AWS account. Full socket & physical core visibility. | Strict regulatory compliance or Bring-Your-Own-License (BYOL) software (Windows Server, Oracle). |

---

### Key Pairs (`.pem` / `.ppk`): The Master Lock & Key Analogy
- **How it works:** AWS uses **asymmetric public-key cryptography**.
  - **Public Key:** AWS injects the public key into the server's `~/.ssh/authorized_keys` file when launching. (The Master Padlock on the server door).
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

## 💾 2. The AWS Storage Triad: EBS vs EFS vs S3

![Storage Triad Comparison](file:///e:/trainer/task/module_03_aws_core/notes/diagrams/04_storage_triad_comparison.png)

| Characteristic | Amazon EBS (Block Storage) | Amazon EFS (File Storage) | Amazon S3 (Object Storage) |
| :--- | :--- | :--- | :--- |
| **Everyday Metaphor** | **The Car's Personal Trunk** | **The Shared Fleet Roof Rack** | **The Global Shipping Container Depot** |
| **Storage Paradigm** | Raw unformatted virtual disk blocks | Hierarchical POSIX directory filesystem | Flat namespace object store (Buckets / Keys) |
| **Scope & Availability** | **Single Availability Zone (AZ)** | **Regional (Multi-AZ synchronous)** | **Regional / Global (Replicated across 3+ AZs)** |
| **Concurrent Access** | 1 EC2 instance (Multi-Attach io2 only) | **Thousands of EC2 instances concurrently** | **Unlimited clients via HTTPS REST API** |
| **Network Protocol** | Dedicated storage network (SCSI block) | Network File System (NFSv4 / Port 2049) | REST API over HTTPS (Port 443) |
| **Latency** | **< 1 millisecond** (ultra-low latency) | ~3–5 milliseconds | ~50–100 milliseconds |
| **Durability** | 99.8% – 99.999% volume durability | 99.999999999% (11 9's) | **99.999999999% (11 9's durability)** |
| **Boot Drive Capability** | **YES (Required for EC2 OS boot)** | NO (Cannot boot an OS from EFS) | NO (Cannot boot an OS from S3) |
| **Volume / Tier Types** | `gp3` (General Purpose), `io2` (High IOPS), `st1` (HDD) | General Purpose, Max I/O, EFS One Zone | Standard, Intelligent-Tiering, Standard-IA, Glacier |
| **Decision Trigger** | OS root drive; high-speed transactional SQL database storage. | Shared web uploads (WordPress `wp-content`), distributed CMS, shared media. | Static website hosting, documents, videos, backups, data lakes, ML datasets. |

### S3 Security & HTTPS Enforced Policy
In enterprise production, you must enforce HTTPS encryption in transit by attaching a JSON Bucket Policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EnforceTLSRequestsOnly",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-production-bucket",
        "arn:aws:s3:::my-production-bucket/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

---

## 🗄️ 3. AWS Databases & In-Memory Caching: When to Use Which One

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

| Service | Data Model | High Availability & Scaling | Latency Profile | When to Choose This Service |
| :--- | :--- | :--- | :--- | :--- |
| **Amazon RDS** | Relational SQL (Postgres, MySQL, MariaDB, Oracle, SQL Server) | **Multi-AZ synchronous standby failover**. Read Replicas (up to 15) for scaling read queries. | Single-digit milliseconds | Traditional business ERP, financial ledgers, strict schemas, complex multi-table JOINs, ACID guarantees. |
| **Amazon Aurora** | Cloud-native SQL (MySQL & Postgres compatible) | **Storage replicated 6 ways across 3 AZs**. Auto-expands storage up to 128 TiB. Aurora Serverless v2. | **5x faster than MySQL, 3x faster than Postgres** | Enterprise high-traffic SaaS, mission-critical banking, automatic storage auto-scaling without maintenance windows. |
| **Amazon DynamoDB** | Serverless NoSQL (Key-Value & Document) | Multi-AZ automatic replication. On-Demand auto-scaling to millions of requests per second. | **Single-digit millisecond latency at any scale** | User shopping carts, real-time gaming state, IoT sensor telemetry, clickstreams, massive write loads. |
| **Amazon ElastiCache** | In-Memory Data Store (Redis & Memcached) | Multi-AZ with automated failover (Redis clusters). | **Sub-millisecond microsecond latency** (reads from RAM) | Sits in front of RDS/DynamoDB (**Cache-Aside pattern**) to eliminate slow database query repeats and store user auth sessions. |

---

## 🏗️ 4. Bridge to Module 04: Infrastructure as Code (IaC) with CloudFormation

### Why Infrastructure as Code (IaC) Beats "ClickOps"?
1. **Repeatability:** Deploy an entire 3-tier architecture across 5 AWS regions in 5 minutes with zero human configuration errors.
2. **Version Control:** Infrastructure templates are checked into Git, allowing peer review via Pull Requests.
3. **Atomic Clean Teardown:** Deleting a CloudFormation stack automatically destroys all provisioned child resources cleanly, preventing accidental runaway bills.

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
- **What is Drift?** Drift occurs when someone makes manual "out-of-band" changes directly in the AWS Management Console (e.g., resizing an EC2 instance or adding an open inbound port in a Security Group) without modifying the CloudFormation template.
- **How to Detect Drift:**
  1. Open CloudFormation Console $\rightarrow$ Select Stack $\rightarrow$ **Stack actions** $\rightarrow$ **Detect drift**.
  2. Review the **Drift Details** report: AWS flags modified properties in red side-by-side with expected values.
- **How to Remediate Drift:**
  - **Option 1 (Rollback):** Revert the manual console change back to match the original template.
  - **Option 2 (Update Code):** Update the CloudFormation YAML template to incorporate the new property and deploy using a **Change Set**.

---

## 🛡️ 5. Student Zero-Dollar Sunset Checklist

Every student must complete this checklist before closing their AWS console:
1. **Stop or Terminate** all practice EC2 instances.
2. In the EC2 console, go to **Elastic Block Store $\rightarrow$ Volumes** and delete any detached volumes in `available` state.
3. Delete custom **CloudFormation stacks** to cleanly terminate all child resources.
4. Release any unattached **Elastic IPs (EIPs)**.
5. Review the **AWS Billing Dashboard** to confirm a \$0.00 balance.

---
*Created by **Sundeep Hiremat** for TASK Nalgonda Center · Cloud Software Developer Mastery Program (2026).*
