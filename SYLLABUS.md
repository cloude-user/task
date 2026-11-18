# Telangana Academy for Skill and Knowledge (TASK)
## Cloud Software Developer — Official Course Syllabus
> **Center:** TASK Nalgonda Training Center  
> **Trainer:** Sundeep Hiremat  
> **Target Audience:** Engineering & Degree Students (UG & PG)  
> **Skill Track:** Cloud Computing, AWS Cloud Architecture, Full-Stack Scripting & Generative AI  

---

## 🎯 Course Overview & Career Path
This curriculum prepares students for modern cloud engineering roles. Starting with programming foundations in **Python**, **JavaScript**, and **Git**, students progress through **AWS Cloud Foundations**, **Hands-on Cloud Architecture**, **Solutions Architecture**, **Developer & Serverless Engineering**, **SysOps Cloud Administration**, and **Generative AI on AWS**.

---

## 📚 Detailed Module Breakdown

### Module 1: Programming Foundations (Python, JavaScript, Git & GitHub)
*Building essential developer logic, scripting skills, and version control workflows.*

* **1.a Python Programming Foundations:**
  * **Developer Setup & Problem Solving:** Installing Python 3.12+, VS Code, terminal basics, and computational thinking.
  * **Python Core Syntax:** Variables, data types, numbers, strings, f-strings, conditionals (`if/elif/else`), and loops (`for`/`while`).
  * **Collections & Data Structures:** Working with lists, dictionaries, tuples, sets, and essential methods.
  * **Functions & Modular Code:** Defining functions, arguments, return values, standard library modules, and virtual environments (`venv`).
  * **OOP & File I/O:** Classes, objects, methods, error handling (`try/except/finally`), file reading/writing, and JSON processing.
* **1.b Modern JavaScript Foundations:**
  * **JavaScript Basics:** ES2024 syntax, `let`/`const`, data types, arrow functions, and template strings.
  * **DOM & Browser Interactions:** Selecting elements, handling clicks/events, and manipulating HTML dynamically.
  * **Asynchronous JavaScript:** Callbacks, Promises, `async/await`, and calling REST APIs using the `fetch()` API.
* **1.c Git & GitHub Version Control:**
  * **Local Version Control:** Tracking code changes with `git init`, `git status`, `git add`, and `git commit`.
  * **Remote Repositories:** Setting up GitHub accounts, linking remote repositories, `git push`, and `git clone`.
  * **Collaborative Workflows:** Creating feature branches, merging code, opening Pull Requests (PRs), and code reviews.

---

### Module 2: AWS Certified Cloud Practitioner (Foundations & Core Services)
*Understanding global cloud concepts, core AWS service families, and cloud security.*

* **2.a Cloud Foundations & Core Service Families:**
  * **Cloud Computing Fundamentals:** Cloud benefits, deployment models (Public, Private, Hybrid), and service models (IaaS, PaaS, SaaS).
  * **AWS Global Infrastructure:** Regions, Availability Zones (AZs), and Edge Locations.
  * **Compute Services:** Amazon EC2 instance overview, Amazon ECS, and container basics.
  * **Storage Services:** Amazon S3 storage classes and tiers, EBS block storage, and EFS shared network file systems.
  * **Database & In-Memory Cache:** Amazon RDS relational databases, DynamoDB NoSQL, and in-memory caching overview.
* **2.b Management, Governance, Security & Integration:**
  * **Security & Compliance:** AWS Shared Responsibility Model (Security OF the Cloud vs. Security IN the Cloud).
  * **Identity & Access Management (IAM):** Creating IAM users, groups, customer managed policies, and IAM roles.
  * **Monitoring & Governance:** Amazon CloudWatch (metrics, dashboards, alarms) and AWS CloudTrail (governance and audit logs).
  * **Application Integration:** Loose coupling using Amazon SQS (message queues) and Amazon SNS (pub/sub notifications).
  * **Cloud Analytics & Insights:** Introduction to AWS analytics services and cloud cost management.
* **2.c Hands-on Lab & Mini Project:**
  * **Account Setup:** Activating personal AWS Free Tier accounts, setting billing alerts, and MFA security.
  * **Mini Project 1:** Deploying and hosting a responsive static portfolio website on an Amazon EC2 Linux instance.

---

### Module 3: AWS Associate Core Knowledge (Deep-Dive & Practical Hands-on)
*Hands-on architecture implementation, VPC networking, web security, and automation.*

