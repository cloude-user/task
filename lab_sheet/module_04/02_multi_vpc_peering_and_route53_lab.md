# Lab 4.2b: Multi-VPC Peering, Gateway Endpoints & Route 53 Private DNS
> **Course Track:** Cloud Software Developer (Module 4: AWS Solutions Architect)  
> **Lab Focus:** Non-Overlapping Subnetting, Bidirectional Peering, S3 Gateway Endpoints & Route 53 Split-View DNS  
> **Prerequisites:** Active AWS Account with VPC, EC2, S3, and Route 53 permissions.  

---

## 🎯 Lab Objectives
By the end of this lab, you will have demonstrated:
1. Designing and provisioning two isolated VPCs with strictly non-overlapping CIDR blocks.
2. Establishing and accepting an **AWS VPC Peering Connection (`pcx`)**.
3. Configuring bidirectional route tables to enable private cross-VPC communication.
4. Deploying a **VPC Gateway Endpoint for Amazon S3** to eliminate NAT data transfer costs.
5. Creating an **Amazon Route 53 Private Hosted Zone** and resolving internal private domain names.
6. Executing a complete, zero-spend resource teardown.

---

## 🛠️ Step-by-Step Practical Instructions

### Task 1: Create VPC A (Production) and VPC B (Analytics)
1. Navigate to the **VPC Console** in region `ap-south-1` (Mumbai).
2. Click **Create VPC** → Select **VPC only**:
   - **Name tag:** `VPC-A-Production`
   - **IPv4 CIDR block:** `10.1.0.0/16` → Click **Create VPC**.
3. Create a public subnet in VPC-A:
   - Go to **Subnets** → Click **Create subnet**.
   - VPC: Select `VPC-A-Production`.
   - Subnet name: `VPC-A-Public-Subnet-1`.
   - Availability Zone: `ap-south-1a`.
   - IPv4 subnet CIDR block: `10.1.1.0/24`.
   - Click **Create subnet**. Enable **Auto-assign public IPv4 address** on this subnet.
4. Create VPC B:
   - Click **Create VPC** → Select **VPC only**.
   - **Name tag:** `VPC-B-Analytics`
   - **IPv4 CIDR block:** `10.2.0.0/16` *(Strictly non-overlapping!)* → Click **Create VPC**.
5. Create a private subnet in VPC-B:
   - Subnet name: `VPC-B-Private-Subnet-1`.
   - VPC: Select `VPC-B-Analytics`.
   - Availability Zone: `ap-south-1b`.
   - IPv4 subnet CIDR block: `10.2.1.0/24`.
   - Click **Create subnet**.

---

### Task 2: Create and Accept the VPC Peering Connection
1. In the VPC Console left navigation menu, click **Peering connections** → Click **Create peering connection**.
2. Configure settings:
   - **Name:** `Peering-VPC-A-to-VPC-B`
   - **VPC ID (Requester):** Select `VPC-A-Production`.
   - Select **My account** and **This region (ap-south-1)**.
   - **VPC ID (Accepter):** Select `VPC-B-Analytics`.
3. Click **Create peering connection**.
4. The status shows **Pending acceptance**.
5. Select the peering connection → Click **Actions** → **Accept request** → Click **Accept request**. Status changes to **Active**.

---

### Task 3: Configure Bidirectional Route Tables (The Critical Step)
1. Go to **Route tables** → Find the main route table for `VPC-A-Production`:
   - Click **Routes** tab → Click **Edit routes** → Click **Add route**.
   - **Destination:** `10.2.0.0/16` (VPC B's CIDR).
   - **Target:** Select **Peering Connection** → Choose `Peering-VPC-A-to-VPC-B`.
   - Click **Save changes**.
2. Now configure VPC B's return path:
   - Select the main route table for `VPC-B-Analytics`.
   - Click **Routes** tab → Click **Edit routes** → Click **Add route**.
   - **Destination:** `10.1.0.0/16` (VPC A's CIDR).
   - **Target:** Select **Peering Connection** → Choose `Peering-VPC-A-to-VPC-B`.
   - Click **Save changes**.

---

### Task 4: Deploy a Free VPC Gateway Endpoint for Amazon S3
1. In the VPC Console, click **Endpoints** → Click **Create endpoint**.
2. Name: `S3-Gateway-Endpoint-VPC-A`.
3. Service category: Select **AWS services**.
4. Services list: Search for `s3` → Select the service named `com.amazonaws.ap-south-1.s3` of type **Gateway**.
5. VPC: Select `VPC-A-Production`.
6. Route tables: Select the checkbox next to the route table for VPC A.
7. Policy: Leave **Full access** → Click **Create endpoint**.
8. Verify in your VPC A route table: You will see a new route pointing to `pl-xxxx (com.amazonaws.ap-south-1.s3)` with target `vpce-xxxx`! All S3 traffic now routes locally and free of charge.

---

### Task 5: Configure Route 53 Private Hosted Zone
1. Open the **Amazon Route 53 Console** → Click **Hosted zones** → Click **Create hosted zone**.
2. Domain name: `internal.task`
3. Type: Select **Private hosted zone for Amazon VPC**.
4. VPCs to associate with the hosted zone:
   - Region: `Asia Pacific (Mumbai) (ap-south-1)`.
   - VPC ID: Select `VPC-A-Production`.
   - Click **Add VPC** → Select `VPC-B-Analytics`.
5. Click **Create hosted zone**.
6. Inside `internal.task`, click **Create record**:
   - Record name: `analytics-db`
   - Record type: `A - Routes traffic to an IPv4 address`
   - Value: `10.2.1.50` (A simulated private database IP in VPC B).
   - TTL: `60` seconds.
7. Click **Create records**. Any EC2 instance running in VPC A or VPC B can now resolve `analytics-db.internal.task` directly to `10.2.1.50` without touching the public internet.

---

## 🧹 Clean-Up Instructions (Prevent Accidental Charges)
1. **Route 53:** Delete the `analytics-db` record, then delete the `internal.task` private hosted zone.
2. **VPC Endpoints:** Select `S3-Gateway-Endpoint-VPC-A` → Click **Actions** → **Delete VPC endpoint**.
3. **Peering Connections:** Select `Peering-VPC-A-to-VPC-B` → Click **Actions** → **Delete peering connection** (Check the box to delete related route table entries).
4. **VPCs:** Delete `VPC-A-Production` and `VPC-B-Analytics` (this cleans up associated subnets automatically).
