# Cloud Software Developer — Official Course Syllabus

---

### Module 1: Programming Foundations (Python, JavaScript, Git & GitHub)
* **1.a Python Programming Foundations:**
  * **1.a.1 Setup & Logic:** Installing Python 3.12+, VS Code, terminal basics, and logic decomposition. *(Outcome: Working local developer environment)*
  * **1.a.2 Core Syntax:** Variables, data types, f-strings, conditionals (`if/else`), and loops (`for`/`while`). *(Outcome: Scripting arithmetic and logic flows)*
  * **1.a.3 Collections:** Lists, dictionaries, tuples, sets, indexing, slicing, and methods. *(Outcome: Storing and manipulating structured data)*
  * **1.a.4 Functions & Modules:** Arguments, return values, standard library, and virtual environments (`venv`). *(Outcome: Writing clean, modular Python scripts)*
  * **1.a.5 OOP & File I/O:** Classes, objects, exception handling (`try/except`), file handling, and JSON parsing. *(Outcome: Robust JSON configuration parser with error handling)*
* **1.b Modern JavaScript Foundations:**
  * **1.b.1 JavaScript Core:** Modern ES2024 syntax, `let`/`const`, arrow functions, and template literals. *(Outcome: Writing modern vanilla JavaScript)*
  * **1.b.2 DOM & Events:** Selecting HTML elements, event listeners, and dynamic UI updates. *(Outcome: Interactive web pages responding to clicks)*
  * **1.b.3 Asynchronous JS:** Callbacks, Promises, `async`/`await`, and calling REST APIs via `fetch()`. *(Outcome: Fetching external live JSON data into the browser)*
* **1.c Git & GitHub Version Control:**
  * **1.c.1 Local Git:** Tracking code changes with `git init`, `git status`, `git add`, and `git commit`. *(Outcome: Local repository with committed project history)*
  * **1.c.2 GitHub Workflows:** Account setup, `git remote`, `git push`, branches, and Pull Requests. *(Outcome: Publishing code to GitHub and managing branches)*

---

### Module 2: AWS Certified Cloud Practitioner (Foundations & Core Services)
* **2.a Cloud Foundations & Core Families:**
  * **2.a.1 Cloud Concepts:** Cloud benefits, deployment models (Public/Private/Hybrid), and service models (IaaS/PaaS/SaaS). *(Outcome: Understanding cloud economics and models)*
  * **2.a.2 Global Infrastructure:** Regions, Availability Zones (AZs), and Edge Locations. *(Outcome: Selecting optimal AWS regions for latency and resilience)*
  * **2.a.3 Compute Services:** Amazon EC2 instance overview, Amazon ECS, and Docker container basics. *(Outcome: Navigating EC2 console and container concepts)*
  * **2.a.4 Storage Services:** Amazon S3 storage classes & tiers, EBS block storage, and EFS shared file systems. *(Outcome: Matching workloads to optimal storage tiers)*
  * **2.a.5 Database & In-Memory Cache:** Amazon RDS relational databases, DynamoDB NoSQL, and in-memory cache concepts. *(Outcome: Distinguishing SQL vs. NoSQL cloud databases)*
* **2.b Management, Security & Integration:**
  * **2.b.1 Shared Responsibility Model:** Security **OF** the Cloud (AWS) vs. Security **IN** the Cloud (Customer). *(Outcome: Identifying security boundaries)*
  * **2.b.2 Identity & Access Management (IAM):** IAM users, user groups, JSON policies, and IAM roles. *(Outcome: Creating secure IAM accounts with least-privilege)*
  * **2.b.3 Monitoring & Governance:** Amazon CloudWatch (metrics & alarms) and AWS CloudTrail (audit logs). *(Outcome: Tracking real-time metrics and audit trails)*
  * **2.b.4 Application Integration:** Loose coupling with Amazon SQS (message queues) and Amazon SNS (pub/sub). *(Outcome: Understanding decoupled messaging architecture)*
* **2.c Hands-on Lab & Mini Project:**
  * **2.c.1 Account Setup:** Activating personal AWS Free Tier accounts, setting billing alerts, and MFA security. *(Outcome: Secure, budget-protected active AWS account)*
  * **2.c.2 Mini Project 1:** Hosting a responsive static portfolio website on Amazon EC2 or Amazon S3. *(Outcome: Live portfolio website accessible via public URL)*

---

### Module 3: AWS Associate Core Knowledge (Deep-Dive & Practical Hands-on)
* **3.a Compute Deep-Dive:**
  * **3.a.1 EC2 Advanced & ECS:** EC2 instance families, lifecycle states, Key Pairs, Security Groups, and ECS containers. *(Outcome: Launching and securing EC2 instances)*
* **3.b Storage & Database Deep-Dive:**
  * **3.b.1 S3 & Block Storage:** S3 bucket versioning, SSE-S3 encryption, lifecycle rules, public access blocks, and EBS volumes/snapshots. *(Outcome: Configuring secure multi-tier S3 storage)*
  * **3.b.2 Databases Deep-Dive:** Provisioning Amazon RDS MySQL/PostgreSQL, Multi-AZ failover, Amazon Aurora, and DynamoDB. *(Outcome: Connecting applications to managed cloud databases)*
