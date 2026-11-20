# Lab 4.5b: AWS Data Security — KMS, Secrets Manager & SSM Parameter Store
> **Course Track:** Cloud Software Developer (Module 4: AWS Solutions Architect)  
> **Lab Focus:** Hands-On Cryptography, SSE-KMS Dual-Gate Testing, Secrets Lifecycle & Centralized Config  
> **Prerequisites:** Active AWS Account, IAM permissions for S3, KMS, Secrets Manager, and Systems Manager.  

---

## 🎯 Lab Objectives
By the end of this lab, you will have successfully demonstrated:
1. Creating a Customer Managed Key (CMK) in AWS KMS with alias `student-demo-key`.
2. Securing an S3 object using SSE-KMS Server-Side Encryption.
3. Validating the Dual-Gate Authorization Model (proving S3 Admin cannot read without `kms:Decrypt`).
4. Storing production database credentials in AWS Secrets Manager.
5. Managing hierarchical microservice configuration using SSM Parameter Store (`String` and `SecureString`).
6. Executing a zero-spend clean-up and scheduling KMS key deletion.

---

## 🛠️ Step-by-Step Practical Instructions

### Task 1: Create a Customer Managed Key (CMK)
1. Open the **AWS Management Console** → Search for and select **Key Management Service (KMS)**.
2. In the navigation pane on the left, click **Customer managed keys** → Click **Create key**.
3. In **Step 1 (Configure key)**:
   - Key type: **Symmetric**
   - Key usage: **Encrypt and decrypt**
   - Advanced options: Leave default (KMS) → Click **Next**.
4. In **Step 2 (Add labels)**:
   - Alias: `student-demo-key`
   - Description: `TASK Module 4 Demo Key for Data Security & Cryptography` → Click **Next**.
5. In **Step 3 (Define key administrative permissions)**:
   - Select your current IAM User or role → Click **Next**.
6. In **Step 4 (Define key usage permissions)**:
   - Select your current IAM User or role → Click **Next**.
7. In **Step 5 (Review)**:
   - Review the JSON policy and click **Finish**.
   - Note the **Key ID** and **Key ARN**.

### Task 2: Upload and Encrypt an S3 Object with SSE-KMS
1. Navigate to the **Amazon S3 Console** → Open your existing lab bucket (or create `task-data-security-<your-name>`).
2. On your computer, open Notepad and create a file called `secret_credentials.txt`:
   ```text
   CONFIDENTIAL TASK APPLICATION CREDENTIALS:
   DATABASE_ENGINE=postgresql
   DATABASE_HOST=prod-cluster.c7z9k.ap-south-1.rds.amazonaws.com
   DATABASE_USER=db_superadmin
   DATABASE_PASSWORD=TaskCloudEngineer#2026!
   ```
3. In the S3 Console, click **Upload** → Add `secret_credentials.txt`.
4. Expand the **Properties** section:
   - Scroll down to **Server-side encryption settings**.
   - Select **Specify an encryption key**.
   - Encryption type: **AWS Key Management Service key (SSE-KMS)**.
   - Choose **Choose from your AWS KMS keys** → Select `student-demo-key`.
   - Bucket Key: Select **Enable**.
5. Click **Upload**.

### Task 3: The Dual-Gate Security Test (The "Aha!" Moment)
1. In the S3 Console, click on `secret_credentials.txt` → Click **Open**.
   - *Result:* The file opens cleanly and displays your database credentials. (Gate 1 and Gate 2 both passed).
2. Now, simulate revoking cryptographic access:
   - Open **AWS KMS** in a new browser tab → Click **Customer managed keys** → Click `student-demo-key`.
   - Switch to the **Key policy** tab → Click **Edit**.
   - Find your IAM User ARN in the `"Statement"` for Key Users and delete the `"kms:Decrypt"` permission, or add an explicit `"Effect": "Deny"` statement for your user on `"kms:Decrypt"`.
   - Click **Save changes**.
3. Return to **Amazon S3** and refresh the page → Click **Open** on `secret_credentials.txt`:
   - *Result:* **HTTP 403 Forbidden / Access Denied!**
   - *Core Lesson:* Even if you have full S3 administrator permissions, without cryptographic permission in the KMS Key Policy, you cannot view the data.
4. Edit the KMS Key Policy and remove the Deny statement so your user can decrypt once again.

### Task 4: Store Credentials in AWS Secrets Manager
1. Navigate to the **AWS Secrets Manager** Console → Click **Store a new secret**.
2. **Secret type:** Choose **Other type of secret**.
3. In the **Key/value pairs** table, enter:
   - Key: `api_key` | Value: `sec_live_994820194820`
   - Key: `jwt_secret` | Value: `jwt_super_token_hash_2026`
4. Encryption key: Select `student-demo-key` → Click **Next**.
5. **Secret name:** Enter `ecommerce/prod/payment_gateway` → Click **Next**.
6. **Configure rotation:** Leave disabled for this quick demo → Click **Next**.
7. Review and click **Store**.
8. Click on your secret → Click **Retrieve secret value** to inspect the encrypted payload.

### Task 5: Store Hierarchical Config in SSM Parameter Store
1. Open **AWS Systems Manager** → In the left navigation, select **Parameter Store**.
2. Click **Create parameter**.
3. Create Parameter 1 (Plaintext Configuration):
   - Name: `/ecommerce/prod/frontend/cdn_url`
   - Description: `Production CloudFront CDN Endpoint`
   - Tier: **Standard**
   - Type: **String**
   - Value: `https://d111111abcdef8.cloudfront.net`
   - Click **Create parameter**.
4. Click **Create parameter** again to create Parameter 2 (Encrypted Secret):
   - Name: `/ecommerce/prod/backend/jwt_private_key`
   - Tier: **Standard**
   - Type: **SecureString**
   - KMS Key Source: Select **My current account** → Choose `student-demo-key`.
   - Value: `MIIEowIBAAKCAQEA0Y9X7e...private_rsa_key`
   - Click **Create parameter**.
5. Observe the Parameter Store list: Notice how `SecureString` hides the sensitive value behind `******`.

### Task 6: Zero-Spend Clean-Up Protocol
1. **Secrets Manager:** Select `ecommerce/prod/payment_gateway` → Actions → **Delete secret** → Click **Delete immediately**.
2. **SSM Parameter Store:** Select both created parameters → Click **Delete**.
3. **Amazon S3:** Delete `secret_credentials.txt` from your bucket.
4. **AWS KMS:** Select `student-demo-key` → Key actions → **Schedule key deletion** → Enter **7 days** → Click **Schedule deletion**.

---
*© Telangana Academy for Skill and Knowledge (TASK) — Lab 4.5b*
