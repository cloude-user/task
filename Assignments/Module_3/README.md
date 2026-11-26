# AWS Assignment 1: Shared Notes API on ECS with EFS

**Author:** Sundeep Hiremat  
**Course:** Cloud Software Developer  
**Module:** Module 03 — Compute, Storage & Containers  
**Services Covered:** Amazon Elastic Container Registry (ECR), Amazon Elastic Container Service (ECS), Amazon Elastic File System (EFS), Amazon Elastic Compute Cloud (EC2), Default VPC & Security Groups

---

## 📌 Executive Summary & Architecture

The objective of this assignment is to build a containerized Node.js (Express) REST API deployed on **AWS ECS (Fargate)** and backed by **Amazon EFS (Elastic File System)** as persistent shared POSIX storage.

To prove that Amazon EFS functions as a distributed shared file system:
1. **ECS Task 1 (Add):** Receives HTTP `POST /notes` requests and writes notes as files directly into `/mnt/efs/notes/`.
2. **ECS Task 2 (Fetch):** Receives HTTP `GET /notes` requests and immediately reads all note files saved by Task 1 from the shared `/mnt/efs/notes/` directory.
3. **EC2 Linux Instance:** Mounted to the identical EFS file system via NFS (`amazon-efs-utils`), inspecting and reading the note files directly via standard terminal commands (`ls` and `cat`).

### Architecture Diagram
![Architecture Overview](images/01_architecture_overview.svg)

---

## 🚀 API Specification

| HTTP Method | Endpoint | Description | Storage Behavior |
| :--- | :--- | :--- | :--- |
| **POST** | `/notes` | Creates and saves a new text note | Writes a `.txt` file into `/mnt/efs/notes/` |
| **GET** | `/notes` | Reads all stored note files | Lists and reads all `.txt` files from `/mnt/efs/notes/` |
| **GET** | `/health` | Service health check | Returns `{ "status": "OK" }` |

*Rules Enforced:*
- No SQL or NoSQL database. No in-memory cache.
- Notes are persisted strictly as filesystem artifacts on `/mnt/efs/notes/`.
- Startup logic automatically ensures `/mnt/efs/notes/` exists (`fs.mkdirSync(..., { recursive: true })`).

---

## 🛠️ Complete Student Setup & Implementation Guide

> [!TIP]
> **Use Default VPC & Default Subnets:**  
> All steps in this lab use your AWS account's **Default VPC** and its **Default Subnets** (which are public subnets). There is no need to create a custom VPC.

---

### Step 1: Set Up Docker Build Environment

If Docker is not installed or locked on your local Windows PC, launch a free-tier EC2 instance to act as your **Docker Build Host**:

1. **Launch EC2 Instance:**
   - **Name:** `docker-builder`
   - **AMI:** Amazon Linux 2023 (Free Tier eligible)
   - **Instance Type:** `t2.micro` or `t3.micro`
   - **Key Pair:** *Proceed without a key pair* (we will connect via browser)
   - **VPC / Subnet:** Default VPC (any default subnet)
   - **IAM Role (Recommended):** Under *Advanced details* → *IAM instance profile*, select an IAM role with ECR permissions (`AmazonEC2ContainerRegistryPowerUser`). If you don't have one yet, you can attach it later in Step 3.
2. **Connect via Browser:**
   - Select the instance → Click **Connect** → Choose **EC2 Instance Connect** → Click **Connect**.
3. **Install and Start Docker (Run once in EC2 terminal):**
   ```bash
   sudo dnf update -y
   sudo dnf install -y docker
   sudo systemctl enable --now docker
   sudo usermod -aG docker ec2-user
   newgrp docker
   ```

---

### Step 2: Create Application Code & Dockerfile

Paste this entire block into your terminal to create the directory `shared-notes-api` and all required source files:

```bash
mkdir -p ~/shared-notes-api && cd ~/shared-notes-api

# 1. Create package.json
cat << 'EOF' > package.json
{
  "name": "shared-notes-api",
  "version": "1.0.0",
  "description": "Shared Notes API using Express on ECS mounted to EFS",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "express": "^4.19.2"
  }
}
EOF

# 2. Create server.js
cat << 'EOF' > server.js
const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;
const NOTES_DIR = process.env.NOTES_DIR || '/mnt/efs/notes';

app.use(express.json());

// Ensure directory exists at startup
if (!fs.existsSync(NOTES_DIR)) {
  fs.mkdirSync(NOTES_DIR, { recursive: true });
}

app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

app.post('/notes', (req, res) => {
  const { title, note } = req.body;
  if (!note) {
    return res.status(400).json({ error: 'Note content is required' });
  }
  const safeTitle = (title || 'note').replace(/[^a-zA-Z0-9_-]/g, '_');
  const filename = `${safeTitle}_${Date.now()}.txt`;
  fs.writeFileSync(path.join(NOTES_DIR, filename), note, 'utf8');
  res.status(201).json({ message: 'Saved to EFS', filename });
});

app.get('/notes', (req, res) => {
  if (!fs.existsSync(NOTES_DIR)) {
    return res.json({ total: 0, notes: [] });
  }
  const files = fs.readdirSync(NOTES_DIR).filter(f => f.endsWith('.txt'));
  const notes = files.map(file => ({
    filename: file,
    content: fs.readFileSync(path.join(NOTES_DIR, file), 'utf8')
  }));
  res.json({ total: notes.length, notes });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Shared Notes API server running on port ${PORT}`);
});
EOF

# 3. Create Dockerfile
cat << 'EOF' > Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY server.js ./
RUN mkdir -p /mnt/efs/notes
EXPOSE 3000
ENV PORT=3000
ENV NOTES_DIR=/mnt/efs/notes
CMD ["node", "server.js"]
EOF

echo "Application files created:"
ls -la
```

---

### Step 3: Build Docker Image and Push to Amazon ECR

#### Authentication: Do you need `aws configure`?
> [!IMPORTANT]
> **No hardcoded credentials needed! (AWS Best Practice)**  
> Rather than typing long-term Access Keys into `aws configure`, attach an **IAM Role** to your EC2 instance. The AWS CLI inside EC2 will authenticate automatically without storing any keys on disk.

##### Method A: Attach an IAM Role (Recommended — Zero Credentials to type)
1. In AWS Console, go to **IAM** → **Roles** → **Create role**.
2. Select **AWS service** → Use case: **EC2** → Click **Next**.
3. Under permissions policies, search and select **`AmazonEC2ContainerRegistryPowerUser`** (or `AdministratorAccess`).
4. Name the role **`EC2-ECR-Role`** and click **Create role**.
5. In **EC2 Console**, select your `docker-builder` instance → **Actions** → **Security** → **Modify IAM role** → Select **`EC2-ECR-Role`** → Click **Update IAM role**.
6. **Done!** You do not need to run `aws configure`. Proceed straight to the commands below.

##### Method B: Alternative (Using `aws configure`)
If you prefer using an IAM User's access keys instead of an IAM Role:
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and Default region (e.g. us-east-1)
```

---

#### Run the Build and Push Script (Copy-Paste)

Run this block directly in your EC2 terminal:

```bash
# Set target region (e.g. us-east-1 or ap-south-1)
export AWS_REGION="us-east-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_NAME="shared-notes-api"

# 1. Create ECR repository (if not already created)
aws ecr create-repository --repository-name $REPO_NAME --region $AWS_REGION 2>/dev/null || echo "Repo exists"

# 2. Build Docker container image
docker build -t $REPO_NAME .

# 3. Authenticate Docker with Amazon ECR (Uses attached IAM Role automatically!)
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# 4. Tag image with ECR URI
docker tag ${REPO_NAME}:latest ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPO_NAME}:latest

# 5. Push image to Amazon ECR
docker push ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPO_NAME}:latest

echo "============================================================"
echo "SUCCESS! YOUR ECR IMAGE URI IS:"
echo "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPO_NAME}:latest"
echo "============================================================"
```

---

### Step 4: Configure Security Groups in Default VPC

Create **two Security Groups** in your Default VPC via AWS Console:

#### 1. Security Group for ECS Tasks (`sg-ecs-tasks`):
- **VPC:** Default VPC
- **Inbound Rules:**
  - Type: **Custom TCP**, Port: `3000`, Source: `0.0.0.0/0` (Anywhere-IPv4)
- **Outbound Rules:**
  - All traffic (`0.0.0.0/0`)

#### 2. Security Group for EFS (`sg-efs-nfs`):
- **VPC:** Default VPC
- **Inbound Rules:**
  - Type: **NFS**, Port: `2049`, Source: Choose `sg-ecs-tasks` (or Default VPC CIDR `172.31.0.0/16`)
- **Outbound Rules:**
  - All traffic (`0.0.0.0/0`)

---

### Step 5: Create Amazon EFS File System

1. In AWS Console, go to **EFS** → Click **Create file system**.
2. **Name:** `shared-notes-efs`
3. **VPC:** Select **Default VPC**.
4. Click **Customize**:
   - Performance settings: **General Purpose**, Throughput: **Bursting**.
   - Under **Network (Mount Targets)**:
     - For each Availability Zone subnet, select security group `sg-efs-nfs` (remove default security group).
5. Click **Create**.
6. Note down your **File System ID** (e.g. `fs-0498a12bc`).

---

### Step 6: Create ECS Task Definition & Run 2 Tasks

#### A. Ensure ECS Task Execution Role Exists
> [!IMPORTANT]
> **Fargate Execution Role Required for Private ECR:**  
> When using AWS Fargate with container images stored in private Amazon ECR, Fargate requires an **Execution Role (`executionRoleArn`)** with `AmazonECSTaskExecutionRolePolicy` to authenticate and pull your image during task startup. Without it, ECS throws:  
> `Fargate requires task definition to have execution role ARN to support ECR images.`

You can verify and create this role with a single command on your EC2 build host:
```bash
# Create the ecsTaskExecutionRole (if it doesn't already exist)
aws iam create-role \
  --role-name ecsTaskExecutionRole \
  --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ecs-tasks.amazonaws.com"},"Action":"sts:AssumeRole"}]}' 2>/dev/null || echo "Role already exists"

# Attach the required AWS managed policy
aws iam attach-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```
*(Or in AWS Console: IAM → Roles → Create role → AWS Service: **Elastic Container Service** → Use case: **Elastic Container Service Task** → Attach **`AmazonECSTaskExecutionRolePolicy`** → Name: **`ecsTaskExecutionRole`**).*

---

#### B. Create Task Definition with JSON
1. Go to **ECS Console** → **Task definitions** → **Create new task definition with JSON**.
2. Replace `<AWS_ACCOUNT_ID>`, `<AWS_REGION>`, and `<EFS_FS_ID>`:

```json
{
  "family": "shared-notes-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::<AWS_ACCOUNT_ID>:role/ecsTaskExecutionRole",
  "volumes": [
    {
      "name": "efs-notes-volume",
      "efsVolumeConfiguration": {
        "fileSystemId": "<EFS_FS_ID>",
        "transitEncryption": "ENABLED",
        "rootDirectory": "/"
      }
    }
  ],
  "containerDefinitions": [
    {
      "name": "shared-notes-api",
      "image": "<AWS_ACCOUNT_ID>.dkr.ecr.<AWS_REGION>.amazonaws.com/shared-notes-api:latest",
      "portMappings": [{ "containerPort": 3000, "protocol": "tcp" }],
      "mountPoints": [
        {
          "sourceVolume": "efs-notes-volume",
          "containerPath": "/mnt/efs",
          "readOnly": false
        }
      ]
    }
  ]
}
```

---

#### C. Run 2 Independent Standalone Tasks on ECS Fargate
1. Go to your ECS Cluster → **Tasks** tab → **Run new task**.
2. **Launch type:** FARGATE.
3. **Task definition:** `shared-notes-task`.
4. **Number of tasks:** `2`.
5. **VPC:** Default VPC.
6. **Subnets:** Select Default Subnets.
7. **Security Group:** Select `sg-ecs-tasks`.
8. ⚠️ **CRITICAL SETTING:** **Public IP = `ENABLED`** (Turned ON).