* **3.a Compute Deep-Dive:**
  * **EC2 Advanced Operations:** Instance lifecycle, instance families (General, Compute, Memory), Key Pairs, and User Data bootstrap scripts.
  * **Custom AMIs:** Capturing custom Amazon Machine Images from running instances for fast replication.
  * **Security Groups:** Stateful firewall rules, port configuration, and best practices.
  * **Containers on AWS:** Deploying Docker containerized apps on Amazon ECS.
* **3.b Storage & Database Deep-Dive:**
  * **Amazon S3 Hands-on:** Bucket creation, object versioning, server-side encryption (SSE-S3), lifecycle rules, and public access blocks.
  * **Block & File Storage:** Provisioning EBS volumes, snapshots, volume expansion, and mounting EFS file systems.
  * **Managed Databases:** Provisioning Amazon RDS (MySQL/PostgreSQL), Multi-AZ deployments, Amazon Aurora clusters, and DynamoDB tables.
* **3.c VPC Networking, Security & Content Delivery:**
  * **Custom VPC Architecture:** IPv4 CIDR blocks (`10.0.0.0/16`), public and private subnets, and custom Route Tables.
  * **Gateways & Egress:** Internet Gateway (IGW) for public routing and NAT Gateway for secure outbound internet for private databases.
  * **AWS WAF (Web Application Firewall):** Protecting applications against common web exploits, SQL injection, and Cross-Site Scripting (XSS).
  * **Amazon CloudFront (CDN):** Global content delivery, CDN origins, cache behaviors, Time-To-Live (TTL), and cache invalidations.
* **3.d Infrastructure as Code (IaC):**
  * **AWS CloudFormation:** Declarative YAML templates, parameters, resources, outputs, change sets, and automated stack deployment.

---

### Module 4: AWS Solutions Architect
*Designing highly available, cost-optimized, and resilient distributed cloud architectures.*

* **4.1 Architecture Design Principles & Well-Architected Framework:**
  * **Theory (4.1a):** The 6 pillars of the AWS Well-Architected Framework (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability).
  * **LabSheet (4.1b):** Implementing budget cost alarms with AWS Budgets and validating IAM policies using IAM Policy Simulator.
* **4.2 Networking Essentials: Route 53 & Advanced VPC:**
  * **Theory (4.2a):** Amazon Route 53 DNS routing policies (Simple, Weighted, Latency, Failover) and Advanced VPC topologies.
  * **LabSheet (4.2b):** Multi-VPC peering, Route 53 private hosted zones (`cci.internal`), NAT Gateway, VPC endpoints, and Reachability Analyzer.
* **4.3 Load Balancing (ELB / ALB / NLB):**
  * **Theory (4.3a):** Elastic Load Balancing architecture: Application Load Balancer (Layer 7) vs. Network Load Balancer (Layer 4).
  * **LabSheet (4.3b):** Configuring an Application Load Balancer (ALB), Target Groups, path-based routing (`/api`), and health check thresholds.
* **4.4 Auto Scaling & ElastiCache:**
  * **Theory (4.4a):** Horizontal elasticity with EC2 Auto Scaling Groups (ASG) and in-memory caching with Redis/Valkey.
  * **LabSheet (4.4b):** Creating Launch Templates, Auto Scaling dynamic policies, and setting up an in-memory Valkey/Redis cache cluster.
* **4.5 Data Security, Encryption & Serverless Architectures:**
  * **Theory (4.5a):** Data encryption at rest and in transit, AWS KMS customer managed keys, and serverless architectural patterns.
  * **LabSheet (4.5b):** AWS KMS key rotation, S3 SSE-KMS encryption, AWS Secrets Manager, and building a serverless DynamoDB + Lambda HTTP API.

---

### Module 5: AWS Developer
*Developing cloud-native applications, SDK programming, event messaging, and serverless workflows.*

* **5.1 AWS SDK & Developer Tooling:**
  * **Theory (5.1a):** Cloud-native developer environments, AWS Cloud9 IDE, AWS CLI v2, and distributed tracing with AWS X-Ray.
  * **LabSheet (5.1b):** Writing Python scripts with the AWS SDK (`boto3`), configuring SigV4 authentication, and tracing latency bottlenecks in X-Ray.
* **5.2 Application Integration: SQS, SNS & DynamoDB:**
  * **Theory (5.2a):** Microservice decoupling, asynchronous messaging with Amazon SQS queues, and pub/sub broadcast with Amazon SNS.
  * **LabSheet (5.2b):** Building an event-driven decoupled architecture: SNS fan-out pattern to SQS queues and event logging in DynamoDB.
