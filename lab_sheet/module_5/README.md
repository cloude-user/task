# Module 5: AWS Developer (CLI, SDK, Serverless, Messaging & NoSQL)

**Trainer:** Sundeep Hiremat  
**Center:** TASK Nalgonda  
**Course:** Cloud Software Developer (AWS DVA-C02)

---

## 🛠️ One-Time Environment Setup (No CloudShell Required)

Since AWS CloudShell may not be enabled in your lab account, choose **either** of the two setups below:

### Option A: Windows PowerShell (Your Local Laptop)
1. **Install AWS CLI v2 & `boto3`:**
   ```powershell
   winget install -e --id Amazon.AWSCLI
   pip install boto3
   ```
   *(Close and reopen PowerShell after installation, then verify with `aws --version`)*

2. **Authenticate (`aws configure`):**
   - In AWS Console: **IAM → Users → Security credentials → Create access key (CLI)**.
   - Run `aws configure` in PowerShell and enter your Access Key ID, Secret Access Key, Region (`us-east-1`), and output (`json`).

### Option B: EC2 Instance Connect (Browser Terminal — Best if Lab PCs Block Installs)
1. Launch a free-tier **`t2.micro` Amazon Linux 2023** EC2 instance.
2. Attach an **IAM Role** with `AdministratorAccess` (or S3, Lambda, SQS, SNS, DynamoDB, IAM permissions).
3. Click **Connect → EC2 Instance Connect** to open a Linux Bash terminal in your browser.
4. Install `boto3` once:
   ```bash
   pip3 install boto3
   ```
   *(AWS CLI is already pre-installed on Amazon Linux 2023!)*

---

## 📚 Module 5 Lab Index

| Lab | Topic | Guide Link |
| :--- | :--- | :--- |
| **Module 5.1 (M5-T1)** | AWS CLI, Credential Chain, Python `boto3`, & Lambda X-Ray Tracing | [module_5.1_cli_sdk_xray/README.md](module_5.1_cli_sdk_xray/README.md) |
| **Module 5.2 (M5-T2)** | SQS (Standard, DLQ, FIFO), SNS Fan-out & Filters, DynamoDB Pipeline | [module_5.2_sqs_sns_dynamodb/README.md](module_5.2_sqs_sns_dynamodb/README.md) |
| **Module 5.3 (M5-T3)** | *(Coming next)* | — |
| **Module 5.4 (M5-T4)** | *(Coming next)* | — |