* **3.c Custom VPC Networking, Security & CDN:**
  * **3.c.1 Custom VPC:** IPv4 CIDR blocks (`10.0.0.0/16`), public and private subnets, and Route Tables. *(Outcome: Architecting an isolated multi-tier VPC from scratch)*
  * **3.c.2 Gateways & NAT:** Internet Gateway (IGW) 1:1 NAT and NAT Gateway outbound egress for private subnets. *(Outcome: Enabling outbound-only internet for database instances)*
  * **3.c.3 Web Security & CDN:** AWS WAF (Web ACLs, SQLi/XSS filters) and Amazon CloudFront (CDN edge caching, origins, and TTL). *(Outcome: Securing and accelerating web apps)*
* **3.d Infrastructure as Code (IaC):**
  * **3.d.1 AWS CloudFormation:** Declarative YAML templates, parameters, resources, outputs, and stack lifecycle. *(Outcome: Automated deployment of S3 and VPC via YAML)*

---

### Module 4: AWS Solutions Architect
* **4.1 Architecture Design Principles & Well-Architected Framework:**
  * **4.1a Theory:** The 6 core pillars of the AWS Well-Architected Framework.
  * **4.1b LabSheet:** Implementing cost alarms with AWS Budgets and validating permissions via IAM Policy Simulator.
* **4.2 Networking Essentials: Route 53 & Advanced VPC:**
  * **4.2a Theory:** Amazon Route 53 DNS routing policies (Simple, Weighted, Failover) and Advanced VPC topologies.
  * **4.2b LabSheet:** Multi-VPC peering, Route 53 private hosted zones, and NAT Gateway.
* **4.3 Load Balancing (ELB / ALB / NLB):**
  * **4.3a Theory:** Elastic Load Balancing: Application Load Balancer (ALB) vs. Network Load Balancer (NLB).
  * **4.3b LabSheet:** Deploying ALB, Target Groups, path-based routing (`/api`), and health check thresholds.
* **4.4 Auto Scaling & ElastiCache:**
  * **4.4a Theory:** High availability with EC2 Auto Scaling Groups (ASG) and in-memory caching with Redis/Valkey.
* **4.5 Data Security, Encryption & Serverless:**
  * **4.5a Theory:** Data encryption at rest/in-transit, AWS KMS customer managed keys, and serverless architectures.
  * **4.5b LabSheet:** AWS KMS key rotation, S3 SSE-KMS, Secrets Manager, and DynamoDB + Lambda HTTP API.

---

### Module 5: AWS Developer
* **5.1 AWS SDK & Developer Tooling:**
  * **5.1a Theory:** Cloud-native developer environments, AWS Cloud9 cloud IDE, and AWS X-Ray distributed tracing.
  * **5.1b LabSheet:** Developing with Python AWS SDK (`boto3`) and instrumenting microservices with AWS X-Ray.
* **5.2 Application Integration: SQS, SNS & DynamoDB:**
  * **5.2a Theory:** Microservice decoupling, asynchronous messaging with SQS queues, and SNS pub/sub.
  * **5.2b LabSheet:** Decoupled event-driven messaging pipeline using SNS fan-out to SQS queues.
* **5.3 DynamoDB & ElastiCache Programming:**
  * **5.3a Theory:** NoSQL data modeling, partition/sort keys, secondary indexes (GSIs), and cache-aside patterns.
  * **5.3b LabSheet:** Programmatic CRUD operations in DynamoDB using SDK and accelerating reads with ElastiCache.
* **5.4 Serverless Development: AWS Lambda:**
  * **5.4a Theory:** Event-driven compute architecture, execution lifecycle, triggers, and IAM execution roles with AWS Lambda.

---

### Module 6: AWS SysOps Administrator
* **6.1 Operations Essentials: CloudTrail, CloudWatch & Recovery:**
  * **6.1a Theory:** Centralized audit logging with CloudTrail, CloudWatch dashboards/alarms, and AWS Backup policies.
  * **6.1b LabSheet:** Configuring centralized CloudWatch metric alarms, automated SNS alerts, and AWS Backup plans.
* **6.2 EC2 Auto Scaling, Load Balancer & Cache Operations:**
  * **6.2a Theory:** Fleet health monitoring, tracking unhealthy targets, and cache hit/miss operational metrics.
  * **6.2b LabSheet:** Troubleshooting unhealthy target groups, analyzing ELB access logs, and cache tuning.
* **6.3 Security Operations: Encryption, KMS & API Gateway:**
  * **6.3a Theory:** Compliance auditing, AWS KMS key policies, and API Gateway security.
  * **6.3b LabSheet:** Securing API Gateway endpoints with IAM authorization and throttling limits.
* **6.4 Monitoring & Troubleshooting (EC2, ELB, RDS, Lambda):**
  * **6.4a Theory:** Systematic fault diagnosis across EC2, ELB, RDS, and Lambda.
  * **6.4b LabSheet:** Diagnosing broken architectures, analyzing VPC Flow Logs, and resolving production error codes.

---

### Module 7: AWS AI Practitioner (Theory Essentials)
* **7.1 Overview of AI on AWS:** Core concepts of Artificial Intelligence, Machine Learning, and Foundation Models on AWS infrastructure.
* **7.2 Amazon Bedrock & Generative AI:** Managed foundation models, prompt engineering fundamentals, and cloud AI services.
* **7.3 Responsible AI & Security:** Data privacy, safety guardrails, PII protection, and ethical AI compliance on AWS.
* **7.4 Vector Embeddings & RAG:** High-dimensional vector embeddings, semantic search concepts, and Retrieval-Augmented Generation (RAG).
