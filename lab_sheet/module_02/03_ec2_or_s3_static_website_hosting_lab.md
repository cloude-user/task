# Lab Sheet 2.3: Hosting a Static Website on Amazon EC2 or Amazon S3
> **Module 2:** AWS Certified Cloud Practitioner  
> **Topic 2.c:** Hands-on Mini Project (EC2 or S3 Web Hosting)  
> **Target:** Cloud Software Developer Trainees  

---

## 🎯 Lab Objectives
Learn the two fundamental methods for hosting a static web application on AWS:
* **Option A:** Traditional Linux Web Server using **Amazon EC2 (Ubuntu 24.04 LTS + Nginx)**.
* **Option B:** Serverless Static Website Hosting using **Amazon S3**.

---

## 🛠️ Option A: Deploy on Amazon EC2 (Linux + Nginx)

### Step 1: Launch the EC2 Instance
1. Open the **EC2 Dashboard** in `ap-south-1` (Mumbai) -> Click **Launch Instance**.
2. **Name:** `my-portfolio-webserver`.
3. **AMI:** `Ubuntu Server 24.04 LTS (HVM), SSD Volume Type`.
4. **Instance Type:** `t2.micro` (or `t3.micro`) — Free tier eligible.
5. **Key pair:** Select an existing key or create `task-key.pem`.
6. **Network settings:**
   * Auto-assign Public IP: **Enable**.
   * Security group: Allow **SSH (Port 22)** from *My IP* and allow **HTTP (Port 80)** from *Anywhere-IPv4 (`0.0.0.0/0`)*.
7. Click **Launch instance**.

### Step 2: Install Nginx & Deploy Web Assets
1. Connect to your instance via **EC2 Instance Connect** (or SSH terminal).
2. Run the update and install commands:
   ```bash
   sudo apt-get update -y
   sudo apt-get install -y nginx
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```
3. Deploy your portfolio HTML into the Nginx root directory:
   ```bash
   echo "<h1>Hello from AWS EC2 Nginx Web Server!</h1>" | sudo tee /var/www/html/index.html
   ```
4. Copy the instance's **Public IPv4 address** from the EC2 console and paste it into your browser tab:
   * URL: `http://<YOUR-EC2-PUBLIC-IP>`
   * *Result:* Your webpage loads live over the internet!

---

## 🛠️ Option B: Deploy Serverless on Amazon S3

### Step 1: Create the S3 Bucket
1. Open the **S3 Dashboard** -> Click **Create bucket**.
2. **Bucket name:** `my-portfolio-<yourname>-2026` (Must be globally unique, lowercase, no spaces).
3. **Region:** `ap-south-1` (Mumbai).
4. **Object Ownership:** ACLs disabled (recommended).
5. **Block Public Access settings for this bucket:**
   * **Uncheck** *Block all public access* (Required for a public static website).
   * Check the acknowledgment box: *"I acknowledge that the current settings might result in this bucket and the objects within becoming public."*
6. Click **Create bucket**.

### Step 2: Enable Static Website Hosting
1. Click on your newly created bucket name -> Click the **Properties** tab.
2. Scroll to the very bottom to **Static website hosting** -> Click **Edit**.
3. Select **Enable**.
4. **Index document:** `index.html`.
5. Click **Save changes**.

### Step 3: Add Public Read Bucket Policy
1. Click the **Permissions** tab -> Scroll to **Bucket policy** -> Click **Edit**.
2. Paste the following JSON policy (replace `<YOUR-BUCKET-NAME>` with your exact bucket name):
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "PublicReadGetObject",
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::<YOUR-BUCKET-NAME>/*"
       }
     ]
   }
   ```
3. Click **Save changes**.

### Step 4: Upload HTML & Access the Live Website
1. Click the **Objects** tab -> Click **Upload** -> Select your `index.html` file.
2. Click **Upload**.
3. Return to the **Properties** tab -> Scroll down to **Static website hosting**.
4. Click the **Bucket website endpoint URL** (e.g., `http://<your-bucket>.s3-website.ap-south-1.amazonaws.com`).
5. *Result:* Your serverless website loads globally with zero server maintenance!

---

### ✅ Verification Checklist
- [ ] Option A: EC2 public IPv4 serves Nginx web page on port 80.
- [ ] Option B: S3 website endpoint serves the uploaded `index.html`.
