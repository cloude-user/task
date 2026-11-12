# TASK Telangana · Cloud Software Developer

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![AWS](https://img.shields.io/badge/AWS-Cloud%20Developer%20(DVA--C02)-orange?logo=amazon-aws)
![Git](https://img.shields.io/badge/Version%20Control-Git%20%26%20GitHub-red?logo=git)
![Center](https://img.shields.io/badge/Center-Nalgonda-brightgreen)

Welcome to the official repository for the **Cloud Software Developer** training program conducted by **TASK (Telangana Academy for Skill and Knowledge)** at the **Nalgonda Center**.

- **Trainer:** Sundeep Hiremath
- **Program:** Cloud Software Developer (AWS EC2-Centric / DVA-C02 Alignment)
- **Target Audience:** Engineering Students & Aspiring Cloud Engineers across Nalgonda colleges

---

## 🚀 Repository Overview

This repository hosts hands-on Jupyter notebooks, source code, cloud architecture labs, and reference guides covering:
1. **Core Python for Cloud Automation:** Syntax, Data Structures, Functional Programming, and JSON manipulation.
2. **AWS Cloud Foundations:** Global Infrastructure (Regions, AZs, Edge Locations), IAM, EC2, S3, RDS, DynamoDB, VPC, and Serverless.
3. **AWS SDK (`boto3`) & CLI:** Programmatic AWS management, automated resource provisioning, and cloud monitoring.
4. **Git & GitHub Version Control:** Professional developer workflows, Conventional Commits, branch strategies, and pull requests.

---

## 📂 Repository Structure

```
task/
├── .gitignore                      # Cloud & Python security shield
├── .env.example                    # Sample environment variables template
├── README.md                       # Project documentation & course map
├── GIT_CHEAT_SHEET.md              # Quick reference for Git & GitHub workflows
├── STUDENT_GIT_COMMANDS.md         # Live classroom demonstration playbook
│
├── notes/                          # Master PDF Handbooks & Guides
│   ├── Day_01_Python_Master_Handbook.pdf
│   └── Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf
│
├── module_basic/                   # Core Python & Cloud Fundamentals (formerly day-01)
│   └── notebooks/
│       ├── 01_hello_python_and_basics.ipynb
│       ├── 02_variables_numbers_and_memory.ipynb
│       ├── 03_strings_and_cloud_formatting.ipynb
│       ├── 04_lists_tuples_and_dictionaries.ipynb
│       ├── 05_decisions_loops_and_cloud_functions.ipynb
│       ├── 06_aws_cloud_foundations_and_budget_shield.ipynb
│       ├── 07_functions_exception_handling.ipynb
│       └── 08_class_objects.ipynb
│
└── module_03_aws_core/             # AWS Core Services (Compute, Storage & Networking)
    ├── MODULE_03_AWS_CORE_STUDENT_NOTES.md
    ├── presentation/
    │   └── Module_03_AWS_Core_Services_Masterclass.pptx
    ├── notes/
    │   └── Module_03_AWS_Core_Services_Vehicle_Analogy_Guide.pdf
    └── lab_guides/
        ├── 01_ec2_launch_and_lifecycle_lab.md
        ├── 02_storage_ebs_efs_s3_lab.md
        └── 03_vpc_networking_and_security_lab.md
```

---

## 📅 Curriculum & Lab Roadmap

### **Module Basic: Python & Cloud Foundations**
- **Python Core:** Variables, data structures, strings, loops, functions, OOP, and exception handling.
- **AWS Foundations:** Global Infrastructure, Regions, AZs, Shared Responsibility Model, IAM.

### **Module 03: AWS Core Services & Infrastructure (Vehicle Metaphor)**
- **EC2 Compute (The Engine):** AMIs, instance types, Key Pairs, Security Groups, User Data automation, Custom AMIs (Golden Images), and Lifecycle billing.
- **Storage Triad (The Storage Shootout):**
  - **EBS (The Personal Trunk):** Block storage, gp3/io2, attachments, formatting, and snapshots.
  - **EFS (The Shared Fleet Cargo):** Regional multi-mount NFSv4 file sharing across 100+ EC2s.
  - **S3 (The Global Shipping Warehouse):** Buckets, objects, 11 9's durability, Block Public Access, and HTTPS bucket policies.
- **VPC Networking (The Gated Industrial Highway):** CIDR blocks (`10.0.0.0/16`), Public Subnets, Private Subnets, Route Tables, Internet Gateways (IGW), NAT Gateways, Stateful Security Groups vs Stateless NACLs, and 3-Tier Enterprise Web Architecture.
- **Python Core:**
  - Setup & installation, Python interactive shell and scripts.
  - Variables, memory addresses (`id()`), type systems, and immutable vs. mutable types.
  - String manipulation, f-strings, JSON string formatting for cloud logs.
  - Collections: Lists, Tuples, Dictionaries, and Sets for resource inventory management.
  - Control flow: `if/elif/else`, `for/while` loops, list comprehensions, and cloud utility functions.
- **AWS Cloud Foundations (Section 1):**
  - Cloud service models: IaaS vs. PaaS vs. SaaS.
  - AWS Global Infrastructure: Regions, Availability Zones (AZs), and Edge Locations.
  - Shared Responsibility Model (Security *of* the cloud vs. Security *in* the cloud).
  - AWS Management Console walkthrough & AWS Free Tier Zero-Dollar Budget Shield.
  - IAM Essentials: Users, Groups, Roles, Policies, STS, and Least Privilege principle.

---

## 🛠️ Getting Started

### 1. Prerequisites
- **Python 3.10+**: [python.org](https://www.python.org/)
- **Git**: [git-scm.com](https://git-scm.com/)
- **AWS CLI v2**: [docs.aws.amazon.com/cli](https://docs.aws.amazon.com/cli/)
- **VS Code** with Jupyter Extension

### 2. Clone Repository
```bash
git clone https://github.com/cloude-user/task.git
cd task
```

### 3. Setup Virtual Environment
```bash
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Linux / macOS:
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install jupyter boto3 python-dotenv requests
```

### 5. Launch Notebooks
```bash
jupyter lab
# or launch directly in VS Code
```

---

## 🛡️ Git & GitHub Standards

This repository follows industry standards outlined in [GIT_CHEAT_SHEET.md](GIT_CHEAT_SHEET.md):

1. **Security First:** Never commit `.env` files, `.pem` keypairs, or AWS access keys.
2. **Conventional Commits:** Write clean, descriptive commit messages:
   - `feat(scope): new capability or notebook`
   - `fix(scope): bug resolution`
   - `docs(scope): documentation or diagram update`
3. **Branching Strategy:** Work on feature branches (`feature/topic-name`) and merge into `main` via pull requests.

---

## 👨‍🏫 Trainer & Contact

**Sundeep Hiremath**  
*Corporate Trainer & Technical Lead*  
*Cloud & AI Software Development*  
TASK (Telangana Academy for Skill and Knowledge) Training Program
