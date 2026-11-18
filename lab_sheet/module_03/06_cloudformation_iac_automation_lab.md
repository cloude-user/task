# Lab Sheet 3.6: Infrastructure as Code (IaC) with AWS CloudFormation
> **Module 3:** AWS Associate Core Knowledge  
> **Topic 3.d:** Declarative YAML Templates & Automated Stack Lifecycle  
> **Target:** Cloud Software Developer Trainees  

---

## 🎯 Lab Objectives
1. Validate a CloudFormation YAML template using the AWS CLI.
2. Deploy a complete enterprise S3 storage stack using CloudFormation.
3. Test **Drift Detection** to catch manual out-of-band AWS console changes.
4. Perform a safe **Stack Update** using a CloudFormation **Change Set**.
5. Perform an automated, clean stack teardown.

---

## 🛠️ Step-by-Step Instructions

### Step 1: Validate the YAML Template Syntax
In your terminal, navigate to your project directory and validate your YAML file:
```bash
aws cloudformation validate-template \
  --template-body file://projects/module_03_cloudformation_s3/s3_production_bucket.yaml \
  --region ap-south-1
```
*If valid, AWS returns the Parameters list and Description with zero errors.*

---

### Step 2: Deploy the Stack via AWS Management Console
1. Open the [AWS Management Console](https://console.aws.amazon.com/) -> Search for **CloudFormation**.
2. Click **Create stack** -> Select **With new resources (standard)**.
3. **Prerequisite:** Select `Template is ready`.
4. **Specify template:** Select `Upload a template file` -> Choose `s3_production_bucket.yaml`.
5. Click **Next**.
6. **Stack name:** `task-s3-iac-stack`.
7. **Parameters:**
   * `EnvironmentName`: `dev`
   * `BucketBaseName`: `task-nalgonda-<yourname>`
   * `EnableVersioning`: `Enabled`
8. Click **Next** -> Click **Next** -> Click **Submit**.

---

### Step 3: Monitor Stack Lifecycle Events
1. Click the **Events** tab.
2. Watch the live progression:
   * `EnterpriseS3Bucket` -> `CREATE_IN_PROGRESS` -> `CREATE_COMPLETE`
   * `EnforceHTTPSBucketPolicy` -> `CREATE_IN_PROGRESS` -> `CREATE_COMPLETE`
   * `task-s3-iac-stack` -> `CREATE_COMPLETE` 🎉
3. Click the **Outputs** tab to view your globally unique bucket name, ARN, and secure HTTPS endpoint!

---

### Step 4: Perform a Drift Detection Test
1. Go to the S3 bucket's **Properties** tab in the console.
2. Add a manual tag: `Key: ConsoleHack` | `Value: UnapprovedChange`.
3. Save changes.
4. In the CloudFormation console, select your stack -> Click **Stack actions** -> **Detect drift**.
5. Click **View drift results**: CloudFormation flags your stack status as **`DRIFTED`** and highlights the unauthorized tag in red!

---

### ⚠️ Clean Teardown
1. Empty all objects and version markers in the S3 bucket.
2. In CloudFormation, select `task-s3-iac-stack` -> Click **Delete**.
3. All provisioned resources are cleanly removed with zero orphaned costs!
