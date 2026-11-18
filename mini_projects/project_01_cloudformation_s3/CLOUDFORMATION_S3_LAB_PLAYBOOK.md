# Student Lab Playbook: Deploying Enterprise S3 via AWS CloudFormation
> **Program:** TASK Telangana · Cloud Software Developer  
> **Trainer:** Sundeep Hiremat | Nalgonda Center  
> **Course Track:** Module 3 — Infrastructure as Code (IaC) & S3 Automation  
> **Target Audience:** Engineering Students & Cloud Software Trainees  

---

## 🎯 Lab Objectives

In this hands-on lab, every student will:
1. Validate a CloudFormation YAML template locally before touching the cloud.
2. Deploy a complete, enterprise-grade S3 bucket stack using both the **AWS Management Console** and the **AWS CLI**.
3. Inspect and verify security configurations: **AES256 Server-Side Encryption**, **Object Versioning**, **Public Access Block**, and **Lifecycle Tiering**.
4. Test and prove the **HTTPS-Only Enforcing Bucket Policy**.
5. Perform an enterprise **Drift Detection** test to catch out-of-band console changes.
6. Perform a safe **Stack Update** using a **CloudFormation Change Set**.
7. Execute a clean, automated stack teardown.

---

## 🏗️ Architecture Overview

```
                      +------------------------------------------------------+
                      |      AWS CLOUDFORMATION TEMPLATE                     |
                      |      (s3_production_bucket.yaml)                     |
                      +------------------------------------------------------+
                                                 |
                                                 v
                      +------------------------------------------------------+
                      |            CLOUDFORMATION STACK                      |
                      |       (sundeep-s3-production-stack)                  |
                      +------------------------------------------------------+
                               /                                    \
                              v                                      v
    +------------------------------------+          +------------------------------------+
    |      AWS::S3::Bucket               |          |       AWS::S3::BucketPolicy        |
    |  - SSE-S3 AES256 Encryption        |          |  - Denies HTTP (Non-SSL) requests  |
    |  - Object Versioning: Enabled      |          |  - Allows only HTTPS (TLS 1.2+)    |
    |  - S3 Public Access Block (All 4)  |          +------------------------------------+
    |  - Lifecycle: IA(30d) -> G(90d)    |
    |  - CORS Configuration Enabled      |
    +------------------------------------+
```

---

## 🛠️ Step-by-Step Execution Playbook

---

### Step 1: Validate the YAML Template Syntax

Before launching a stack, professional cloud engineers always validate their templates locally to ensure there are no indentation or syntax errors.

#### Method A: Using AWS CLI (Terminal)
Open your terminal (PowerShell or Bash) and run:
```bash
aws cloudformation validate-template \
  --template-body file://s3_production_bucket.yaml \
  --region ap-south-1
```
* **Expected Output:** AWS returns a JSON summary listing the parameters and description:
  ```json
  {
      "Parameters": [
          {
              "ParameterKey": "BucketBaseName",
              "DefaultValue": "task-nalgonda",
              "NoEcho": false,
              "Description": "Unique prefix for the S3 bucket..."
          },
          ...
      ],
      "Description": "TASK Telangana Cloud Software Developer Batch..."
  }
  ```

---

### Step 2: Deploy via the AWS Management Console

