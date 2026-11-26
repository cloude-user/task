# Lab 4.4b: EC2 Auto Scaling Groups & Amazon ElastiCache (Redis)
> **Course Track:** Cloud Software Developer (Module 4: AWS Solutions Architect)  
> **Lab Focus:** Launch Templates, Dynamic Auto Scaling Groups, CPU Stress Testing, Target Tracking & ElastiCache Caching  
> **Prerequisites:** Active AWS Account with EC2, Auto Scaling, and ElastiCache permissions.  

---

## 🎯 Lab Objectives
By the end of this lab, you will have demonstrated:
1. Creating an **EC2 Launch Template** with automated Apache installation and CPU stress tooling.
2. Configuring a **Multi-AZ Auto Scaling Group (ASG)** with Min=2, Desired=2, Max=4 instances.
3. Attaching the ASG to an Application Load Balancer Target Group.
4. Configuring a **Target Tracking Scaling Policy** based on Average CPU Utilization (50%).
5. Generating simulated CPU load using Linux stress utilities to observe automated horizontal scale-out live.
6. Deploying an **Amazon ElastiCache (Redis/Valkey)** cluster and verifying sub-millisecond in-memory caching.

---

## 🛠️ Step-by-Step Practical Instructions

### Task 1: Create an EC2 Launch Template
1. Open the **EC2 Console** → In the left menu under **Instances**, click **Launch Templates** → Click **Create launch template**.
2. Configure settings:
   - **Launch template name:** `lt-task-web-tier`
   - **Template version description:** `v1 - Web server with stress-ng tool`
   - **Application and OS Images (AMI):** `Amazon Linux 2023 AMI`
   - **Instance type:** `t3.micro` (Free Tier)
   - **Key pair:** Select your key pair or proceed without key pair.
   - **Network settings:**
     - Select **Create security group**: `sg-asg-web` allowing Inbound HTTP (Port 80) from your ALB security group (or `0.0.0.0/0`).
3. Expand **Advanced details** → Scroll to **User data**:
   ```bash
   #!/bin/bash
   dnf update -y
   dnf install -y httpd stress-ng
   systemctl start httpd
   systemctl enable httpd
   INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
   AZ=$(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)
   echo "<h1>TASK ASG Node: $INSTANCE_ID in AZ: $AZ</h1>" > /var/www/html/index.html
   echo "healthy" > /var/www/html/healthz
   ```
4. Click **Create launch template**.

---

### Task 2: Create a Multi-AZ Auto Scaling Group (ASG)
1. In the EC2 left menu, under **Auto Scaling**, click **Auto Scaling Groups** → Click **Create Auto Scaling group**.
2. **Step 1 (Choose launch template):**
   - Auto Scaling group name: `asg-task-production`
   - Launch template: Select `lt-task-web-tier` (Version: `Latest (1)`) → Click **Next**.
3. **Step 2 (Choose instance launch options):**
   - Network: Select Default VPC.
   - Availability Zones and subnets: Select at least two subnets (e.g., `ap-south-1a` and `ap-south-1b`) to guarantee multi-AZ redundancy.
   - Click **Next**.
4. **Step 3 (Configure advanced options):**
   - Under **Load balancing**, select **Attach to an existing load balancer** (or attach to Target Group `tg-web-production` if created in Lab 4.3b).
   - Under **Health checks**: Check **Turn on Elastic Load Balancing health checks** (ASG will replace instances that fail ALB health checks).
   - Health check grace period: `300` seconds → Click **Next**.
5. **Step 4 (Configure group size and scaling):**
   - **Desired capacity:** `2`
   - **Minimum capacity:** `2`
   - **Maximum capacity:** `4`
   - Under **Scaling policies**, select **Target tracking scaling policy**:
     - Metric type: **Average CPU utilization**
     - Target value: `50` (% CPU)
     - Warmup time: `120` seconds.
   - Click **Next** → Click **Next** (Skip notifications) → Click **Next** (Skip tags) → Click **Create Auto Scaling group**.

---