#### Verification Screenshot: Both Tasks Running
Once started, note the public IPv4 addresses for **Task 1** and **Task 2**:
![Both ECS Tasks Running](images/03_ecs_tasks_running.svg)

---

### Step 7: Mount EFS on EC2 Linux Instance

Connect to your EC2 instance (`docker-builder` or a fresh Amazon Linux 2023 instance) in the default VPC:

```bash
# 1. Install Amazon EFS client utilities
sudo dnf install -y amazon-efs-utils

# 2. Create mount directory
sudo mkdir -p /mnt/efs

# 3. Mount EFS via TLS (replace fs-0498a12bc with your EFS File System ID)
sudo mount -t efs -o tls fs-0498a12bc:/ /mnt/efs

# 4. Verify mount
df -h | grep efs
```

---

### Step 8: Complete Verification Proof

#### Test A: Postman Verification (Recommended)

##### 1. POST Request — Save Note via Task 1
- **Method:** `POST`
- **URL:** `http://<TASK_1_PUBLIC_IP>:3000/notes`
- **Headers:**
  - `Content-Type`: `application/json`
- **Body:** Select **raw** → Choose **JSON**:
  ```json
  {
    "title": "Project_Milestone_Alpha",
    "note": "Backend API successfully persisted on AWS EFS shared storage!"
  }
  ```
- **Click Send** → Expected Response (`201 Created`):
  ```json
  {
    "message": "Saved to EFS",
    "filename": "Project_Milestone_Alpha_1732617700000.txt"
  }
  ```

---

##### 2. GET Request — Read Note via Task 2 (Proves EFS Shared Storage)
- **Method:** `GET`
- **URL:** `http://<TASK_2_PUBLIC_IP>:3000/notes`
- **Headers:** *(None required)*
- **Body:** *(None)*
- **Click Send** → Expected Response (`200 OK`):
  ```json
  {
    "total": 1,
    "notes": [
      {
        "filename": "Project_Milestone_Alpha_1732617700000.txt",
        "content": "Backend API successfully persisted on AWS EFS shared storage!"
      }
    ]
  }
  ```

![Postman Proof](images/04_postman_sharing_proof.svg)

---

#### Test B: Terminal / CLI Verification (Alternative to Postman)

- **Windows PowerShell:**
  ```powershell
  # 1. POST Note via Task 1
  curl.exe -X POST http://<TASK_1_PUBLIC_IP>:3000/notes -H "Content-Type: application/json" -d "{\"title\": \"Project_Milestone_Alpha\", \"note\": \"Backend API successfully persisted on AWS EFS shared storage!\"}"

  # 2. GET Notes via Task 2
  curl.exe http://<TASK_2_PUBLIC_IP>:3000/notes
  ```

- **Linux / macOS Bash:**
  ```bash
  # 1. POST Note via Task 1
  curl -X POST http://<TASK_1_PUBLIC_IP>:3000/notes \
    -H "Content-Type: application/json" \
    -d '{"title": "Project_Milestone_Alpha", "note": "Backend API successfully persisted on AWS EFS shared storage!"}'

  # 2. GET Notes via Task 2
  curl http://<TASK_2_PUBLIC_IP>:3000/notes
  ```

---

#### Test C: EC2 Terminal Proof
On your mounted EC2 instance terminal:
```bash
ls -la /mnt/efs/notes/
cat /mnt/efs/notes/Project_Milestone_Alpha_*.txt
```

![EC2 Terminal Proof](images/05_ec2_terminal_proof.svg)

---

## 📦 Deliverables Structure

For assignment submission, organize your zip archive with the following structure:

```
sundeep_hiremat_assignment_1.zip
├── 1/
│   ├── Dockerfile
│   ├── package.json
│   └── server.js
├── 2/
│   └── ecr_image_uri.txt
├── 3/
│   └── ecs_tasks_running_screenshot.svg
├── 4/
│   └── postman_post_task1_and_get_task2.svg
└── 5/
    └── ec2_terminal_ls_and_cat.svg
```

The completed package is located at:  
`assignments/module_03_aws_assignment/sundeep_hiremat_assignment_1.zip`
