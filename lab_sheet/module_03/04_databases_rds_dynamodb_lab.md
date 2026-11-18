# Lab Sheet 3.4: Managed Cloud Databases — Amazon RDS & Amazon DynamoDB
> **Module 3:** AWS Associate Core Knowledge  
> **Topic 3.b:** Relational (RDS/Aurora) & NoSQL (DynamoDB) Databases  
> **Target:** Cloud Software Developer Trainees  

---

## 🎯 Lab Objectives
1. Launch a managed relational database on **Amazon RDS** (PostgreSQL or MySQL) within the custom VPC.
2. Configure database Subnet Groups, Security Groups, and connection endpoints.
3. Create a serverless NoSQL table on **Amazon DynamoDB** with primary keys (Partition Key & Sort Key).
4. Perform item insertion, query, and scan operations in DynamoDB.

---

## 🛠️ Part 1: Amazon RDS Managed Database

### Step 1: Create a DB Subnet Group
1. Open the **Amazon RDS Dashboard** -> Click **Subnet groups** in the left menu.
2. Click **Create DB subnet group**.
3. **Name:** `task-database-subnet-group`.
4. **VPC:** Select your custom VPC (`10.0.0.0/16`).
5. Under *Add subnets*: Select two Availability Zones (e.g., `ap-south-1a` and `ap-south-1b`) and select the private subnets.
6. Click **Create**.

### Step 2: Launch the RDS Database Instance
1. Click **Databases** in the left menu -> Click **Create database**.
2. **Choose a database creation method:** `Standard create`.
3. **Engine options:** `PostgreSQL` (or `MySQL`).
4. **Templates:** Select **Free tier** (crucial to avoid unexpected charges!).
5. **Settings:**
   * **DB instance identifier:** `task-prod-db`.
   * **Master username:** `postgresadmin`.
   * **Master password:** Set a secure password.
6. **Instance configuration:** `db.t3.micro` or `db.t4g.micro`.
7. **Storage:** General Purpose SSD (gp2 or gp3), 20 GiB. Disable storage autoscaling for lab.
8. **Connectivity:**
   * Virtual Private Cloud: Select your custom VPC.
   * DB Subnet Group: `task-database-subnet-group`.
   * Public access: **No** (Database remains safely shielded in the private subnet!).
   * VPC security group: Create new `rds-database-sg`, allowing port `5432` only from the EC2 web security group.
9. Click **Create database**.

---

## 🛠️ Part 2: Amazon DynamoDB Serverless NoSQL

### Step 1: Create a DynamoDB Table
1. Open the **DynamoDB Dashboard** in `ap-south-1` -> Click **Create table**.
2. **Table name:** `Students`.
3. **Partition key (PK):** `StudentId` (Type: `String`).
4. **Sort key (SK):** `CourseCode` (Type: `String`).
5. **Table class:** `DynamoDB Standard`.
6. **Capacity settings:** Select **On-demand** (Pay only per read/write request).
7. Click **Create table**.

### Step 2: Insert and Query Items
1. Click on the `Students` table -> Click **Actions** -> Select **Create item**.
2. Add attributes:
   * `StudentId`: `TASK-NLG-001`
   * `CourseCode`: `CSD-2026`
   * `StudentName` (String): `B. Sai Kiran`
   * `Attendance` (Number): `100`
3. Click **Create item**.
4. Repeat for another student record.
5. In the **Explore table items** tab, run a Query on `StudentId = TASK-NLG-001` and verify sub-millisecond retrieval!

---

### ⚠️ Mandatory Resource Teardown
1. Select the RDS database `task-prod-db` -> Click **Actions** -> **Delete**.
2. Uncheck *Create final snapshot* -> Check *"I acknowledge that upon instance deletion..."* -> Type `delete me` -> Confirm.
3. Delete the DynamoDB table `Students`.
