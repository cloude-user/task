# Lab 1: Amazon EC2 Provisioning, Lifecycle & Custom AMIs
> **Program:** TASK Telangana · Cloud Software Developer  
> **Module 03:** AWS Core Services & Infrastructure  
> **Trainer:** Sundeep Hiremath | Nalgonda Training Center  
> **Analogy:** *Renting, Configuring & Duplicating the Vehicle Engine*

---

## 🎯 Lab Objectives
By the end of this hands-on lab, every student will be able to:
1. Launch an Amazon EC2 instance using **Amazon Linux 2023** on the **AWS Free Tier** (`t2.micro` or `t3.micro`).
2. Generate and securely store an SSH Key Pair (`.pem` format).
3. Configure an inbound **Security Group** permitting SSH (Port 22) and Web HTTP (Port 80).
4. Inject automated **User Data** (bootstrapping script) to auto-configure Apache and Python without manual SSH.
5. Inspect and execute EC2 Lifecycle states (**Running ➔ Stopping ➔ Stopped ➔ Terminated**) and understand billing impacts.
6. Bake a **Custom AMI (Golden Image)** and spin up an instant twin clone in under 60 seconds.

---

## 🚗 The Vehicle Metaphor in Action

| Cloud Concept | Vehicle Metaphor | Explanation |
|---|---|---|
| **EC2 Instance** | The Rental Car Engine & Chassis | You don't buy a car manufacturing plant; you rent an engine on-demand by the hour. |
| **AMI** | Car Model Blueprint | Determines whether you are driving a Sedan (Amazon Linux) or a Sports Coupe (Ubuntu). |
| **Instance Type** | Engine Cylinders & Horsepower | `t3.micro` is a fuel-efficient 1-cylinder engine for students; `c5.xlarge` is a V8 race engine. |
| **Key Pair** | Physical Ignition Key | Without this digital key file, no one on Earth can enter or drive the car. |
| **User Data** | Pre-delivery automated accessories | Fuels the tank, tunes the stereo, and turns on the AC before you touch the steering wheel. |

---

## 🛠️ Step-by-Step Lab Instructions

