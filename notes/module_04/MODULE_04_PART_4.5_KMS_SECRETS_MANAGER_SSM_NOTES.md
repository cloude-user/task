# Module 4 Part 4.5: Data Security, AWS KMS, Secrets Manager & SSM Parameter Store
> **Program:** Telangana Academy for Skill and Knowledge (TASK)  
> **Course Track:** Cloud Software Developer (Module 4: AWS Solutions Architect / Developer DVA-C02)  
> **Topic Focus:** Data Security, Cryptographic Key Architecture, Secrets Management & Centralized Configuration  
> **Document Type:** Master Architecture & Comprehensive Study Guide  
> **Target Audience:** Engineering Students, Cloud Developers & AWS Solutions Architect Candidates  

---

## 📑 Table of Contents
1. [Data Security Fundamentals & The Threat of Plaintext Data](#1-data-security-fundamentals--the-threat-of-plaintext-data)
   - [The Production Security Dilemma](#the-production-security-dilemma)
   - [Encryption at Rest vs. Encryption in Transit](#encryption-at-rest-vs-encryption-in-transit)
   - [The Bank Vault and Personal Safe Analogy](#the-bank-vault-and-personal-safe-analogy)
   - [Core Principle: KMS Controls Keys, Not Customer Data](#core-principle-kms-controls-keys-not-customer-data)
2. [AWS Key Management Service (KMS) Architecture & Key Tiers](#2-aws-key-management-service-kms-architecture--key-tiers)
   - [The Three KMS Key Tiers](#the-three-kms-key-tiers)
   - [Symmetric vs. Asymmetric Keys](#symmetric-vs-asymmetric-keys)
   - [KMS Key Policies & IAM Integration](#kms-key-policies--iam-integration)
3. [Envelope Encryption Deep Dive & The 4 KB Direct Limit](#3-envelope-encryption-deep-dive--the-4-kb-direct-limit)
   - [The Hardware Security Module (HSM) 4 KB Constraint](#the-hardware-security-module-hsm-4-kb-constraint)
   - [Envelope Encryption Architecture (Master Key + Data Key)](#envelope-encryption-architecture-master-key--data-key)
   - [Step-by-Step Two-Key Cryptographic Workflow](#step-by-step-two-key-cryptographic-workflow)
   - [Architecture Diagram: Envelope Encryption Flow](#architecture-diagram-envelope-encryption-flow)
4. [The S3 + KMS Dual-Gate Authorization Model](#4-the-s3--kms-dual-gate-authorization-model)
   - [The Two Independent Authorization Gates](#the-two-independent-authorization-gates)
   - [Why S3 Administrator Access Alone Fails (HTTP 403 Access Denied)](#why-s3-administrator-access-alone-fails-http-403-access-denied)
   - [Architecture Diagram: S3 and KMS Dual-Gate Verification](#architecture-diagram-s3-and-kms-dual-gate-verification)
   - [Step-by-Step Console Verification Walkthrough](#step-by-step-console-verification-walkthrough)
5. [AWS Secrets Manager vs. AWS Systems Manager (SSM) Parameter Store](#5-aws-secrets-manager-vs-aws-systems-manager-ssm-parameter-store)
   - [AWS Secrets Manager: Native Rotation & Enterprise Security](#aws-secrets-manager-native-rotation--enterprise-security)
   - [SSM Parameter Store: Hierarchical Configuration Storage](#ssm-parameter-store-hierarchical-configuration-storage)
   - [Architecture Diagram: Head-to-Head Architectural Comparison](#architecture-diagram-head-to-head-architectural-comparison)
   - [Comprehensive Comparison Matrix & Enterprise Decision Framework](#comprehensive-comparison-matrix--enterprise-decision-framework)
6. [Key Lifecycle, Auditing & Critical Production Guardrails](#6-key-lifecycle-auditing--critical-production-guardrails)
   - [AWS CloudTrail Immutable Auditing](#aws-cloudtrail-immutable-auditing)
   - [Automatic 365-Day Key Rotation Mechanics](#automatic-365-day-key-rotation-mechanics)
   - [Mandatory 7-to-30-Day Waiting Period for Key Deletion](#mandatory-7-to-30-day-waiting-period-for-key-deletion)
   - [Cost Optimization & S3 Bucket Keys](#cost-optimization--s3-bucket-keys)
7. [AWS Solutions Architect Certification & Real-World Interview Scenarios](#7-aws-solutions-architect-certification--real-world-interview-scenarios)
8. [Hands-On Lab Guide (Lab 4.5b: Practical Cryptography & Secrets Management)](#8-hands-on-lab-guide-lab-45b-practical-cryptography--secrets-management)

---

## 1. Data Security Fundamentals & The Threat of Plaintext Data

### The Production Security Dilemma
In modern cloud architectures, every web application, background worker, and API microservice interacts with sensitive data. This includes:
* Database credentials (master usernames, administrative passwords, connection strings).
* Third-party API keys (Stripe payment tokens, Twilio SMS keys, OpenAI API secrets).
* Customer personally identifiable information (Aadhaar cards, PAN numbers, passport details, medical records).

A dangerous anti-pattern frequently observed among junior cloud engineers is **hardcoding credentials directly into source code** (e.g., `settings.py`, `application.properties`) or uploading unencrypted configuration files directly to Amazon S3 buckets. If a developer accidentally pushes that code to a public GitHub repository, automated bots scan and exploit those credentials within seconds. Similarly, if an S3 bucket is mistakenly made public, unencrypted data files are immediately exposed to the entire internet.

### Encryption at Rest vs. Encryption in Transit
AWS enforces two fundamental encryption boundaries:
* **Encryption in Transit:** Protects data packets travelling across networks (between client browsers and cloud endpoints, or between EC2 instances and databases) using **TLS/HTTPS (Transport Layer Security)**. This prevents eavesdropping and man-in-the-middle (MITM) packet sniffing.
* **Encryption at Rest:** Protects data written to physical storage media (Amazon S3 disks, Amazon EBS volumes, Amazon RDS storage, Amazon DynamoDB tables). If an unauthorized actor physically removes or accesses the storage hardware, the data appears as meaningless random gibberish (ciphertext).

### The Bank Vault and Personal Safe Analogy
To understand how AWS structures encryption, consider how a high-security bank branch operates:

1. **The Personal Safe (Your Encrypted Data / Ciphertext):**  
   Imagine you place your property title deeds and gold inside a hardened steel safe in your home. Even if an intruder enters the building, they cannot inspect or read your documents because they cannot breach the locked safe. In AWS, this locked safe represents your **encrypted ciphertext stored inside Amazon S3 or EBS**.
2. **The Bank Vault Keeper (AWS Key Management Service - KMS):**  
   The bank manager does not store your family gold or cash in their personal desk drawers. Instead, the bank operates a centralized, blast-proof vault that securely stores and controls the physical keys required to open the deposit safes. Similarly, **AWS KMS does NOT store your files or databases; KMS stores, manages, and audits the cryptographic keys**.
3. **The Biometric Authorization Check (KMS Key Policy):**  
   To open your safe, you cannot simply show a standard college ID or general office badge (standard S3 permission). You must present your registered biometric thumbprint and official government identity (an explicit `kms:Decrypt` permission in the KMS Key Policy).
4. **The Security Camera Ledger (AWS CloudTrail):**  
   Every time someone approaches the vault to request a key, a 24/7 security camera logs who they are, their exact timestamp, their identity badge number, and their IP address into an immutable, tamper-proof ledger.

> 💡 **Core Architectural Principle:** AWS KMS is a centralized key authority. KMS never stores client business data; it creates, stores, governs, and audits cryptographic keys.

---

## 2. AWS Key Management Service (KMS) Architecture & Key Tiers

AWS Key Management Service (AWS KMS) is a fully managed service that makes it easy to create and control cryptographic keys across more than 100 AWS integrated services and applications. AWS KMS uses Hardware Security Modules (HSMs) validated under **FIPS 140-2 Cryptographic Module Validation Program** to generate and protect keys.

### The Three KMS Key Tiers

| Key Tier | Ownership & Governance | Creation Cost | Rotation Schedule | Key Policy Customization | Typical Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. AWS Owned Keys** | Owned, operated, and managed entirely by AWS. Invisible in the KMS console. | 100% Free | Controlled by AWS internally | Cannot be viewed, edited, or audited | Default internal encryption for DynamoDB tables, SQS queues, and S3. |
| **2. AWS Managed Keys** | Automatically created in your account when you enable encryption in an AWS service (`aws/s3`, `aws/ebs`, `aws/rds`). | Free to create and maintain | Automatically rotated every 365 days by AWS | Visible in console, but Key Policy cannot be altered | Standard, zero-effort encryption when custom access segregation is not required. |
| **3. Customer Managed Keys (CMKs)** | Created, owned, and configured by you. You have total control over permissions and lifecycle. | $1.00 / month per key (+ API request fees) | Configurable automatic rotation (every 365 days) | 100% full control over Key Policy, IAM users, and cross-account access | Strict regulatory compliance, separation of duties, and granular access delegation. |

### Symmetric vs. Asymmetric Keys
* **Symmetric Encryption (AES-256):** Represents 99% of cloud encryption use cases. The exact same 256-bit key is used to both encrypt and decrypt data. The unencrypted key material **never leaves AWS KMS Hardware Security Modules (HSMs)**. All encryption and decryption operations occur inside the HSM boundary.
* **Asymmetric Encryption (RSA / ECC):** Uses a mathematically linked public/private key pair. The Public Key can be exported outside AWS to allow external clients to encrypt data or verify digital signatures, while the Private Key remains locked inside the KMS HSM to perform decryption and signing.

---

## 3. Envelope Encryption Deep Dive & The 4 KB Direct Limit

### The Hardware Security Module (HSM) 4 KB Constraint
A crucial architectural concept tested in AWS Solutions Architect exams and technical interviews is the direct payload size limit of AWS KMS:

> ⚠️ **The 4 KB Limit:** Direct KMS cryptographic APIs (`kms:Encrypt` and `kms:Decrypt`) can only accept plaintext data up to **4 Kilobytes (4,096 bytes)** in size.

KMS HSMs are specialized cryptographic microchips engineered for maximum mathematical security, high transactions-per-second, and zero key leakage. They are not high-throughput file processors. If an application attempted to stream a 50 Gigabyte database backup or a 4 Gigabyte video file over the network to KMS for encryption, network bandwidth would saturate, latency would skyrocket, and the KMS API would be overwhelmed.

### Envelope Encryption Architecture (Master Key + Data Key)
To solve the 4 KB constraint, AWS utilizes **Envelope Encryption**:
1. A **Key Management Service Key (KMS CMK)** acts as the **Master Key** (Key Encryption Key - KEK).
2. A separate, temporary **Data Encryption Key (DEK)** is generated to encrypt the actual large payload locally using high-speed symmetric AES-256 algorithms.
3. The Plaintext Data Key is then encrypted by the Master Key, and the resulting **Encrypted Data Key** is stored alongside the encrypted data file.

```
+----------------------------------------------------------------------------------------------------+
|                                    ENVELOPE ENCRYPTION MECHANICS                                   |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  [ AWS KMS Cloud Vault ]                                                                           |
|       |                                                                                            |
|       | 1. GenerateDataKey(KeyId='student-demo-key')                                               |
|       v                                                                                            |
|  KMS returns TWO keys:                                                                             |
|       |                                                                                            |
|       +---> [ Plaintext Data Key (RAM) ] --------+                                                 |
|       |                                          |                                                 |
|       +---> [ Encrypted Data Key (Ciphertext) ]  |                                                 |
|                                                  v                                                 |
|  [ Client Application / RAM ]             [ Local File (10 GB) ]                                   |
|       |                                          |                                                 |
|       | 2. AES-256 Local Encryption              v                                                 |
|       +----------------------------------> [ Encrypted File (10 GB) ]                               |
|       |                                          |                                                 |
|       | 3. PURGE Plaintext Data Key from RAM!    |                                                 |
|       v                                          v                                                 |
|  [ Storage: Amazon S3 Bucket ]            [ Encrypted Object Metadata ]                            |
|       • Encrypted File (Ciphertext)              |                                                 |
|       • Encrypted Data Key (Stored with File) <--+                                                 |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

### Step-by-Step Two-Key Cryptographic Workflow

#### The Encryption Workflow:
1. **Generate Data Key:** The application calls KMS API: `GenerateDataKey(KeyId="alias/student-demo-key", KeySpec="AES_256")`.
2. **KMS Response:** KMS generates a high-entropy 256-bit symmetric key. It returns two components:
   - A **Plaintext Data Key** in clear memory.
   - An **Encrypted Data Key** (the data key encrypted under the Customer Master Key).
3. **Local Encryption:** The client application uses the Plaintext Data Key to encrypt the large dataset (e.g., a 10 GB file) locally in memory.
4. **RAM Zeroization:** The application **permanently erases (zeroizes) the Plaintext Data Key from RAM** immediately after encryption completes.
5. **Storage Packaging:** The application saves the Encrypted File along with the Encrypted Data Key in persistent storage (e.g., S3 object metadata). The Master Key remains safe in KMS.

#### The Decryption Workflow:
1. **Retrieve Package:** The client downloads the Encrypted File and the Encrypted Data Key from S3.
2. **KMS Decrypt Request:** The client sends the Encrypted Data Key to KMS: `Decrypt(CiphertextBlob=EncryptedDataKey)`.
3. **KMS Authorization & Decryption:** KMS verifies that the caller has `kms:Decrypt` permission in the Key Policy, decrypts the data key inside its HSM, and returns the **Plaintext Data Key**.
4. **Local Payload Decryption:** The client decrypts the 10 GB file in memory using the Plaintext Data Key.
5. **Wipe Memory:** The client wipes the Plaintext Data Key from memory.

![KMS Envelope Encryption Flow](diagrams/01_kms_envelope_encryption_flow.png)

---

## 4. The S3 + KMS Dual-Gate Authorization Model

### The Two Independent Authorization Gates
When sensitive data is stored in Amazon S3 using AWS KMS Server-Side Encryption (SSE-KMS), access is controlled by **two distinct, independent security boundaries**:

```
+---------------------------------------------------------------------------------------------+
|                             S3 + KMS DUAL-GATE EVALUATION PIPELINE                          |
+---------------------------------------------------------------------------------------------+
|                                                                                             |
|  Client Request: s3:GetObject on 'secret.txt'                                               |
|       |                                                                                     |
|       v                                                                                     |
|  [ GATE 1: S3 STORAGE BOUNDARY ]                                                            |
|       • Does IAM Policy allow 's3:GetObject'?                                               |
|       • Does S3 Bucket Policy allow access?                                                 |
|       • Is S3 Public Access Blocked?                                                        |
|            |                                                                                |
|            +--- [ NO ]  =========> HTTP 403 Forbidden (S3 Access Denied)                    |
|            |                                                                                |
|            +--- [ YES ] =========> Pass to Gate 2                                           |
|                                         |                                                   |
|                                         v                                                   |
|                              [ GATE 2: KMS CRYPTOGRAPHIC BOUNDARY ]                         |
|                                   • Does KMS Key Policy allow 'kms:Decrypt'?                |
|                                   • Does IAM Policy grant 'kms:Decrypt' on Key ARN?         |
|                                        |                                                    |
|                                        +--- [ NO ]  ====> HTTP 403 Forbidden (KMS Denied)  |
|                                        |                                                    |
|                                        +--- [ YES ] ====> Plaintext Returned to Client!     |
|                                                                                             |
+---------------------------------------------------------------------------------------------+
```

### Why S3 Administrator Access Alone Fails
A common security vulnerability in corporate AWS accounts occurs when junior administrators or third-party contractors are granted `AmazonS3FullAccess`. Organizations fear that such users can inspect every sensitive document, payroll spreadsheet, or database export in the company's S3 buckets.

**SSE-KMS completely neutralizes this risk through Separation of Duties:**
* Even if a user has `AdministratorAccess` or `AmazonS3FullAccess`, they can only download the encrypted bytes.
* When S3 attempts to decrypt the file, it calls KMS on behalf of the user. If the user's IAM principal is **NOT explicitly listed under the KMS Key Policy's Key Users**, KMS rejects the operation with `AccessDeniedException`.
* S3 then terminates the request and returns an **HTTP 403 Access Denied** response to the user.

![S3 KMS Dual Gate Authorization](diagrams/02_kms_s3_dual_authorization_gate.png)

### Step-by-Step Console Verification Walkthrough
To verify this dual-gate mechanism:
1. Create a Customer Managed Key named `student-demo-key` in KMS.
2. In S3, upload a file named `secret.txt` containing confidential credentials.
3. In object properties, select **Server-side encryption settings** → Choose **AWS Key Management Service key (SSE-KMS)** → Select `student-demo-key`.
4. Download and view the file: Notice that it opens normally because your user identity is defined as a Key User in the KMS Key Policy.
5. Open KMS → Select `student-demo-key` → Switch to the **Key Policy** tab → Remove your user ARN from the `kms:Decrypt` action block (or simulate using an IAM user with `AmazonS3FullAccess` but no KMS policy).
6. Return to S3 and attempt to open `secret.txt`: **The request fails immediately with HTTP 403 Access Denied!** This proves that storage authorization without cryptographic authorization is completely powerless.

---

## 5. AWS Secrets Manager vs. AWS Systems Manager (SSM) Parameter Store

AWS provides two specialized services for externalizing application configurations and secrets. Understanding when to use each is essential for system architecture and certification.

![Secrets Manager vs SSM Parameter Store](diagrams/03_secrets_manager_vs_ssm_parameter_store.png)

### AWS Secrets Manager: Native Rotation & Enterprise Security
AWS Secrets Manager is purpose-built for managing database credentials, API tokens, and OAuth keys that require strict lifecycle security and automated credential cycling:
* **Built-in Automatic Rotation:** Integrates natively with AWS Lambda to automatically rotate database credentials for Amazon RDS (MySQL, PostgreSQL, Oracle, SQL Server), Amazon Aurora, and Amazon DocumentDB on a scheduled frequency (e.g., every 30 days) without downtime.
* **Cross-Account Access & Multi-Region Replication:** Secrets can be replicated synchronously across multiple AWS regions to support disaster recovery and global multi-region microservices.
* **Cost Structure:** \$0.40 per secret per month + \$0.05 per 10,000 API calls.

### SSM Parameter Store: Hierarchical Configuration Storage
AWS Systems Manager (SSM) Parameter Store provides centralized storage for application configuration values, environment variables, feature flags, license codes, and secrets:
* **Hierarchical Tree Organization:** Parameters are organized using filesystem-like slash paths:
  - `/ecommerce/prod/database/endpoint`
  - `/ecommerce/prod/payment/timeout_seconds`
  - `/ecommerce/dev/feature_flags/new_checkout`
* **Three Parameter Types:**
  1. `String`: Plain text configurations (e.g., URL endpoints, port numbers).
  2. `StringList`: Comma-separated lists (e.g., `us-east-1a,us-east-1b,us-east-1c`).
  3. `SecureString`: Sensitive values encrypted at rest using an AWS KMS key.
* **Cost Structure:** The **Standard Tier is 100% Free** (up to 10,000 parameters per account/region with values up to 4 KB each).

### Comprehensive Comparison Matrix & Enterprise Decision Framework

| Evaluation Criteria | AWS Secrets Manager | AWS Systems Manager Parameter Store |
| :--- | :--- | :--- |
| **Primary Architectural Purpose** | Complex secrets, database credentials, API tokens requiring automated rotation | Centralized application configuration, environment variables, hierarchical settings |
| **Automated Credential Rotation** | **Native Built-in Support** via AWS Lambda out-of-the-box (RDS, Aurora, Redshift) | **No native rotation** (Requires custom manual Lambda triggers via EventBridge) |
| **Cost / Pricing Model** | **\$0.40 / secret / month** + \$0.05 per 10,000 API calls | **Standard Tier: 100% FREE**; Advanced Tier: \$0.05 / param / month |
| **Maximum Storage Size** | Up to **64 KB** per secret | Standard Tier: **4 KB**; Advanced Tier: **8 KB** |
| **Random Password Generation** | Native CLI / SDK generator with complexity rules | No native random generator |
| **Multi-Region Secret Replication** | Built-in 1-click cross-region replication | Manual synchronization required |
| **Encryption Support** | Encrypted by default with KMS (Customer Managed or AWS Managed) | `SecureString` type encrypted with KMS; `String` stored in plaintext |
| **Enterprise Decision Rule** | Use for **RDS database passwords & high-value secrets** requiring auto-rotation | Use for **general application configs, URLs, and secrets** without auto-rotation |

---

## 6. Key Lifecycle, Auditing & Critical Production Guardrails

### AWS CloudTrail Immutable Auditing
Every cryptographic request executed against AWS KMS generates an immutable event in AWS CloudTrail:
* When an S3 object is retrieved, CloudTrail logs a `kms:Decrypt` event.
* The event record includes:
  - The exact ARN of the IAM user or role who initiated the request.
  - The precise timestamp to the millisecond.
  - The Source IP Address and User-Agent.
  - The Key ARN utilized.
  - The specific AWS service that proxied the request (e.g., `s3.amazonaws.com`).
This enables corporate security teams to perform compliance forensics and satisfy stringent regulatory audits (SOC-2, ISO 27001, HIPAA, PCI-DSS).

### Automatic 365-Day Key Rotation Mechanics
When automatic key rotation is enabled for a Customer Managed Key (CMK):
* AWS KMS automatically generates a new cryptographic backing key every **365 days** (or custom intervals down to 90 days).
* **Crucial Architectural Behavior:** KMS retains all older backing keys indefinitely.
* You do **NOT** need to re-encrypt existing files or EBS volumes! When older data is read, KMS automatically selects the specific backing key that was used during that file's original encryption.
* The Key ARN, Key ID, Key Policy, and IAM permissions remain 100% unchanged.

### Mandatory 7-to-30-Day Waiting Period for Key Deletion
Accidental deletion of a KMS key is catastrophic: any data encrypted under that key becomes permanently and irreversibly unrecoverable.

To eliminate accidental data destruction, AWS strictly prohibits immediate key deletion:
* When an administrator schedules key deletion, AWS KMS forces a mandatory **waiting period between 7 and 30 days** (default: 30 days).
* During this waiting period, the key transitions to the `PendingDeletion` state.
* While in `PendingDeletion`, the key cannot be used to encrypt or decrypt data.
* If the deletion was accidental, the administrator can cancel the deletion at any time before the timer expires using the `kms:CancelKeyDeletion` API, instantly restoring the key to the `Enabled` state.

### Cost Optimization & S3 Bucket Keys
* Each active Customer Managed Key costs **\$1.00 per month**. Creating 100 distinct CMKs for individual files wastes \$100/month. Best practice is to use shared CMKs segregated by application domain or security tier.
* Every S3 object read/write invokes a KMS API call (\$0.03 per 10,000 requests). For buckets processing millions of requests, this accumulates substantial fees.
* Enabling **Amazon S3 Bucket Keys** reduces KMS request traffic and costs by up to **99%** by creating a short-lived bucket-level key that handles object encryption locally in S3.

---

## 7. AWS Solutions Architect Certification & Real-World Interview Scenarios

### Scenario 1: The S3 Access Denied Mystery
* **Question:** A junior developer is assigned the AWS managed policy `AmazonS3FullAccess`. However, when attempting to download an object from `s3://company-finance-reports/q3_earnings.xlsx`, the developer receives an HTTP 403 Access Denied error. All other objects in adjacent buckets download without issue. What is the root cause and the required fix?
* **Architectural Explanation:** The object is encrypted with SSE-KMS using a Customer Managed Key. While the developer has full S3 permissions (passing Gate 1), the KMS Key Policy does not include the developer's IAM ARN in the `kms:Decrypt` action block (failing Gate 2). The administrator must update the KMS Key Policy or attach an IAM policy granting `kms:Decrypt` on that specific Key ARN.

### Scenario 2: Automated RDS Credential Rotation
* **Question:** A financial application requires its Amazon RDS PostgreSQL master password to be rotated every 30 days in compliance with banking regulations. The engineering team wants zero downtime and zero manual administrative intervention. Which service should they choose?
* **Architectural Explanation:** **AWS Secrets Manager**. Secrets Manager has native out-of-the-box integration with AWS Lambda to rotate Amazon RDS credentials automatically on a 30-day schedule, updating both the database user account and the stored secret atomically.

### Scenario 3: Microservice Configuration Fleet at Zero Cost
* **Question:** A software company operates 150 microservices on AWS. Each microservice requires 20 environment configuration settings (endpoints, log levels, retry counts). The architecture team refuses to pay monthly secret storage fees for non-sensitive configuration values. Which service should be used?
* **Architectural Explanation:** **AWS Systems Manager Parameter Store (Standard Tier)**. The Standard Tier allows up to 10,000 parameters per region for **100% Free**. Configuration strings are organized hierarchically (`/microservices/service-a/log_level`) and retrieved via the AWS SDK at zero cost.

### Scenario 4: Encrypting a 15 GB Video File with KMS
* **Question:** A developer attempts to execute `aws kms encrypt --key-id <key-id> --plaintext fileb://video.mp4` on a 15 GB video file. The command crashes immediately. Why did it fail, and what is the proper AWS architectural approach?
* **Architectural Explanation:** The `kms:Encrypt` API has a hard direct payload ceiling of **4 KB**. The developer must implement **Envelope Encryption**: call `kms:GenerateDataKey` to obtain a temporary Data Encryption Key (DEK), encrypt the video file locally using AES-256, erase the plaintext DEK from memory, and store the encrypted DEK alongside the video.

### Scenario 5: Accidental Key Deletion Recovery
* **Question:** A cloud engineer accidentally clicks "Delete key" on the production KMS CMK. Production workloads immediately report cryptographic errors. Can the key be restored, and how?
* **Architectural Explanation:** Yes. AWS KMS enforces a mandatory 7-to-30-day waiting period. The key is in the `PendingDeletion` state. The administrator must execute `aws kms cancel-key-deletion --key-id <key-id>` or click "Cancel key deletion" in the console. The key will immediately return to the `Enabled` state, restoring application operations.

---

## 8. Hands-On Lab Guide (Lab 4.5b: Practical Cryptography & Secrets Management)

### Lab Objective
In this hands-on lab, you will configure end-to-end data security controls on AWS:
1. Create a Customer Managed Key (CMK) with an alias and custom key policy.
2. Upload and encrypt a sensitive credential file in Amazon S3 using SSE-KMS.
3. Validate the Dual-Gate Security Model by testing access permissions and observing HTTP 403 errors.
4. Store and retrieve sensitive credentials in AWS Secrets Manager.
5. Create and query hierarchical configuration parameters in SSM Parameter Store (`SecureString`).
6. Execute zero-spend teardown and schedule key deletion.

### Task 1: Create a Customer Managed Key (CMK)
1. Open the [AWS Management Console](https://console.aws.amazon.com/) → Navigate to **Key Management Service (KMS)**.
2. In the navigation pane, choose **Customer managed keys** → Click **Create key**.
3. **Configure Key:**
   - Key type: **Symmetric**
   - Key usage: **Encrypt and decrypt**
   - Advanced options: Leave Key material origin as **KMS** → Click **Next**.
4. **Add Labels:**
   - Alias: `student-demo-key`
   - Description: `TASK Module 4 Demo Key for Data Security & Cryptography` → Click **Next**.
5. **Define Key Administrators:**
   - Select your current IAM User or Admin Role → Click **Next**.
6. **Define Key Users:**
   - Select your current IAM User → Click **Next**.
7. Review the generated JSON Key Policy and click **Finish**. Note the assigned **Key ARN**.

### Task 2: Upload and Encrypt a Sensitive File in Amazon S3
1. Open the **Amazon S3 Console** → Select or create a lab bucket (e.g., `task-security-lab-<your-name>`).
2. On your local machine, create a test file named `credentials.txt` containing:
   ```text
   TASK CLOUD DEVELOPER SENSITIVE CONFIGURATION:
   DB_HOST=prod-db.task.internal
   DB_USER=masteradmin
   DB_PASSWORD=SuperSecretKMSPassword2026!
   ```
3. In your S3 bucket, click **Upload** → Add `credentials.txt`.
4. Expand **Properties** → Scroll to **Server-side encryption settings**:
   - Select **Specify an encryption key**.
   - Encryption type: **AWS Key Management Service key (SSE-KMS)**.
   - Select **Choose from your AWS KMS keys** → Select `student-demo-key`.
   - Bucket Key: Select **Enable** (optimizes cost).
5. Click **Upload**.

### Task 3: The Dual-Gate Security Verification
1. Click on `credentials.txt` in the S3 bucket → Click **Open**.
2. Notice that the file downloads and displays plaintext credentials cleanly. (Both Gate 1 and Gate 2 succeeded).
3. Now test Gate 2 isolation:
   - Navigate back to **AWS KMS** → Click `student-demo-key`.
   - Select the **Key Policy** tab → Click **Edit**.
   - Locate the `Key Users` statement and temporarily comment out or delete your user ARN, or change `"Effect": "Allow"` to `"Effect": "Deny"` for `kms:Decrypt`.
   - Click **Save changes**.
4. Return to **Amazon S3** → Click **Open** on `credentials.txt`.
5. **Observe the Result:** S3 immediately throws an **HTTP 403 Forbidden (Access Denied)** error!
6. Restore the Key Policy to `"Effect": "Allow"` before proceeding.

### Task 4: Store Database Credentials in AWS Secrets Manager
1. Navigate to **AWS Secrets Manager** → Click **Store a new secret**.
2. **Secret type:** Choose **Credentials for Amazon RDS database** (or **Other type of secret**).
3. Under Key/value pairs, add:
   - Key: `username` | Value: `task_admin`
   - Key: `password` | Value: `SecureTaskVaultPass#2026`
   - Key: `dbname`   | Value: `production_task_db`
4. Encryption key: Select `student-demo-key` (or default `aws/secretsmanager`) → Click **Next**.
5. **Secret name:** Enter `app/prod/database_credentials` → Click **Next**.
6. **Automatic Rotation:** Keep disabled for this lab (observe the 30-day rotation settings) → Click **Next**.
7. Review and click **Store**.
8. Click on your stored secret → Click **Retrieve secret value** to verify stored JSON credentials.

### Task 5: Store Application Configuration in SSM Parameter Store
1. Navigate to **AWS Systems Manager** → In the left sidebar, click **Parameter Store**.
2. Click **Create parameter**.
3. **Parameter details:**
   - Name: `/ecommerce/prod/payment_api_url`
   - Type: **String**
   - Value: `https://api.payments.task.gov.in/v2/checkout` → Click **Create parameter**.
4. Create a second sensitive parameter:
   - Name: `/ecommerce/prod/stripe_secret_key`
   - Type: **SecureString**
   - KMS Key Source: Select **My current account** → Choose `student-demo-key`.
   - Value: `mock_stripe_secret_key_demo_only`
5. Click **Create parameter**.
6. In the Parameter Store list, observe that the `String` parameter displays its plain value, while the `SecureString` parameter masks its value with asterisks (`******`) until explicit decryption is requested.

### Task 6: Zero-Spend Clean-Up Protocol
To avoid ongoing charges on your AWS billing account:
1. **Secrets Manager:** Select `app/prod/database_credentials` → Actions → **Delete secret** → Select 7 days waiting period (or click "Delete immediately without recovery").
2. **SSM Parameter Store:** Select the two created parameters → Click **Delete**.
3. **Amazon S3:** Delete `credentials.txt` from your lab bucket.
4. **AWS KMS:** Select `student-demo-key` → Key actions → **Schedule key deletion** → Enter **7 days** (the minimum allowed waiting period) → Confirm deletion.

---
*© Telangana Academy for Skill and Knowledge (TASK) — Cloud Software Developer Curriculum*
