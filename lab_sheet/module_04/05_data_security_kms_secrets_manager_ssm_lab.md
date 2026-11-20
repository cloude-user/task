# Lab 4.5b: Data Security, AWS KMS, Secrets Manager & SSM Parameter Store
> **Course Track:** Cloud Software Developer (Module 4: AWS Solutions Architect)  
> **Lab Code:** `LAB-4.5b`  
> **Objective:** Create a Customer Managed KMS Key (CMK), enforce S3 SSE-KMS encryption, demonstrate dual-authorization access denial, store secrets in SSM Parameter Store & Secrets Manager, and schedule key deletion.  
> **Estimated Duration:** 40 Minutes  
> **Prerequisites:** Active AWS Account (Free Tier), IAM User with Administrative permissions.

---

## 🛠️ Lab Architecture Overview

In this lab, you will validate enterprise-grade cloud data security:
1. **Part 1:** Provision an AWS KMS Customer Managed Key (CMK) with custom alias.
2. **Part 2:** Enforce Server-Side Encryption (SSE-KMS) on an Amazon S3 object.
3. **Part 3:** Conduct the "Aha!" Security Gate experiment by revoking `kms:Decrypt` access.
4. **Part 4:** Create and query an SSM Parameter Store `SecureString` parameter.
5. **Part 5:** Safely schedule KMS key deletion to maintain $0.00 zero-bill compliance.

---

## 📋 Step-by-Step Lab Instructions

### Part 1: Provision a Customer Managed Key (CMK)
1. Log in to the **AWS Management Console** in your active region (e.g. `ap-south-1` Mumbai or `us-east-1`).
2. Search for **KMS** in the top search bar and open **Key Management Service**.
3. In the left panel, click **Customer managed keys** → Click **Create key**.
4. Configure Step 1 (Configure key):
   * Key type: **Symmetric**
   * Key usage: **Encrypt and decrypt**
   * Advanced options: Keep defaults (KMS origin) → Click **Next**.
5. Configure Step 2 (Add labels):
   * Alias: `student-demo-key`
   * Description: `Lab 4.5b Customer Managed Encryption Key` → Click **Next**.
6. Configure Step 3 (Define key administrative permissions):
   * Select your current IAM User / Role as the Key Administrator → Click **Next**.
7. Configure Step 4 (Define key usage permissions):
   * Select your current IAM User as the Key User → Click **Next**.
8. Configure Step 5 (Review):
   * Inspect the generated JSON key policy statement.
   * Notice the `"Action": ["kms:Encrypt", "kms:Decrypt", ...]` statement tied to your user ARN.
   * Click **Finish**.

---

### Part 2: Secure an S3 Object with SSE-KMS
1. Navigate to the **Amazon S3** console.
2. Select an existing bucket (or create a temporary bucket named `task-kms-lab-[your-name]`).
3. Prepare a local test file on your computer named `secret_credentials.txt` containing:
   ```text
   PRODUCTION APPLICATION CONFIG:
   DATABASE_HOST=db.task-internal.net
   DATABASE_PORT=5432
   MASTER_PASSWORD=SuperSecretKMSPassword#2026
   ```
4. Click **Upload** → Select `secret_credentials.txt`.
5. Expand **Properties** → Scroll to **Server-side encryption settings**:
   * Select **Specify an encryption key**.
   * Select **AWS Key Management Service key (SSE-KMS)**.
   * Key: Choose **Choose from your AWS KMS keys** → Select `student-demo-key`.
   * Bucket Key: Select **Enable** (recommended best practice to reduce KMS request cost).
6. Click **Upload**.

---

### Part 3: The "Aha!" Security Verification (Separation of Duty)
1. In the S3 console, click `secret_credentials.txt` → Click **Open**.
   * **Verification:** The file opens cleanly in your browser.
2. Now open a new browser tab and navigate to **AWS KMS** → Select `student-demo-key`.
3. Click the **Key policy** tab → Click **Edit**.
4. Scroll to the statement granting `"kms:Decrypt"` to your IAM user.
5. Temporarily delete your user ARN from the `"Principal"` block (or change `"kms:Decrypt"` to `"kms:DisableKey"`), then click **Save changes**.
6. Switch back to your S3 tab and click **Open** or **Download** on `secret_credentials.txt`.
7. **Expected Result:**
   * Your browser displays `HTTP 403 Forbidden: Access Denied`.
   * **Critical Learning:** Even if an attacker compromises S3 storage permissions, they cannot read data without explicit authorization from the KMS Key Policy!

---

### Part 4: Storing Secrets in AWS SSM Parameter Store
1. In the top search bar, search for **Systems Manager** → Open **Systems Manager**.
2. In the left navigation, scroll to **Application Management** → Click **Parameter Store**.
3. Click **Create parameter**.
4. Configure the parameter:
   * **Name:** `/taskapp/production/db_password` (Hierarchical naming)
   * **Description:** `Production Database Password`
   * **Tier:** **Standard** (Free tier)
   * **Type:** Select **SecureString**
   * **KMS Key source:** Select **My current account** → Choose `student-demo-key` (or default `alias/aws/ssm`).
   * **Value:** `ProdDbPass_9872!#`
5. Click **Create parameter**.
6. In the list, click `/taskapp/production/db_password` → Observe that the value is masked (`*****`).
7. Click **Show** to decrypt the value via KMS on demand.

---

### Part 5: Mandatory Resource Cleanup (Zero-Spend Guardrail)
1. In **Amazon S3**:
   * Delete the object `secret_credentials.txt`.
   * Empty and delete the bucket if created solely for this lab.
2. In **AWS Systems Manager Parameter Store**:
   * Select `/taskapp/production/db_password` → Click **Delete**.
3. In **AWS KMS**:
   * Select `student-demo-key` → Click **Key actions** → **Schedule key deletion**.
   * Waiting period: Enter `7` days (AWS minimum enforced safety window).
   * Confirm and schedule deletion.