### Step 1: Access AWS Console & Set Region
1. Open your browser and navigate to the [AWS Management Console](https://console.aws.amazon.com/).
2. In the top-right navigation bar, ensure your region is set to **Asia Pacific (Mumbai) `ap-south-1`** (or `us-east-1`).

---

### Step 2: Launch Instance Wizard
1. In the search bar at the top, type `EC2` and press Enter.
2. Click the orange **Launch Instance** button.
3. **Name and tags:**
   - Name: `task-student-webserver-01`
4. **Application and OS Images (Amazon Machine Image - AMI):**
   - Select **Amazon Linux**.
   - Under AMI dropdown: Ensure **Amazon Linux 2023 AMI (Free tier eligible)** is selected.
   - Architecture: `64-bit (x86)`.
5. **Instance Type:**
   - Select `t2.micro` (or `t3.micro` depending on availability in your account). Both provide 1 vCPU and 1 GiB memory.

---

### Step 3: Configure Key Pair (The Ignition Key)
1. Under **Key pair (login)**, click **Create new key pair**.
2. **Key pair name:** `task-nalgonda-key`
3. **Key pair type:** `RSA`
4. **Private key file format:**
   - Select **`.pem`** (Works directly with Windows PowerShell, OpenSSH, Mac, and Linux).
5. Click **Create key pair**.
   - ⚠️ *Your browser will immediately download `task-nalgonda-key.pem`. Move this file to a safe folder (e.g., `C:\Users\sundeep\Downloads\` or your project folder). AWS never stores a copy!*

---

### Step 4: Network Settings & Security Group (The Personal Bodyguard)
1. Under **Network settings**, click **Edit** (top right of network box).
2. **VPC:** Leave as *Default VPC*.
3. **Subnet:** Select any subnet (or *No preference*).
4. **Auto-assign public IP:** Ensure this is set to **Enable**.
5. **Firewall (security groups):**
   - Select **Create security group**.
   - Security group name: `task-web-sg`
   - Description: `Allow SSH from My IP and HTTP from anywhere`
6. **Inbound Security Group Rules:**
   - **Rule 1 (SSH):**
     - Type: `SSH` | Protocol: `TCP` | Port: `22` | Source: Select `My IP` (Recommended for security) or `Anywhere-IPv4` (`0.0.0.0/0`).
   - Click **Add security group rule**.
   - **Rule 2 (HTTP Web):**
     - Type: `HTTP` | Protocol: `TCP` | Port: `80` | Source: `Anywhere-IPv4` (`0.0.0.0/0`).

---

### Step 5: Configure Storage (The Root Car Trunk)
- Leave the root volume as default: **8 GiB gp3 (General Purpose SSD)**.
- Note: AWS Free Tier includes up to **30 GiB of EBS storage per month free**.

---

### Step 6: Inject User Data Bootstrapping Script
1. Scroll down and expand the **Advanced details** section.
2. Scroll to the very bottom to the **User data** box.
3. Paste the following startup script:

```bash
#!/bin/bash
# 1. Update OS software repositories
dnf update -y

# 2. Install Apache web server and python tools
dnf install -y httpd python3 git

# 3. Start Apache HTTP service and enable on boot
systemctl start httpd
systemctl enable httpd

# 4. Fetch instance metadata using secure IMDSv2
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
INSTANCE_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
AZ=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/placement/availability-zone)

# 5. Write rich student landing page
cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html>
<head>
    <title>TASK Cloud Lab - EC2 Active</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #232F3E; color: white; text-align: center; padding-top: 50px; }
        .card { background: white; color: #1A202C; max-width: 650px; margin: auto; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); border-top: 6px solid #FF9900; }
        h1 { color: #232F3E; margin-bottom: 5px; }
        .badge { background: #FF9900; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; }
        .info { text-align: left; background: #F8FAFC; border: 1px solid #E2E8F0; padding: 15px; border-radius: 8px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">TASK TELANGANA · NALGONDA CENTER</span>
        <h1>🚀 EC2 Web Server Bootstrapped!</h1>
        <p>Trainer: <b>Sundeep Hiremath</b> | Cloud Software Developer</p>
        <div class="info">
            <p><b>Instance ID:</b> $INSTANCE_ID</p>
            <p><b>Availability Zone:</b> $AZ</p>
            <p><b>Status:</b> Apache HTTPD running via User Data automation!</p>
        </div>
    </div>
</body>
</html>
EOF
```

4. Click **Launch instance**!

---

### Step 7: Verify Live Web Application
1. In the confirmation screen, click the **Instance ID** link.
2. In the instances table, wait until **Instance State** turns to `Running` and **Status Check** shows `2/2 checks passed`.
3. Select your instance and locate the **Public IPv4 address** in the details pane below.
4. Copy the IP (e.g. `13.233.xx.xx`).
5. Open a new browser tab and navigate to:  
   `http://<YOUR-PUBLIC-IPV4-ADDRESS>`
6. 🎉 **Success!** Your bootstrapped web server is serving the customized page live on the world wide web!

---

### Step 8: Connecting via SSH (Terminal / PowerShell)

To connect from Windows PowerShell or macOS/Linux:

```powershell
# 1. Navigate to directory where task-nalgonda-key.pem is saved
cd ~/Downloads

# 2. (Linux/macOS only) Enforce read-only permissions
chmod 400 task-nalgonda-key.pem

# 3. Connect via OpenSSH
ssh -i "task-nalgonda-key.pem" ec2-user@<YOUR-PUBLIC-IPV4-ADDRESS>
```

Type `yes` when prompted to verify host authenticity. You are now logged directly into the Linux EC2 terminal!

---

### Step 9: Creating a Custom AMI (The Golden Image)

Why configure servers manually every day? Snapshot your configured web server into a reusable AMI:

1. In the EC2 Console, select `task-student-webserver-01`.
2. Click **Actions** ➔ **Image and templates** ➔ **Create image**.
3. **Image name:** `task-golden-ami-v1`
4. **Image description:** `Pre-configured Apache and Python web server`
5. Click **Create image**.
6. On the left sidebar under *Images*, click **AMIs**.
7. Watch the status change from `pending` to `available` (takes ~2 minutes).
8. Once available, select it and click **Launch instance from AMI**.
9. Notice that this second instance immediately serves your web application without running any User Data script!

---

### Step 10: Decommission & Cost Hygiene (Zero-Dollar Shield)

Before leaving the lab:
1. Select your test instances.
2. Click **Instance state** ➔ **Stop instance** (to pause compute billing).
3. If you no longer need the test instance, click **Instance state** ➔ **Terminate instance** (permanently removes instance and releases root EBS storage).