* **5.3 DynamoDB & ElastiCache Programming:**
  * **Theory (5.3a):** NoSQL data modeling, partition keys, sort keys, secondary indexes (GSI/LSI), and cache-aside design patterns.
  * **LabSheet (5.3b):** Writing programmatic CRUD operations in DynamoDB using SDK and accelerating query reads with ElastiCache.
* **5.4 Serverless Development: Lambda, Step Functions & CI/CD:**
  * **Theory (5.4a):** Event-driven compute with AWS Lambda, visual multi-step workflows with AWS Step Functions, and AWS SAM templates.
  * **LabSheet (5.4b):** Building, testing, and deploying serverless microservices with automated GitHub Actions CI/CD pipelines.

---

### Module 6: AWS SysOps Administrator
*Operational monitoring, high availability management, security governance, and system troubleshooting.*

* **6.1 Operations Essentials: CloudTrail, CloudWatch & Recovery:**
  * **Theory (6.1a):** Centralized log aggregation, real-time metrics, CloudWatch alarms, Route 53 DNS health checks, and AWS Backup policies.
  * **LabSheet (6.1b):** Setting up automated CloudWatch metric alarms, incident notification topics in SNS, and snapshot backup plans.
* **6.2 EC2 Auto Scaling, Load Balancer & Cache Operations:**
  * **Theory (6.2a):** Fleet management, tracking unhealthy instances, load balancer capacity management, and cache hit/miss operational metrics.
  * **LabSheet (6.2b):** Troubleshooting unhealthy target groups, analyzing ELB access logs, and adjusting Auto Scaling cooldown timers.
* **6.3 Security Operations: Encryption, KMS, Cognito & API Gateway:**
  * **Theory (6.3a):** Compliance auditing, AWS KMS key policies, user authentication with Amazon Cognito, and API Gateway authorization.
  * **LabSheet (6.3b):** Securing REST endpoints with Amazon Cognito User Pools, JWT token validation, and API Gateway throttling limits.
* **6.4 Monitoring & Troubleshooting (EC2, ELB, RDS, Lambda):**
  * **Theory (6.4a):** Systematic troubleshooting methodologies, AWS Health Dashboard, CloudWatch Logs Insights, and VPC Flow Logs.
  * **LabSheet (6.4b):** Triage and resolve real-world broken infrastructure scenarios (EC2 connection timeouts, RDS storage exhaustion, Lambda memory errors).

---

### Module 7: AWS AI Practitioner
*Harnessing artificial intelligence, machine learning, and Generative AI on AWS.*

* **7.1 Introduction to AI on AWS: Infrastructure & Technology:**
  * **Theory (7.1a):** Overview of AI, Machine Learning (ML), and Deep Learning (DL) infrastructure on AWS, Amazon SageMaker, and specialized chips (Trainium & Inferentia).
  * **LabSheet (7.1b):** Exploring foundation models in the Amazon Bedrock console, testing text and image generation.
* **7.2 AI Use Cases, ML Lifecycle & Generative AI Optimization:**
  * **Theory (7.2a):** Business use cases of AI, the Machine Learning development lifecycle (prepare, train, tune, deploy), and prompt engineering techniques.
  * **LabSheet (7.2b):** Building a prompt-engineered AI assistant using Amazon Bedrock foundation models with streaming responses.
* **7.3 Responsible AI: Security, Compliance & Governance:**
  * **Theory (7.3a):** Principles of responsible AI, detecting model bias, data privacy, toxicity filtering, PII masking, and regulatory compliance.
  * **LabSheet (7.3b):** Implementing Amazon Bedrock Guardrails to block prohibited topics, filter toxic inputs, and redact sensitive personal information.
* **7.4 Vector Databases, Embeddings & RAG:**
  * **Theory (7.4a):** High-dimensional vector embeddings, semantic search, vector databases (OpenSearch Serverless, Aurora pgvector), and Retrieval-Augmented Generation (RAG).
  * **LabSheet (7.4b):** Building an enterprise Knowledge Base on Amazon Bedrock to chat with internal business documents using RAG.

---

## 🏆 Capstone Project & Placement Preparation
* **Comprehensive Capstone Project:** Full-stack cloud deployment integrating React/HTML frontend hosted on S3/CloudFront, Application Load Balancer with EC2 Auto Scaling, secure database layer, KMS encryption, and CI/CD automation.
* **Certification & Interview Readiness:** Mock quizzes aligned with **AWS Certified Cloud Practitioner (CLF-C02)** and **AWS Certified Developer Associate (DVA-C02)**, technical resume review, and GitHub portfolio showcase.

---
*Created for TASK Telangana Cloud Software Developer Batch · Nalgonda Training Center*
