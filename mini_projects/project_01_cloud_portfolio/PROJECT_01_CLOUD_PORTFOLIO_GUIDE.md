# Mini Project 1: Deploying a Cloud Portfolio on Ubuntu 24.04 LTS with Nginx & GitHub
> **Program:** TASK Telangana · Cloud Software Developer  
> **Trainer:** Sundeep Hiremat | Nalgonda Training Center  
> **Level:** Beginner to Intermediate | Hands-on Production Lab  
> **Prerequisites:** Active AWS Account, GitHub Account  

---

## 🎯 Project Overview & Real-World Goal

In this mini project, every student will provision an enterprise-grade **Ubuntu 24.04 LTS Linux server** on Amazon EC2, configure the high-performance **Nginx** web server, clone their personal portfolio directly from **GitHub**, configure Linux permissions (`www-data`), and publish their live developer portfolio accessible to anyone worldwide via public IPv4.

```
       [ Public Internet / Hiring Managers ]
                         |
                         v  (HTTP: Port 80)
              [ Security Group Firewall ]
                         |
                         v
  +-------------------------------------------------------+
  | AMAZON EC2 INSTANCE (Ubuntu 24.04 LTS)                |
  |                                                       |
  |  +--------------------+       +--------------------+  |
  |  |    NGINX ENGINE    |<------| GITHUB REPOSITORY  |  |
  |  | (Reverse Proxy/Web)|       | (git clone via SSH)|  |
  |  +--------------------+       +--------------------+  |
  |            |                                          |
  |            v                                          |
  |   /var/www/html/ (Portfolio Assets: HTML/CSS/JS)      |
  +-------------------------------------------------------+
```

---

## 🛠️ Step-by-Step Execution Playbook

### Step 1: Launch the Ubuntu EC2 Instance

