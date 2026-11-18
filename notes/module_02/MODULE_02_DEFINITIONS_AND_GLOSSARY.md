# AWS Cloud Software Developer — Master Definitions & Glossary (Modules 2 & 3)
> **Program:** Telangana Academy for Skill and Knowledge (TASK)  
> **Course Track:** Cloud Software Developer  
> **Coverage:** Complete Terminology, Acronyms, Architecture & Real-World Analogies for Module 2 & Module 3  
> **Target Audience:** Engineering Students, Cloud Beginners & Certification Candidates  

---

## 📑 Table of Contents by Category
1. [Cloud Computing Fundamentals & Economics (Module 2.a)](#1-cloud-computing-fundamentals--economics-module-2a)
2. [AWS Global Infrastructure (Module 2.a)](#2-aws-global-infrastructure-module-2a)
3. [Compute Services & Virtualization (Modules 2.a & 3.a)](#3-compute-services--virtualization-modules-2a--3a)
4. [Storage Architectures (Modules 2.a & 3.b)](#4-storage-architectures-modules-2a--3b)
5. [Database & Caching Technologies (Modules 2.a & 3.b)](#5-database--caching-technologies-modules-2a--3b)
6. [Security, Identity & Governance (Modules 2.b & 3.b)](#6-security-identity--governance-modules-2b--3b)
7. [Management, Monitoring & Integration (Module 2.b)](#7-management-monitoring--integration-module-2b)
8. [VPC Networking & Traffic Routing (Module 3.c)](#8-vpc-networking--traffic-routing-module-3c)
9. [Web Security & Content Acceleration: WAF & CloudFront (Module 3.c)](#9-web-security--content-acceleration-waf--cloudfront-module-3c)
10. [Infrastructure as Code (IaC) & CloudFormation (Module 3.d)](#10-infrastructure-as-code-iac--cloudformation-module-3d)

---

## 1. Cloud Computing Fundamentals & Economics (Module 2.a)

### Cloud Computing
* **Technical Definition:** The on-demand delivery of compute power, database storage, applications, and other IT resources through a cloud services platform via the internet with pay-as-you-go pricing.
* **Student Explanation:** Instead of buying and maintaining physical server machines in your house or college lab, you rent computing resources from Amazon's massive data centers across the internet.
* **Real-World Analogy:** Renting electricity from the municipal power grid rather than building your own private power generator.

### CapEx (Capital Expenditure)
* **Technical Definition:** Upfront investments made by an organization in physical fixed assets such as servers, cooling systems, data center real estate, and networking cables before launching an application.
* **Student Explanation:** Buying an expensive car with a large upfront down payment before you even know if you need to travel.

### OpEx (Operational Expenditure)
* **Technical Definition:** Day-to-day ongoing operational expenses where you pay only for the exact resources your business consumes over a given billing period.
* **Student Explanation:** Paying for an Uber or auto-rickshaw ride only for the exact distance travelled.

### Public Cloud
* **Technical Definition:** Cloud infrastructure owned, managed, and operated by a third-party cloud provider (such as AWS), delivering computing resources over the public internet to multiple client organizations (multi-tenant architecture).
* **Student Explanation:** A commercial multiplex theatre where multiple moviegoers share the building, but each has their own ticket and assigned seat.

### Private Cloud
* **Technical Definition:** Cloud infrastructure provisioned and operated exclusively for a single enterprise, hosted either on-premises or by a third party.
* **Student Explanation:** A home home-theatre system installed inside a private bungalow for a single family.

### Hybrid Cloud
* **Technical Definition:** A unified computing environment connecting on-premises infrastructure (private cloud) with third-party public cloud services via encrypted VPN or dedicated fiber lines (AWS Direct Connect).
* **Student Explanation:** A college keeping confidential exam papers on internal offline office servers while hosting student admission registration on AWS to handle massive traffic.

### IaaS (Infrastructure as a Service)
* **Technical Definition:** A cloud service model providing raw, virtualized computing resources (virtual servers, block storage, networking firewalls) over the internet.
* **Key Boundary:** Customer manages the Operating System, installed software, runtimes, and security patches; AWS manages physical hardware and virtualization.
* **AWS Examples:** Amazon EC2, Amazon EBS, Amazon VPC.

### PaaS (Platform as a Service)
* **Technical Definition:** A cloud service model providing a pre-configured platform allowing customers to develop, run, and manage applications without the complexity of building and maintaining infrastructure.
* **Key Boundary:** Customer writes and uploads application code; AWS automatically handles OS patching, scaling, and server maintenance.
* **AWS Examples:** AWS Elastic Beanstalk, AWS Lambda.

### SaaS (Software as a Service)
* **Technical Definition:** A complete cloud service delivery model where end-user applications are hosted, operated, and maintained entirely by the cloud vendor.
* **Key Boundary:** Provider manages hardware, OS, code, databases, and updates; customer accesses the app via web browser.
* **Examples:** Gmail, Microsoft 365, Salesforce.

---

## 2. AWS Global Infrastructure (Module 2.a)

### AWS Region
* **Technical Definition:** A distinct physical geographical location worldwide containing a cluster of multiple isolated, physically separated Availability Zones.
* **Student Explanation:** A major geographic hub (e.g., `ap-south-1` Mumbai, `us-east-1` N. Virginia) where Amazon has built clusters of data centers.
* **Key Rule:** Regions are completely independent for legal compliance, data sovereignty, and fault isolation.

### Availability Zone (AZ)
* **Technical Definition:** One or more discrete data centers within an AWS Region, each equipped with independent redundant power, cooling, and networking connectivity, linked to other AZs via ultra-low-latency fiber networks.
* **Student Explanation:** Individual data centers within the city (e.g., `ap-south-1a`, `ap-south-1b`, `ap-south-1c`). If a flood knocks out data center 'A', data center 'B' continues running without interruption.
* **Key Rule:** Every AWS Region has a minimum of 3 Availability Zones.

### Edge Location (Point of Presence / PoP)
* **Technical Definition:** A specialized site that AWS uses to cache web content closer to end-users globally via Amazon CloudFront and Route 53.
* **Student Explanation:** Local caching kiosks stationed in major metropolitan cities (Hyderabad, Chennai, Bengaluru, Delhi) so Indian users don't have to fetch website images from servers across the world.

---

## 3. Compute Services & Virtualization (Modules 2.a & 3.a)

### Amazon EC2 (Elastic Compute Cloud)
* **Technical Definition:** A web service providing secure, resizable compute capacity (virtual servers) in the cloud.
* **Student Explanation:** A virtual computer running Linux or Windows in Amazon's data center that you can start, stop, resize, and access via SSH/terminal in 30 seconds.

### EC2 Instance Types & Families
* **Technical Definition:** Pre-configured hardware combinations of CPU, Memory, Storage, and Networking optimized for specific workloads.
* **Key Families:**
  - `T` & `M` (General Purpose): Balanced compute, memory, and networking (e.g., `t2.micro`, `t3.medium`).
  - `C` (Compute Optimized): High-performance processors for batch processing, gaming servers, and media transcoding.
  - `R` (Memory Optimized): High RAM capacity for in-memory databases (Redis/ElastiCache) and big data analytics.
  - `I` & `D` (Storage Optimized): High sequential read/write IOPS for massive distributed file systems.

### EC2 Instance Lifecycle States
* **Pending:** Launch initiated; AWS is allocating virtual hardware.
* **Running:** Instance is active, billed per second, and accessible over the network.
* **Stopping:** Graceful shutdown initiated; memory flushed to disk.
* **Stopped:** Virtual hardware released; no compute charges (only attached EBS storage is billed).
* **Terminated:** Permanent deletion; virtual machine destroyed and root EBS volume wiped.

### Key Pair
* **Technical Definition:** A cryptographic authentication mechanism consisting of a Public Key (stored by AWS on the instance) and a Private Key (a `.pem` or `.ppk` file kept secretly by the user) used to securely log in via SSH without passwords.

### Security Group (SG)
* **Technical Definition:** A stateful virtual firewall that operates at the elastic network interface (ENI) level of an EC2 instance to control inbound and outbound IPv4/IPv6 traffic.
* **Key Rule:** **Stateful:** If an inbound packet is allowed in (e.g., HTTP on Port 80), return response traffic is automatically allowed out, regardless of outbound rules!

### Amazon ECS (Elastic Container Service)
* **Technical Definition:** A fully managed container orchestration service that makes it easy to deploy, manage, and scale Docker containerized applications across AWS clusters.

---

## 4. Storage Architectures (Modules 2.a & 3.b)

### Amazon S3 (Simple Storage Service)
* **Technical Definition:** An object storage service offering industry-leading scalability, data availability, security, and performance with 99.999999999% (11 9's) durability.
* **Student Explanation:** A massive, virtually limitless cloud hard drive accessible via web HTTP URLs. You store files as "objects" (photos, videos, backups, HTML code) inside containers called "buckets".

### S3 Storage Classes
* **S3 Standard:** For frequently accessed data with millisecond latency.
* **S3 Intelligent-Tiering:** Automatically moves objects between frequent, infrequent, and archive access tiers based on usage patterns to slash costs with zero operational overhead.
* **S3 Standard-IA (Infrequent Access):** For data accessed less frequently but requiring immediate millisecond access when needed (cheaper storage, small retrieval fee).
* **S3 Glacier Flexible Archive:** Cold archive storage for compliance and audit records; retrieval takes 1 minute to 5 hours.
* **S3 Glacier Deep Archive:** The lowest-cost storage in the cloud ($1 per TB per month); retrieval takes 12 to 48 hours.

### S3 Object Versioning
* **Technical Definition:** A bucket feature that keeps multiple variants of an object in the same bucket.
* **Student Explanation:** Accidental deletion protection. If you delete `index.html`, S3 adds a "Delete Marker" instead of erasing the file, allowing you to restore historical versions instantly!

### Amazon EBS (Elastic Block Store)
* **Technical Definition:** High-performance, persistent block-level storage volumes designed for use with Amazon EC2 instances.
* **Student Explanation:** The virtual C: drive or Linux root SSD hard drive plugged into an EC2 server.
* **Key Rule:** Bound to a single Availability Zone. To backup an EBS volume, you take an **EBS Snapshot** (stored durably in S3).

### Amazon EFS (Elastic File System)
* **Technical Definition:** A serverless, fully elastic network file system (NFS) that automatically grows and shrinks as you add and remove files.
* **Student Explanation:** A shared network folder (like Google Drive) that can be mounted simultaneously by 1,000+ EC2 Linux instances for concurrent read and write.

---

## 5. Database & Caching Technologies (Modules 2.a & 3.b)

### Amazon RDS (Relational Database Service)
* **Technical Definition:** A managed web service that simplifies the setup, operation, and scaling of relational SQL databases in the cloud.
* **Supported Engines:** MySQL, PostgreSQL, MariaDB, Oracle, Microsoft SQL Server, and Amazon Aurora.
* **Student Explanation:** Instead of installing MySQL manually on an EC2 server and worrying about Linux updates and daily backups, RDS automates hardware provisioning, database engine patching, automated daily snapshots, and failover.

### Multi-AZ Deployment (RDS)
* **Technical Definition:** An RDS high-availability architecture that automatically provisions and maintains a synchronous standby replica in a different Availability Zone.
* **Student Explanation:** If a power outage hits your primary database in `ap-south-1a`, RDS automatically flips the DNS endpoint to the standby database in `ap-south-1b` in under 60 seconds with zero data loss!

### Amazon Aurora
* **Technical Definition:** AWS's cloud-native relational database engine compatible with MySQL and PostgreSQL, delivering up to 5x the throughput of standard MySQL.
* **Key Architecture:** Replicates 6 copies of your database storage across 3 Availability Zones automatically and features a distributed, self-healing storage subsystem.

### Amazon DynamoDB
* **Technical Definition:** A fully managed, serverless, key-value and document NoSQL database designed to deliver single-digit millisecond performance at any scale.
* **Key Concepts:**
  - **Partition Key (PK):** Hash attribute used to distribute data across physical storage partitions.
  - **Sort Key (SK):** Range attribute used to store related items together in sorted order.
  - **On-Demand Capacity:** Pay purely per read and write request with zero capacity planning.

### Amazon ElastiCache
* **Technical Definition:** A fully managed in-memory data store and cache service supporting Redis and Memcached.
* **Student Explanation:** Caches frequent database queries in ultra-fast RAM so that instead of querying a disk-based SQL database (taking 50ms), data is fetched in 1 millisecond.

---

## 6. Security, Identity & Governance (Modules 2.b & 3.b)

### AWS Shared Responsibility Model
* **Technical Definition:** A security framework that outlines the distinct security obligations of AWS versus the customer.
* **AWS Responsibility:** **Security "OF" the Cloud:** Physical data centers, server hardware, hypervisor virtualization software, and global networking cables.
* **Customer Responsibility:** **Security "IN" the Cloud:** Customer data, operating system updates & patches on EC2, firewall rules (Security Groups), and IAM user credentials.

### AWS IAM (Identity and Access Management)
* **Technical Definition:** A web service that helps you securely control access to AWS resources by managing authentication and authorization.
* **Root Account:** The initial identity created with complete administrative access. Must be protected with MFA and never used for everyday coding!
* **IAM User:** An individual account created for a specific student or employee.
* **IAM Group:** A collection of IAM users (e.g., `DevOpsTeam`) sharing the same permissions.
* **IAM Policy:** A formal JSON document stating: **Effect** (Allow/Deny), **Action** (`s3:GetObject`), **Resource** (`arn:aws:s3:::bucket/*`), and **Condition**.
* **IAM Role:** Temporary credentials assumed by AWS services (e.g., granting an EC2 instance permission to write to S3 without saving access keys in code).
* **Least Privilege Principle:** Granting users only the minimum permissions necessary to complete their job, and nothing more!

---

## 7. Management, Monitoring & Integration (Module 2.b)

### Amazon CloudWatch
* **Technical Definition:** A monitoring and observability service providing data and actionable insights for AWS, hybrid, and on-premises resources.
* **Student Explanation:** The car dashboard: displays CPU percentage, network traffic graphs, memory usage, and sounds an alarm when metrics exceed safe thresholds.

### AWS CloudTrail
* **Technical Definition:** An auditing, compliance, and governance service that records every API call made in your AWS account (via Management Console, CLI, or SDK).
* **Student Explanation:** The aircraft black box: records *who* logged in, *what* command they executed, *when*, and from *which IP address*.

### Amazon SQS (Simple Queue Service)
* **Technical Definition:** A fully managed message queuing service that enables you to decouple and scale microservices, distributed systems, and serverless applications.
* **Standard Queue:** Unlimited throughput, at-least-once delivery, best-effort message ordering.
* **FIFO Queue:** Strictly First-In-First-Out message delivery, exactly-once processing.

### Amazon SNS (Simple Notification Service)
* **Technical Definition:** A fully managed publish/subscribe (pub/sub) messaging service that delivers messages to multiple subscribing endpoints (SQS queues, HTTP webhooks, Lambda functions, email, and SMS).
* **Student Explanation:** A megaphone: one publisher broadcasts a message once, and SNS fans it out to thousands of subscribers simultaneously.

---

## 8. VPC Networking & Traffic Routing (Module 3.c)

### Amazon VPC (Virtual Private Cloud)
* **Technical Definition:** A logically isolated virtual network dedicated to your AWS account, configured with private IP address ranges (CIDR blocks), subnets, route tables, and gateways.
* **Tollywood Analogy:** The Sandhya 70mm Multiplex boundary compound wall. Nobody enters or leaves the compound without explicit gates.

### CIDR Block (Classless Inter-Domain Routing)
* **Technical Definition:** A method for allocating IP addresses and IP routing using a prefix length notation (e.g., `10.0.0.0/16`).
* **Sizing Rules:**
  - `10.0.0.0/16` = $2^{32-16} = 2^{16} = 65,536$ private IPv4 addresses.
  - `10.0.1.0/24` = $2^{32-24} = 2^8 = 256$ IP addresses.

### AWS Subnet Reserved IPs (The "Minus 5" Rule)
* **Technical Definition:** In every AWS subnet, **5 IP addresses** are reserved by Amazon and cannot be assigned to instances:
  1. `10.0.0.0`: Network address.
  2. `10.0.0.1`: VPC Router address.
  3. `10.0.0.2`: DNS server address (Route 53 Resolver).
  4. `10.0.0.3`: Reserved by AWS for future use.
  5. `10.0.0.255`: Network broadcast address (AWS does not support broadcast, so this is reserved).
* **Usable IPs Formula:** In a `/24` subnet (256 total IPs), exactly **251 IPs** are usable!

### Public Subnet
* **Technical Definition:** A subnet whose associated Route Table has an explicit default route (`0.0.0.0/0`) pointing to an Internet Gateway (IGW).
* **Tollywood Analogy:** The front ticket counter and canteen area open to movie fans walking in from the public road.

### Private Subnet
* **Technical Definition:** A subnet whose Route Table does NOT have a direct route to an Internet Gateway. Instances inside receive only private IPs.
* **Tollywood Analogy:** The theatre projector room and cash safe (galla pette). Outside fans cannot walk in.

### Internet Gateway (IGW)
* **Technical Definition:** A horizontally scaled, redundant, highly available VPC component that allows communication between your VPC and the internet, performing 1-to-1 NAT translation for public IPv4 addresses.
* **Tollywood Analogy:** The main double-door grand entrance gate of the theatre complex connecting to the public highway.

### NAT Gateway
* **Technical Definition:** A managed Network Address Translation service that enables instances in a private subnet to connect to outbound internet services (e.g., downloading security patches or OS updates) while preventing unsolicited inbound traffic from reaching them.
* **Tollywood Analogy:** "Chotu", the trusted theatre canteen boy who has an exit gate pass (Elastic IP). He steps out to the highway to fetch food deliveries and software patches for the staff inside, but outsiders cannot follow him back in!

### Route Table
* **Technical Definition:** A set of routing rules (called routes) that determine where network packets from your subnet are directed.
* **Standard Rule:** `10.0.0.0/16 -> local` (Traffic within the VPC stays inside). `0.0.0.0/0 -> igw-xxxx` (Unknown traffic goes out to the internet).

### Network ACL (NACL)
* **Technical Definition:** An optional, stateless layer of security that acts as a firewall for controlling traffic in and out of one or more subnets.
* **Key Differences vs. Security Groups:**
  - **Stateless:** Both Inbound AND Outbound rules must be explicitly created!
  - Evaluated in numerical order (Rule 100 before Rule 200).
  - Can explicitly **DENY** specific IP addresses (Security Groups can only ALLOW).
* **Tollywood Analogy:** The police traffic checkpoint outside RTC X Roads checking helmet and RC on the way in, and re-checking on the way out.

---

## 9. Web Security & Content Acceleration: WAF & CloudFront (Module 3.c)

### AWS WAF (Web Application Firewall)
* **Technical Definition:** A layer 7 application firewall that monitors HTTP and HTTPS requests forwarded to Amazon CloudFront, an Application Load Balancer, or API Gateway, allowing you to filter malicious traffic based on customizable rules.
* **Why Use It:** Defends against SQL Injection (SQLi), Cross-Site Scripting (XSS), bad bots, and HTTP flood attacks that bypass Layer 4 Security Groups!

### Web ACL (Web Access Control List)
* **Technical Definition:** The top-level AWS WAF resource containing the rules and rule groups that evaluate incoming HTTP/S requests.
* **Default Action:** Can be set to **Allow** (filter only bad traffic) or **Block** (whitelist only approved traffic).

### Amazon CloudFront
* **Technical Definition:** A global Content Delivery Network (CDN) service that securely delivers data, videos, applications, and APIs to users globally with low latency and high transfer speeds via 450+ Edge Locations.

### Cache Hit vs. Cache Miss
* **Cache Hit:** The requested asset is already stored in the local Edge Location's cache and is returned to the user's browser in ~10 milliseconds without touching the origin.
* **Cache Miss:** The requested asset is not in edge cache. CloudFront forwards the request across the private AWS backbone to the origin server (S3 or ALB), serves the user, and caches the file for future visitors.

### Origin Access Control (OAC)
* **Technical Definition:** A security enhancement that restricts direct access to an Amazon S3 origin, allowing requests only when signed by an authorized CloudFront distribution principal.
* **Why It Matters:** Guarantees that public users cannot bypass CloudFront and WAF security filters by trying to access the raw S3 bucket URL!

### Cache Invalidation
* **Technical Definition:** A command sent to CloudFront to explicitly remove objects from edge caches before their Time-To-Live (TTL) expires.
* **Example:** Submitting `/*` invalidates all cached files worldwide in under 60 seconds after a website deployment.

---

## 10. Infrastructure as Code (IaC) & CloudFormation (Module 3.d)

### Infrastructure as Code (IaC)
* **Technical Definition:** The management and provisioning of IT infrastructure (networks, virtual machines, load balancers, and storage) through human-readable, machine-consumable configuration files rather than manual interactive configuration in web consoles.

### AWS CloudFormation
* **Technical Definition:** Amazon's native declarative service that allows developers to model, provision, and manage AWS and third-party resources using formatted YAML or JSON text templates.

### CloudFormation Stack
* **Technical Definition:** A single management unit representing a collection of AWS resources created, updated, or deleted together by CloudFormation from a single template.

### Change Set
* **Technical Definition:** A preview generated by CloudFormation showing an itemized summary of proposed resource additions, modifications, or destructive replacements before you execute an update on an active stack.

### Drift Detection
* **Technical Definition:** A CloudFormation capability that compares the expected configuration defined in your template against the actual live configuration of resources in your AWS account to identify unapproved, out-of-band console changes.

### Automatic Rollback
* **Technical Definition:** A safety mechanism where, if any single resource in a CloudFormation stack fails to create or update, the engine halts execution and rolls back all previously created resources to maintain a clean, consistent state.

---
*Telangana Academy for Skill and Knowledge (TASK) · Cloud Software Developer Master Glossary*
