# Lab 2: AWS Storage Triad (EBS Volumes, Snapshots, EFS & Secure S3 Buckets)
> **Program:** TASK Telangana · Cloud Software Developer  
> **Module 03:** AWS Core Services & Infrastructure  
> **Trainer:** Sundeep Hiremath | Nalgonda Training Center  
> **Analogy:** *The Personal Trunk (EBS), Shared Roof Cargo (EFS), and Global Container Depot (S3)*

---

## 🎯 Lab Objectives
By the end of this hands-on lab, every student will be able to:
1. Articulate the exact architectural differences between **Block (EBS)**, **File (EFS)**, and **Object (S3)** storage.
2. Create an Amazon EBS volume, attach it to a running EC2 instance, format it with a filesystem (`ext4`), and mount it.
3. Take a point-in-time **EBS Snapshot** and restore it into a new volume.
4. Provision an **Amazon S3 Bucket**, confirm **Block Public Access (BPA)** is enforced, and upload objects.
5. Author and attach a JSON **S3 Bucket Policy** enforcing encrypted in-transit requests (**HTTPS/TLS only**).

---

## 🚗 Storage Architecture Metaphor

```
+---------------------------------------------------------------------------------+
|                                 THE VEHICLE FLEET                               |
|                                                                                 |
|   [ EC2 Car A (ap-south-1a) ]                       [ EC2 Car B (ap-south-1b) ] |
|                |                                                 |              |
|   +------------+------------+                       +------------+------------+ |
|   |                         |                       |                         | |
|   v                         v                       v                         v |
| [ EBS Personal Trunk ]  [ EFS Shared Cargo Rack (Mounts across AZs) ]           |
| (gp3 - 1 Car only)      (NFSv4 - Accessible by Car A & Car B simultaneously)    |
+---------------------------------------------------------------------------------+
                                      |
                                      v
              [ AMAZON S3: GLOBAL CONTAINER SHIPPING DEPOT ]
              (Infinite durability, accessible anywhere via HTTPS)
```

---

## 🛠️ Hands-on Lab 2A: Amazon EBS Volume & Snapshot Management

### Step 1: Create an Additional EBS Volume
1. Open the [EC2 Console](https://console.aws.amazon.com/ec2/).
2. On the left navigation pane under **Elastic Block Store**, click **Volumes**.
3. Click the orange **Create volume** button.
4. **Volume settings:**
   - **Volume type:** `General Purpose SSD (gp3)` (Free baseline 3,000 IOPS and 125 MB/s).
   - **Size:** `5 GiB` (Keeps within AWS Free Tier).
   - **Availability Zone:** ⚠️ **CRITICAL:** *Select the EXACT same Availability Zone as your running EC2 instance (e.g., `ap-south-1a`). EBS volumes cannot be attached across different AZs!*
5. Click **Create volume**.

---

### Step 2: Attach the Volume to EC2
1. Select the new 5 GiB volume from the list.
2. Click **Actions** ➔ **Attach volume**.
3. **Instance:** Click the search box and select your running `task-student-webserver-01`.
4. **Device name:** Leave as default (e.g. `/dev/sdf` or `/dev/xvdf`).
5. Click **Attach volume**.

---

### Step 3: Format & Mount the Volume inside Linux
1. Connect to your EC2 instance via SSH or **EC2 Instance Connect**.
2. Run the block device list command to verify the volume is attached:
   ```bash
   lsblk
   ```
   *You will see `xvdf` (5G) with no partition.*

3. Check if the disk already has a filesystem (it should be empty):
   ```bash
   sudo file -s /dev/xvdf
   # Output will say: /dev/xvdf: data
   ```

4. Format the volume with an `ext4` filesystem:
   ```bash
   sudo mkfs -t ext4 /dev/xvdf
   ```

5. Create a mount point directory and mount the disk:
   ```bash
   sudo mkdir -p /mnt/student_data
   sudo mount /dev/xvdf /mnt/student_data
   ```

6. Verify the newly mounted storage space:
   ```bash
   df -h /mnt/student_data
   ```

7. Write a test file to the new drive:
   ```bash
   echo "TASK Telangana Cloud Lab - EBS Storage Verified!" | sudo tee /mnt/student_data/test_log.txt
   cat /mnt/student_data/test_log.txt
   ```

---

### Step 4: Create an EBS Snapshot
1. Go back to the AWS Console ➔ **EC2** ➔ **Volumes**.
2. Select your 5 GiB volume.
3. Click **Actions** ➔ **Create snapshot**.
4. **Description:** `task-ebs-backup-v1`
5. Click **Create snapshot**.
6. On the left menu under *Elastic Block Store*, click **Snapshots** to see your backup stored safely in Amazon S3!

---

## 🛠️ Hands-on Lab 2B: Amazon S3 & Secure Bucket Policies

### Step 1: Create a Secure S3 Bucket
1. Navigate to the **Amazon S3 Console** (`s3.console.aws.amazon.com`).
2. Click the orange **Create bucket** button.
3. **Bucket name:** `task-nalgonda-<your-rollno-or-name>-2026`  
   *(Must be globally unique across all AWS customers worldwide, lowercase letters, numbers, and hyphens).*
4. **AWS Region:** Select `ap-south-1` (Asia Pacific - Mumbai).
5. **Block Public Access settings for this bucket:**
   - Ensure **Block all public access** remains **CHECKED** (Industry Best Practice).
6. **Bucket Versioning:** Keep disabled for now (or Enable for change tracking).
7. **Default Encryption:** Leave as **Server-side encryption with Amazon S3 managed keys (SSE-S3)**.
8. Click **Create bucket**.

---

### Step 2: Upload Files to S3
1. Click on your newly created bucket name.
2. Click the **Upload** button.
3. Click **Add files** and select any sample image, PDF, or text file from your computer.
4. Scroll down and click **Upload**.
5. Once complete, click the uploaded file to view its **Object Overview**, including its S3 URI (`s3://...`) and Object URL.

---

### Step 3: Author & Apply an HTTPS-Only Bucket Policy
Enforce corporate compliance: Any request sent over plain insecure HTTP must be strictly denied.

1. In your bucket, click the **Permissions** tab.
2. Scroll down to the **Bucket policy** section and click **Edit**.
3. In the JSON policy editor, paste the following policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowOnlySecureTransportRequests",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::REPLACE-WITH-YOUR-BUCKET-NAME",
        "arn:aws:s3:::REPLACE-WITH-YOUR-BUCKET-NAME/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

4. ⚠️ **Replace `REPLACE-WITH-YOUR-BUCKET-NAME`** with your actual S3 bucket name.
5. Click **Save changes**.
6. Your S3 bucket now strictly rejects unencrypted communication!

---

## 💡 Quick Summary Checklist for Students

| Storage Question | Answer |
|---|---|
| Need low-latency boot disk for 1 EC2 instance? | **Amazon EBS** (`gp3`) |
| Need a shared drive mounted by 100 EC2 instances simultaneously? | **Amazon EFS** (NFSv4) |
| Need to store images, videos, and backups accessible anywhere? | **Amazon S3** |
| What is the durability of S3 and EFS? | **99.999999999% (11 9's)** |
| What is the most critical S3 security setting? | **Block Public Access (BPA)** |