1. Open the [AWS Management Console](https://console.aws.amazon.com/) and navigate to **EC2 Dashboard**.
2. Click the orange **Launch Instance** button.
3. Configure the instance specifications as follows:

| Field | Configuration Value | Why This Setting Matters |
|---|---|---|
| **Name** | `gauri-portfolio` *(or `<your-name>-portfolio`)* | Identifies your server instance in the AWS console. |
| **OS / AMI** | **Ubuntu Server 24.04 LTS (HVM), SSD Volume Type** | Long-Term Support (LTS) release; standard in enterprise DevOps. |
| **Architecture** | `64-bit (x86)` | Standard x86 compatibility for widespread binary packages. |
| **Instance Type** | `t2.micro` or `t3.micro` *(Free tier eligible)* | 1 vCPU & 1 GiB RAM—free under AWS Free Tier allowance. |
| **Key Pair** | Select existing key or create `task-nalgonda-key.pem` | Secures direct administrative access. |
| **Network / VPC** | `Default VPC` | Pre-configured AWS VPC with public routing. |
| **Subnet** | Any Public Subnet (e.g. `ap-south-1a`) | Provides a route out to the Internet Gateway. |
| **Auto-assign Public IP**| **Enable** | Required so your website gets a public IPv4 address! |

#### Configure the Security Group Firewall:
Select **Create security group**, name it `portfolio-web-sg`, and add these exact rules:

| Type | Protocol | Port Range | Source | Purpose |
|---|---|---|---|---|
| **SSH** | TCP | `22` | **My IP** | Secure administrative terminal access only from your machine. |
| **HTTP** | TCP | `80` | **Anywhere-IPv4 (`0.0.0.0/0`)** | Allows any recruiter or student worldwide to view your portfolio. |

4. Leave storage at **8 GiB gp3 (General Purpose SSD)**.
5. Click **Launch instance**.

---

### Step 2: Connect to Ubuntu via EC2 Instance Connect

AWS provides browser-based terminal connectivity without requiring PuTTY or local SSH key setup:

1. In the EC2 Console, go to **Instances** and select your running `gauri-portfolio` instance.
2. Click the **Connect** button at the top.
3. Choose the **EC2 Instance Connect** tab.
4. Verify username is set to `ubuntu`.
5. Click **Connect**.
6. A black browser terminal opens with your shell prompt:
   ```bash
   ubuntu@ip-xxx-xxx-xxx-xxx:~$
   ```

---

### Step 3: Update and Upgrade the Ubuntu OS

Always refresh package repository indexes before installing new software:

```bash
# Update repository index lists
sudo apt update

# Upgrade existing packages to latest patches
sudo apt upgrade -y
```

---

### Step 4: Install Git and the Nginx Web Server

Nginx is the world's most popular high-concurrency web server and reverse proxy:

```bash
# Install Git and Nginx in a single command
sudo apt install git nginx -y
```

Verify that the Nginx service is running:

```bash
sudo systemctl status nginx
```

Look for:  
`Active: active (running) since ...`  
*(Press `q` to exit the status view).*

---

### Step 5: Test the Default Nginx Welcome Page

1. Switch back to your AWS EC2 Console.
2. Select your instance and copy its **Public IPv4 address** (e.g., `13.233.45.67`).
3. Open a new browser tab and navigate to:
   ```
   http://YOUR_EC2_PUBLIC_IP
   ```
   *(Note: Make sure your browser uses `http://` and not `https://`).*
4. You should see the **Welcome to nginx!** page. This confirms your network, security group, and web server daemon are fully operational!

---

### Step 6: Deploy Your GitHub Portfolio

Now we replace the default Nginx placeholder with real production portfolio code:

```bash
# 1. Navigate to the web root directory
cd /var/www/html

# 2. Remove the default Nginx placeholder page
sudo rm -f index.nginx-debian.html

# 3. Clone the portfolio repository directly into the current directory (.)
sudo git clone https://github.com/gauri-abc/gauri-yadav-cloud-portfolio.git .
```

> 💡 **Student Customization Note:**  
> If you have your own GitHub portfolio repository, replace the URL above with your own repository URL:  
> `sudo git clone https://github.com/<your-username>/<your-portfolio-repo>.git .`

Verify the cloned files:

```bash
ls -la
```

You should see:
```text
drwxr-xr-x 4 root root 4096 Nov 13 10:00 .
drwxr-xr-x 3 root root 4096 Nov 13 09:55 ..
drwxr-xr-x 8 root root 4096 Nov 13 10:00 .git
-rw-r--r-- 1 root root 8421 Nov 13 10:00 index.html
drwxr-xr-x 2 root root 4096 Nov 13 10:00 css
drwxr-xr-x 2 root root 4096 Nov 13 10:00 img
drwxr-xr-x 2 root root 4096 Nov 13 10:00 js
```

---

### Step 7: Configure Linux File Permissions for Web Security

On Ubuntu, Nginx runs under the service account **`www-data`**. We must grant ownership and readable permissions so Nginx can serve files cleanly:

```bash
# Set ownership of all web files to the Nginx service account
sudo chown -R www-data:www-data /var/www/html

# Set directory permissions to 755 (read/execute for all, write for owner)
sudo chmod -R 755 /var/www/html
```

---

### Step 8: Restart and Enable Nginx

```bash
# Restart Nginx to reload all assets cleanly
sudo systemctl restart nginx

# Ensure Nginx automatically starts if the server ever reboots
sudo systemctl enable nginx
```

---

### Step 9: Final Test & Verification

1. Go back to your browser tab.
2. Hard-refresh the page (`Ctrl + F5` on Windows or `Cmd + Shift + R` on Mac):
   ```
   http://YOUR_EC2_PUBLIC_IP
   ```
3. 🎉 **Congratulations!** You are now viewing the live, responsive **Cloud Portfolio** website served directly from your Amazon EC2 server!

---

## 🔍 Troubleshooting Guide for Students

| Symptom | Probable Cause | Exact Fix Command / Action |
|---|---|---|
| **Browser says "Site cannot be reached" (Timeout)** | Security Group missing Inbound HTTP Port 80 rule. | In EC2 Console ➔ Security Groups ➔ Edit Inbound Rules ➔ Add `HTTP | Port 80 | 0.0.0.0/0`. |
| **Browser redirects to HTTPS and fails** | Browser auto-appended `https://` (No SSL certificate installed yet). | Explicitly type `http://<YOUR_IP>` in the URL bar. |
| **Default Nginx page still displays** | `index.nginx-debian.html` was not deleted. | Run `sudo rm -f /var/www/html/index.nginx-debian.html` and hard-refresh browser. |
| **403 Forbidden Error** | File permissions are incorrect. | Run `sudo chown -R www-data:www-data /var/www/html` and `sudo chmod -R 755 /var/www/html`. |
| **Nginx service fails to start** | Apache or another process is occupying Port 80. | Run `sudo netstat -tulpn | grep :80` or `sudo systemctl stop httpd`. |

---

## 🧹 Project Teardown & Cost Hygiene

Once you have demonstrated your portfolio to the trainer or completed your lab:
- If keeping the site online: Leave running (1 `t2.micro` or `t3.micro` instance is free for 750 hours/month under AWS Free Tier).
- If saving Free Tier hours: In EC2 Console ➔ Select `gauri-portfolio` ➔ **Instance state** ➔ **Stop instance**.
- When stopping an instance, your public IP changes upon next restart.