1. Log in to the [AWS Management Console](https://console.aws.amazon.com/) in the **Asia Pacific (Mumbai) `ap-south-1`** region.
2. Search for **CloudFormation** in the top search bar and click on it.
3. Click the orange **Create stack** button (top right) and select **With new resources (standard)**.

#### Screen 1: Create stack
* **Prerequisite - Prepare template:** Select `Template is ready`.
* **Specify template:** Select `Upload a template file`.
* Click **Choose file** and select your local file: `s3_production_bucket.yaml`.
* Click **Next**.

#### Screen 2: Specify stack details
* **Stack name:** Enter `myname-s3-prod-stack` (e.g., `hemanth-s3-prod-stack` or `saikiran-s3-prod-stack`).
* **Parameters:**
  * **EnvironmentName:** Select `dev` (or `prod`).
  * **BucketBaseName:** Enter `task-nalgonda-<yourname>` (e.g., `task-nalgonda-hemanth`).
  * **EnableVersioning:** Leave as `Enabled`.
  * **TransitionToStandardIADays:** `30`.
  * **TransitionToGlacierDays:** `90`.
  * **ObjectExpirationDays:** `365`.
* Click **Next**.

#### Screen 3: Configure stack options
* **Tags:** Add a tag:
  * **Key:** `Owner` | **Value:** `<Your Name>`
  * **Key:** `Batch` | **Value:** `TASK-Nalgonda-2026`
* Leave all other settings at default.
* Click **Next**.

#### Screen 4: Review and Submit
* Scroll to the bottom and click **Submit**.

---

### Step 3: Monitor Live Stack Creation Events

Once you click Submit, CloudFormation takes over:
1. Click the **Events** tab.
2. Watch the live timeline:
   * `AWS::CloudFormation::Stack` -> `CREATE_IN_PROGRESS` (User Initiated)
   * `AWS::S3::Bucket` (`EnterpriseS3Bucket`) -> `CREATE_IN_PROGRESS`
   * `AWS::S3::Bucket` (`EnterpriseS3Bucket`) -> `CREATE_COMPLETE`
   * `AWS::S3::BucketPolicy` (`EnforceHTTPSBucketPolicy`) -> `CREATE_IN_PROGRESS`
   * `AWS::S3::BucketPolicy` (`EnforceHTTPSBucketPolicy`) -> `CREATE_COMPLETE`
   * `AWS::CloudFormation::Stack` -> `CREATE_COMPLETE` 🎉

3. Click the **Outputs** tab:
   * View your globally unique `BucketName`.
   * View the `BucketArn`.
   * View the `BucketRegionalDomainName`.
   * View the `BucketSecureURL`.

---

### Step 4: Verify the S3 Security Configurations in AWS Console

Now let's verify that CloudFormation configured our S3 bucket exactly as promised:

1. In the AWS console search bar, search for **S3** and open the S3 service.
2. Click on your newly created bucket name in the list.
3. **Verify Encryption:**
   * Click the **Properties** tab.
   * Under *Default encryption*, verify: **Server-side encryption with Amazon S3 managed keys (SSE-S3)** is **Enabled** (AES256).
4. **Verify Object Versioning:**
   * Still on the *Properties* tab, locate *Bucket Versioning*:
   * Status must show **Bucket Versioning: Enabled**.
5. **Verify Lifecycle Rules:**
   * Click the **Management** tab.
   * Under *Lifecycle rules*, locate `TieredCostOptimizationRule`.
   * Verify the transitions:
     - Standard-IA at 30 days
     - Glacier at 90 days
     - Delete active objects at 365 days
     - Noncurrent versions expire after 90 days.
6. **Verify Public Access Block:**
   * Click the **Permissions** tab.
   * Verify all 4 checkboxes under *Block public access (bucket settings)* are marked **On**.

---

### Step 5: Test the HTTPS-Only Enforcing Bucket Policy

Our template included an S3 Bucket Policy that denies any request that does not use HTTPS (`aws:SecureTransport: false`).

#### Test with AWS CLI:
1. Upload a test text file using the standard secure CLI command:
   ```bash
   echo "Hello CloudFormation from TASK Nalgonda!" > test.txt
   aws s3 cp test.txt s3://<YOUR-BUCKET-NAME>/test.txt
   ```
   * Result: **Upload succeeds instantly!** (The AWS CLI uses HTTPS/TLS by default).

2. If any rogue client attempts to send an insecure HTTP request, AWS S3 immediately rejects it with `403 Forbidden` (`Access Denied`)!

---

### Step 6: The "Drift Detection" Experiment

In production companies, managers use **Drift Detection** to find out if someone manually changed cloud settings behind their backs!

1. Go to the S3 bucket's **Properties** tab in the console.
2. Scroll to **Tags** and click **Edit**.
3. Add a rogue tag:
   * **Key:** `ManualHack` | **Value:** `JuniorEngineerClickedThis`
4. Click **Save changes**. *(You have now created "drift" between live AWS and CloudFormation code!)*
5. Return to the **CloudFormation** console.
6. Select your stack -> Click the **Stack actions** dropdown (top right) -> Select **Detect drift**.
7. Wait 10 seconds, then click **View drift results**.
8. CloudFormation flags your stack status as: **`DRIFTED`**!
9. Click the resource name: CloudFormation shows you a visual diff highlighting the unexpected tag in red!

---

### Step 7: Performing a Safe Stack Update via Change Sets

Now suppose we want to update the lifecycle rule from 30 days to 45 days.

1. Open `s3_production_bucket.yaml` in your editor.
2. In CloudFormation console, select your stack -> Click **Update**.
3. Select **Replace current template** -> Upload your modified template.
4. On the parameters screen, change `TransitionToStandardIADays` to `45`.
5. On the review screen, scroll to the bottom and select **Create change set** instead of submitting immediately!
6. Name the change set `update-lifecycle-45-days` and click **Create change set**.
7. CloudFormation generates a preview table:
   * **Action:** `Modify`
   * **Resource:** `EnterpriseS3Bucket`
   * **Replacement:** `False` *(Guarantees your bucket will NOT be deleted or recreated!)*
8. Once verified safe, click **Execute change set** to apply the update seamlessly!

---

### Step 8: Clean Teardown (Stack Deletion)

At the end of your lab, clean up your resources to ensure **zero unexpected AWS charges**:

> ⚠️ **Important S3 Deletion Rule:**  
> Amazon S3 does not allow CloudFormation to delete a bucket that still contains files or version markers! You must empty the bucket first.

1. Open the **S3 Console**, select your bucket, and click the **Empty** button.
2. Type `permanently delete` to confirm and click **Empty**.
3. Return to the **CloudFormation** console.
4. Select your stack (`myname-s3-prod-stack`) and click the orange **Delete** button.
5. Click **Delete** to confirm.
6. CloudFormation deletes the bucket policy, deletes the bucket, and cleanly removes the stack!

---
*Created for TASK Telangana Cloud Software Developer Batch · Nalgonda Training Center*
