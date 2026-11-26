# Lab 4.3b: Elastic Load Balancing (ALB) & Zero-Downtime Draining
> **Course Track:** Cloud Software Developer (Module 4: AWS Solutions Architect)  
> **Lab Focus:** Application Load Balancer (ALB), Target Groups, Path Routing, Deregistration Delay & HTTP 502/503 Triage  
> **Prerequisites:** Active AWS Account with EC2, VPC, and ELB permissions.  

---

## 🎯 Lab Objectives
By the end of this lab, you will have demonstrated:
1. Launching two EC2 instances with distinct web server banners across two separate Availability Zones.
2. Configuring an **Application Load Balancer (ALB)** and **Target Group** with automated HTTP health checks.
3. Observing Round Robin traffic distribution in a web browser.
4. Testing **Deregistration Delay (Connection Draining)** to observe graceful shutdown without customer disruption.
5. Deliberately simulating and diagnosing **HTTP 502 Bad Gateway** and **HTTP 503 Service Unavailable** outages.

---

## 🛠️ Step-by-Step Practical Instructions

### Task 1: Launch Two EC2 Web Servers in Different AZs
1. Navigate to the **EC2 Console** → Click **Launch instances**.
2. Instance 1:
   - **Name:** `WebServer-Node-A`
   - **AMI:** `Amazon Linux 2023 AMI`
   - **Instance type:** `t3.micro` (Free Tier eligible)
   - **Key pair:** Proceed without key pair (or use existing).
   - **Network settings:**
     - Select Default VPC.
     - Subnet: Select an AZ (e.g., `ap-south-1a`).
     - Auto-assign public IP: **Enable**.
     - Security group: Create security group `sg-web-servers` allowing Inbound HTTP (Port 80) from `0.0.0.0/0`.
   - **Advanced details (User Data):**
     ```bash
     #!/bin/bash
     dnf update -y
     dnf install -y httpd
     systemctl start httpd
     systemctl enable httpd
     echo "<h1>TASK Nalgonda Cloud Lab - Server A (AZ: ap-south-1a)</h1>" > /var/www/html/index.html
     echo "healthy" > /var/www/html/healthz
     ```
   - Click **Launch instance**.
3. Launch Instance 2:
   - **Name:** `WebServer-Node-B`
   - Subnet: Choose a **different AZ** (e.g., `ap-south-1b`).
   - Security group: Select existing `sg-web-servers`.
   - **User Data:**
     ```bash
     #!/bin/bash
     dnf update -y
     dnf install -y httpd
     systemctl start httpd
     systemctl enable httpd
     echo "<h1>TASK Nalgonda Cloud Lab - Server B (AZ: ap-south-1b)</h1>" > /var/www/html/index.html
     echo "healthy" > /var/www/html/healthz
     ```
   - Click **Launch instance**.

---

### Task 2: Create Target Group with Health Checks
1. In the EC2 left navigation menu, under **Load Balancing**, click **Target Groups** → Click **Create target group**.
2. Target type: **Instances**.
3. Target group name: `tg-web-production`.
4. Protocol: **HTTP**, Port: **80**, VPC: Default VPC.
5. Health checks:
   - Health check protocol: **HTTP**
   - Health check path: `/healthz`
   - Expand **Advanced health check settings**:
     - Healthy threshold: `2`
     - Unhealthy threshold: `2`
     - Timeout: `5` seconds
     - Interval: `10` seconds
     - Success codes: `200`
6. Click **Next**.
7. In the **Register targets** screen: Select both `WebServer-Node-A` and `WebServer-Node-B` → Click **Include as pending below** → Click **Create target group**.

---

### Task 3: Create Internet-Facing Application Load Balancer
1. In the left navigation, click **Load Balancers** → Click **Create load balancer**.
2. Under **Application Load Balancer**, click **Create**:
   - **Load balancer name:** `alb-task-web-tier`
   - **Scheme:** `Internet-facing`
   - **IP address type:** `IPv4`
   - **Network mapping:** Select Default VPC → Select at least two Availability Zones (`ap-south-1a` and `ap-south-1b`).
   - **Security groups:** Create/select `sg-alb` allowing Inbound HTTP (Port 80) from `0.0.0.0/0`.
   - **Listeners and routing:**
     - Protocol: **HTTP**, Port: **80**
     - Default action: Forward to Target Group `tg-web-production`.
3. Click **Create load balancer**. Wait 2 minutes for state to change from `Provisioning` to `Active`.

---

### Task 4: Verify Load Balancing & Round Robin
1. Select `alb-task-web-tier` → Copy the **DNS name** (e.g., `alb-task-web-tier-12345.ap-south-1.elb.amazonaws.com`).
2. Open a browser tab and navigate to `http://<alb-dns-name>`.
3. Refresh the page several times:
   - *Observation:* You will see the response oscillate between:
     - `TASK Nalgonda Cloud Lab - Server A (AZ: ap-south-1a)`
     - `TASK Nalgonda Cloud Lab - Server B (AZ: ap-south-1b)`
   - The ALB is successfully balancing traffic across both healthy targets!

---

### Task 5: Observe Connection Draining (Deregistration Delay)
1. Go to **Target Groups** → Select `tg-web-production` → Click **Group details** tab.
2. Under **Attributes**, click **Edit**:
   - Notice **Deregistration delay**: Default is `300` seconds. Change it to `60` seconds for lab demonstration → Click **Save changes**.
3. Click the **Targets** tab.
4. Select `WebServer-Node-A` → Click **Deregister**.
5. Observe the status column:
   - Status changes immediately to **draining**.
   - Open your browser and refresh the ALB DNS name repeatedly:
   - Notice that **all new requests** are immediately forwarded exclusively to Server B! Server A receives zero new requests while its in-flight connections finish.
   - After 60 seconds, Server A transitions to **unused**.

---

### Task 6: Simulate and Diagnose HTTP 503 Outage
1. Now select `WebServer-Node-B` in the Target Group and click **Deregister**.
2. Both targets are now removed or draining.
3. Refresh the ALB DNS name in your browser:
   - *Result:* **HTTP 503 Service Unavailable: No healthy targets in target group!**
   - *Core Lesson:* When students encounter HTTP 503 in production, the first place to inspect is Target Health in the Target Group.

---

## 🧹 Clean-Up Instructions
1. **Load Balancers:** Select `alb-task-web-tier` → Click **Actions** → **Delete load balancer**.
2. **Target Groups:** Select `tg-web-production` → Click **Actions** → **Delete**.
3. **EC2 Instances:** Select both `WebServer-Node-A` and `WebServer-Node-B` → Click **Instance state** → **Terminate instance**.