### Task 3: Observe Auto Scaling Self-Healing & Live Instance Launch
1. Click on `asg-task-production` → Go to the **Instance management** tab.
2. Watch the status: ASG launches exactly 2 instances, distributing one in `ap-south-1a` and one in `ap-south-1b`.
3. **The Chaos Engineering Test:**
   - Go to **EC2 Instances**, select ONE of the running ASG instances, and manually click **Terminate instance**!
   - Return to the Auto Scaling Group **Activity** tab:
   - Observe that the ASG immediately detects the degraded capacity (`Capacity is 1, Desired is 2`) and launches a brand new replacement EC2 instance automatically to restore desired capacity!

---

### Task 4: Simulate CPU Stress & Observe Horizontal Scale-Out
1. Connect to one of the ASG EC2 instances via **EC2 Instance Connect** (browser-based terminal).
2. Run the Linux stress utility to artificially saturate all CPU cores:
   ```bash
   stress-ng --cpu 2 --timeout 300s --metrics-brief
   ```
3. Open a second terminal window or check `htop` / `top`: CPU will spike to 100%.
4. Open the **Amazon CloudWatch Console** → Alarms:
   - Notice the alarm created by ASG: `TargetTracking-asg-task-production-AlarmHigh-...` triggers when CPU exceeds 50%.
5. Within 2 to 3 minutes, return to the Auto Scaling Group **Activity** tab:
   - You will see the event: *"Launching a new EC2 instance in response to TargetTracking policy"*.
   - Capacity scales out from 2 to 3, and then to 4 instances!
6. Once the 300-second stress command completes, CPU drops back to 0%, and the ASG initiates a graceful **Scale-In** terminating excess instances according to termination policy.

---

### Task 5: Provision Amazon ElastiCache (Redis) & Cache-Aside Verification
1. Navigate to the **Amazon ElastiCache Console** → Click **Redis clusters** (or **Valkey clusters**).
2. Click **Create cluster**:
   - Cluster deployment: **Redis (cluster mode disabled)**
   - Name: `cache-task-session-store`
   - Node type: `cache.t3.micro` (or `cache.t4g.micro`)
   - Number of replicas: `0` (for single-node lab demonstration)
   - Subnet group: Default VPC private subnets.
3. Click **Create**. Wait 3 to 5 minutes until status is `Available`.
4. Copy the **Primary Endpoint** (e.g., `cache-task-session-store.xxxx.0001.aps1.cache.amazonaws.com:6379`).
5. From an EC2 instance in the same VPC, verify the sub-millisecond cache latency using Python:
   ```python
   import redis
   import time

   # Connect to ElastiCache endpoint
   r = redis.Redis(host='<your-elasticache-endpoint>', port=6379, db=0)

   # Cache-Aside Simulation
   user_id = "user:101"
   start = time.time()
   cached_data = r.get(user_id)

   if cached_data is None:
       print("CACHE MISS: Fetching from Database (simulated 50ms disk query)...")
       time.sleep(0.05) # Simulate database latency
       db_data = '{"name": "TASK Student", "role": "Cloud Architect"}'
       r.setex(user_id, 300, db_data) # Store in RAM with 300s TTL
       print(f"Data saved to Redis. Total latency: {(time.time() - start)*1000:.2f} ms")
   else:
       print(f"CACHE HIT from Redis RAM! Total latency: {(time.time() - start)*1000:.2f} ms")
   ```
6. Run the script once: outputs **CACHE MISS** (~52 ms).
7. Run the script a second time: outputs **CACHE HIT** (~0.8 ms)! Demonstrating a **65x latency improvement**!

---

## 🧹 Clean-Up Instructions (MANDATORY TO AVOID BILLING)
1. **Auto Scaling Groups:**
   - Select `asg-task-production` → Click **Edit** → Change Desired: `0`, Min: `0`, Max: `0` → Click **Update**.
   - Wait 1 minute for all instances to terminate cleanly.
   - Click **Actions** → **Delete Auto Scaling group**.
2. **Launch Templates:** In Launch Templates, select `lt-task-web-tier` → **Actions** → **Delete template**.
3. **ElastiCache:** In the ElastiCache Console, select `cache-task-session-store` → **Actions** → **Delete** (Uncheck create final backup).
