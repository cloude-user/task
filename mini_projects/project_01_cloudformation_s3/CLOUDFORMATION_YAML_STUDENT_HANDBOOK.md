# AWS CloudFormation & YAML Mastery Handbook
> **Program:** TASK Telangana · Cloud Software Developer  
> **Trainer:** Sundeep Hiremat | Nalgonda Center  
> **Course Track:** Module 3 — Infrastructure as Code (IaC) & AWS Automation  
> **Target Audience:** Cloud Software Developer Trainees & Engineering Students  

---

## 📑 Table of Contents
1. [Why Infrastructure as Code (IaC)? — The Problem with "ClickOps"](#1-why-infrastructure-as-code-iac--the-problem-with-clickops)
2. [What is AWS CloudFormation? — The Blueprint Engine](#2-what-is-aws-cloudformation--the-blueprint-engine)
3. [YAML Demystified — The Human-Friendly Data Language](#3-yaml-demystified--the-human-friendly-data-language)
   - [The Golden Rules of YAML](#the-golden-rules-of-yaml)
   - [YAML Data Structures: Scalars, Lists, and Mappings](#yaml-data-structures-scalars-lists-and-mappings)
   - [Multiline Strings: Literal `|` vs Folded `>`](#multiline-strings-literal--vs-folded-)
   - [YAML vs JSON Side-by-Side Comparison](#yaml-vs-json-side-by-side-comparison)
4. [Anatomy of an AWS CloudFormation Template](#4-anatomy-of-an-aws-cloudformation-template)
   - [The 9 Standard Sections](#the-9-standard-sections)
   - [Deep Dive into Parameters, Resources, and Outputs](#deep-dive-into-parameters-resources-and-outputs)
5. [CloudFormation Intrinsic Functions & Pseudo Parameters](#5-cloudformation-intrinsic-functions--pseudo-parameters)
   - [Intrinsic Functions: `!Ref`, `!GetAtt`, `!Sub`, `!Join`, `!FindInMap`](#intrinsic-functions-ref-getatt-sub-join-findinmap)
   - [Pseudo Parameters: Account ID, Region, Stack Name](#pseudo-parameters-account-id-region-stack-name)
6. [How to Access and Deploy CloudFormation](#6-how-to-access-and-deploy-cloudformation)
   - [Workflow 1: AWS Management Console (Drag & Drop / Upload)](#workflow-1-aws-management-console-drag--drop--upload)
   - [Workflow 2: CloudFormation Designer (Visual Architecture)](#workflow-2-cloudformation-designer-visual-architecture)
   - [Workflow 3: AWS CLI (`validate-template`, `deploy`, `create-stack`)](#workflow-3-aws-cli-validate-template-deploy-create-stack)
7. [Advanced CloudFormation Capabilities](#7-advanced-cloudformation-capabilities)
   - [Change Sets (Safety Preview)](#change-sets-safety-preview)
   - [Drift Detection (Catching Out-of-Band Console Tampering)](#drift-detection-catching-out-of-band-console-tampering)
   - [Rollback Behavior & Stack Protection](#rollback-behavior--stack-protection)
8. [Top 10 Common YAML & CloudFormation Traps (and How to Fix Them)](#8-top-10-common-yaml--cloudformation-traps-and-how-to-fix-them)

---

## 1. Why Infrastructure as Code (IaC)? — The Problem with "ClickOps"

In Days 1 through 5, we created AWS resources manually by logging into the **AWS Management Console** and clicking buttons:
- We clicked to launch an EC2 instance.
- We clicked to create security groups and add inbound rules.
- We clicked to create VPCs, subnets, and route tables.

While clicking through the console is great for beginners to understand AWS services visually, in enterprise IT production, manual clicking (known as **"ClickOps"**) has fatal flaws:
1. **Human Error:** If you launch 10 EC2 instances manually, you will misconfigure a security group rule or forget an encryption checkbox on at least two of them.
2. **Zero Audit Trail:** Who opened port 22 to `0.0.0.0/0` at 2:00 AM? You cannot tell from the console without digging through deep CloudTrail JSON logs.
3. **Disaster Recovery is Impossible:** If a typhoon knocks down an entire AWS Region (e.g., `ap-south-1` Mumbai), recreating your 50 VPCs, 200 servers, and 15 databases by clicking through the console would take weeks!
4. **Environment Drift:** Your development environment never matches production because someone manually tweaked a setting in prod and forgot to document it.

### The Solution: Infrastructure as Code (IaC)
> **Infrastructure as Code (IaC)** means defining your entire IT infrastructure (servers, databases, networks, storage, firewall rules) as human-readable, version-controlled **text files** (code).

With IaC:
* Your infrastructure is stored in **Git / GitHub**.
* You review infrastructure changes with Pull Requests (PRs).
* You can recreate an entire bank's cloud infrastructure in 10 minutes with a single command!

---

## 2. What is AWS CloudFormation? — The Blueprint Engine

**AWS CloudFormation** is Amazon's native declarative Infrastructure as Code service. 

```
+-----------------------------------------------------------+
|          CLOUDFORMATION TEMPLATE (YAML / JSON)            |
| "I want 1 VPC, 2 Subnets, and 1 Enterprise S3 Bucket"     |
+-----------------------------------------------------------+
                             |
                             v  (aws cloudformation deploy)
+-----------------------------------------------------------+
|              AWS CLOUDFORMATION ENGINE                    |
|  - Parses YAML syntax                                     |
|  - Calculates dependency graph (VPC first, then Subnet)   |
|  - Calls AWS APIs in exact mathematical sequence          |
|  - Handles rollback if any resource fails                 |
+-----------------------------------------------------------+
                             |
                             v
+-----------------------------------------------------------+
|                   LIVE AWS RESOURCES                      |
|      [ S3 Bucket ]     [ VPC Network ]     [ EC2 Server ]  |
+-----------------------------------------------------------+
```

### Core Terminology You Must Know:
* **Template:** A formatted text file (YAML or JSON) that acts as the architectural blueprint describing your desired AWS resources.
* **Stack:** The live, instantiated collection of resources created and managed as a single unit by CloudFormation. When you delete the stack, all resources inside it are cleanly destroyed in reverse order!
* **Change Set:** A preview generated by CloudFormation showing exactly what resources will be added, modified, or destroyed *before* you execute the update.

---

## 3. YAML Demystified — The Human-Friendly Data Language

CloudFormation templates can be written in either **JSON** or **YAML**. In 95% of real-world companies, developers write CloudFormation in **YAML**.

### Why YAML over JSON?
* **YAML** stands for *"YAML Ain't Markup Language"*.
* It does not use messy `{}` curly braces or `[]` square brackets.
* It supports **inline comments** (`#`), which JSON does not!
* It allows concise shorthand syntax for CloudFormation intrinsic functions (e.g., `!Ref` instead of `{"Ref": "..."}`).

---

### The Golden Rules of YAML

1. **Rule 1: Indentation is Everything (Spaces Only, NEVER Tabs!):**
   * YAML uses spaces to denote hierarchy (structure).
   * Standard convention is **2 spaces per indentation level**.
   * **TAB characters (`\t`) are strictly forbidden in YAML!** Pressing the Tab key in your editor will cause syntax errors. In VS Code, configure your editor to convert tabs to 2 spaces.

2. **Rule 2: Case Sensitivity:**
   * Keys, properties, and values are case-sensitive. `BucketName` is NOT the same as `bucketname`.

3. **Rule 3: Colons must be followed by a Space:**
   * Key-value pairs are written as `Key: Value`.
   * `Name:Production` (WRONG — no space after colon!)
   * `Name: Production` (CORRECT — single space after colon!)

---

### YAML Data Structures: Scalars, Lists, and Mappings

#### 1. Key-Value Mappings (Dictionaries / Hash Maps)
```yaml
# Simple key-value pairs
ProjectName: CloudPortfolio
Environment: Production
MaxInstances: 5
IsEncrypted: true
```

#### 2. Lists (Arrays / Sequences)
Lists in YAML start with a dash `-` followed by a space:
```yaml
# List of strings
AvailabilityZones:
  - ap-south-1a
  - ap-south-1b
  - ap-south-1c

# List of objects
SecurityGroupRules:
  - Protocol: tcp
    Port: 80
    Cidr: 0.0.0.0/0
  - Protocol: tcp
    Port: 443
    Cidr: 0.0.0.0/0
```

#### 3. Nested Mappings (Object within Object)
```yaml
DatabaseConfig:
  Engine: postgres
  Version: 15.3
  Storage:
    AllocatedGb: 20
    StorageType: gp3
```

---

### Multiline Strings: Literal `|` vs Folded `>`

When writing bash scripts or complex JSON policies inside YAML (such as EC2 UserData or S3 Bucket Policies), YAML gives you two special operators:

* **Pipe `|` (Literal Style):** Preserves all newlines exactly as typed.
  ```yaml
  UserData: |
    #!/bin/bash
    apt-get update -y
    apt-get install -y nginx
    systemctl start nginx
  ```
* **Greater-Than `>` (Folded Style):** Replaces newlines with single spaces, collapsing a long paragraph into one line.
  ```yaml
  Description: >
    This CloudFormation template provisions a hardened
    enterprise S3 bucket with AES256 server-side encryption
    and automated lifecycle management.
  ```

---

### YAML vs JSON Side-by-Side Comparison

Look how much cleaner and more readable YAML is compared to JSON for defining the exact same S3 bucket:

| JSON (Verbose & Cluttered) | YAML (Clean & Readable) |
|---|---|
| ```json<br>{<br>  "Resources": {<br>    "MyBucket": {<br>      "Type": "AWS::S3::Bucket",<br>      "Properties": {<br>        "BucketName": "task-nalgonda-s3",<br>        "VersioningConfiguration": {<br>          "Status": "Enabled"<br>        }<br>      }<br>    }<br>  }<br>}<br>``` | ```yaml<br>Resources:<br>  MyBucket:<br>    Type: AWS::S3::Bucket<br>    Properties:<br>      BucketName: task-nalgonda-s3<br>      VersioningConfiguration:<br>        Status: Enabled<br>``` |

---

## 4. Anatomy of an AWS CloudFormation Template

An AWS CloudFormation template contains up to **9 top-level sections**. 
Only one section is mandatory: **`Resources`**. All others are optional but essential for production templates!

```yaml
AWSTemplateFormatVersion: '2010-09-09'  # 1. Format Version (Always 2010-09-09)
Description: 'Template description'     # 2. Human-readable summary

Metadata:                               # 3. UI grouping and layout details
  ...

Parameters:                             # 4. Inputs passed in at deployment time
  ...

Mappings:                              # 5. Static lookup tables (e.g. Region -> AMI)
  ...

Conditions:                            # 6. If/Else logic for resource creation
  ...

Transform:                             # 7. Macros (e.g. AWS::Serverless-2016-10-31)
  ...

Resources:                             # 8. MANDATORY: The AWS resources to build
  ...

Outputs:                               # 9. Return values (ARNs, URLs, exports)
  ...
```

---

### Deep Dive into the 3 Core Sections

#### Section A: `Parameters` (Custom Inputs)
Parameters make your template reusable across development, testing, and production without editing the code!

```yaml
Parameters:
  EnvironmentName:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - prod
    Description: Enter the deployment environment (dev, staging, or prod).

  TransitionDays:
    Type: Number
    Default: 30
    MinValue: 1
    MaxValue: 365
    Description: Number of days before moving cold objects to Standard-IA storage.
```

#### Section B: `Resources` (The Mandatory Core)
This is where you declare what AWS components CloudFormation should construct. Every resource has:
1. **Logical ID:** A unique name within the template (e.g., `MyEnterpriseBucket`).
2. **Type:** The official AWS resource identifier (e.g., `AWS::S3::Bucket`, `AWS::EC2::Instance`, `AWS::EC2::VPC`).
3. **Properties:** Service-specific configuration settings.

```yaml
Resources:
  MyEnterpriseBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'mycompany-${EnvironmentName}-assets'
      VersioningConfiguration:
        Status: Enabled
```

#### Section C: `Outputs` (Exported Results)
Outputs display important values on the CloudFormation console (e.g., website URLs, IP addresses) and allow other CloudFormation stacks to import them using `!ImportValue`.

```yaml
Outputs:
  BucketArn:
    Description: The Amazon Resource Name of the created S3 bucket.
    Value: !GetAtt MyEnterpriseBucket.Arn
    Export:
      Name: !Sub '${AWS::StackName}-BucketArn'
```

---

## 5. CloudFormation Intrinsic Functions & Pseudo Parameters

To make templates dynamic, CloudFormation provides built-in helper functions. In YAML, you can use convenient exclamation-mark (`!`) short forms.

### Essential Intrinsic Functions

| Short Form | Function Name | Purpose & Example |
|---|---|---|
| `!Ref` | `Ref` | Returns the value of a Parameter OR the physical ID of a Resource.<br>`VpcId: !Ref MyVpc` |
| `!GetAtt` | `Fn::GetAtt` | Retrieves an attribute from a resource (such as ARN, DNS name, or Private IP).<br>`Value: !GetAtt MyBucket.Arn` |
| `!Sub` | `Fn::Sub` | Substitutes variables inside a string (String interpolation).<br>`BucketName: !Sub '${AWS::StackName}-${EnvironmentName}-data'` |
| `!Join` | `Fn::Join` | Concatenates a list of strings with a delimiter.<br>`!Join [ '-', [ 'task', 'nalgonda', 's3' ] ]` |
| `!FindInMap` | `Fn::FindInMap` | Looks up a value in the `Mappings` table.<br>`ImageId: !FindInMap [ RegionMap, !Ref 'AWS::Region', AMI ]` |
| `!If` | `Fn::If` | Returns one value if a Condition is true, and another if false.<br>`BucketEncryption: !If [ IsProd, 'aws:kms', 'AES256' ]` |

---

### Pseudo Parameters (Predefined AWS Variables)

AWS automatically provides pseudo parameters that you can reference anytime without defining them in the `Parameters` section:

* `AWS::AccountId`: The 12-digit AWS account ID where the stack is running.
* `AWS::Region`: The current region (e.g., `ap-south-1`, `us-east-1`).
* `AWS::StackName`: The name given to the stack when deployed.
* `AWS::StackId`: The complete unique ARN of the CloudFormation stack.
* `AWS::NoValue`: Acts as a `null`/remove operator; if assigned to a property, CloudFormation ignores that property completely.

---

## 6. How to Access and Deploy CloudFormation

There are three primary ways to interact with AWS CloudFormation:

### Workflow 1: AWS Management Console (Drag & Drop / Upload)
1. Log in to the **AWS Management Console** and search for **CloudFormation**.
2. Click the orange **Create stack** button -> choose **With new resources (standard)**.
3. Under *Prerequisite - Prepare template*, select **Template is ready**.
4. Under *Specify template*, select **Upload a template file** and choose your `.yaml` file.
5. Click **Next** -> Specify Stack Name (e.g., `sundeep-s3-prod-stack`) -> Enter Parameter values.
6. Click **Next** -> Configure stack options (leave defaults or add tags) -> Click **Next**.
7. Review your configuration, check the IAM acknowledgment box (if prompted), and click **Submit**.
8. Watch the **Events** tab refresh in real time as each resource changes status from `CREATE_IN_PROGRESS` to `CREATE_COMPLETE`!

---

### Workflow 2: CloudFormation Designer (Visual Architecture)
* Click **Create stack** -> Select **Create template in CloudFormation Designer**.
* CloudFormation opens a visual diagramming canvas where you can drag AWS services from the left palette and drop them onto the canvas.
* As you drag resources or connect lines between them (e.g., attaching an Internet Gateway to a VPC), CloudFormation automatically writes the corresponding YAML code in the integrated code editor below!

---

### Workflow 3: AWS CLI (Automated Terminal Deployment)

In enterprise CI/CD pipelines (Jenkins, GitHub Actions, GitLab CI), CloudFormation is deployed via terminal commands.

#### 1. Validate YAML Syntax:
```bash
aws cloudformation validate-template \
  --template-body file://s3_production_bucket.yaml \
  --region ap-south-1
```
*If valid, AWS returns the Parameters list and Description. If invalid, it gives you the exact line number of your YAML error!*

#### 2. Deploy the Stack:
```bash
aws cloudformation deploy \
  --template-file s3_production_bucket.yaml \
  --stack-name sundeep-s3-production-stack \
  --parameter-overrides EnvironmentName=dev BucketBaseName=task-nalgonda \
  --region ap-south-1
```

#### 3. Describe Stack Outputs:
```bash
aws cloudformation describe-stacks \
  --stack-name sundeep-s3-production-stack \
  --query "Stacks[0].Outputs" \
  --output table \
  --region ap-south-1
```

#### 4. Delete the Stack (Clean Teardown):
```bash
aws cloudformation delete-stack \
  --stack-name sundeep-s3-production-stack \
  --region ap-south-1
```

---

## 7. Advanced CloudFormation Capabilities

### 1. Change Sets (Safety Preview)
Before modifying an active production stack, you can create a **Change Set**.
* CloudFormation analyzes your updated YAML template against the currently deployed stack.
* It outputs an itemized summary showing which resources will be:
  - `Add` (New resource created)
  - `Modify` (Existing resource updated without interruption)
  - `Replacement` (**DANGER!** Resource will be destroyed and recreated, causing downtime or data loss if not carefully planned!)

### 2. Drift Detection (Catching Out-of-Band Console Tampering)
Suppose you deployed an S3 bucket with versioning enabled via CloudFormation. A junior engineer logs into the AWS console and clicks "Suspend Versioning".
* Your live AWS infrastructure is now in a state of **Drift** (it no longer matches the code in Git!).
* In CloudFormation, click **Stack actions** -> **Detect drift**.
* CloudFormation scans your live AWS resources, compares them with the template, and flags the drifted property in red!

### 3. Automatic Rollback on Failure
If a stack creation fails on resource #5 out of 10, CloudFormation triggers an **automatic rollback**:
* It cleanly deletes resources #1 through #4 in reverse order.
* It ensures you never leave orphaned, half-configured, or unbilled resources in your AWS account!

---

## 8. Top 10 Common YAML & CloudFormation Traps (and How to Fix Them)

| # | Trap / Error Message | Root Cause | How to Fix It |
|---|---|---|---|
| 1 | `Tab character detected in YAML` | Pressed the `Tab` key instead of spaces. | Configure VS Code: `"editor.insertSpaces": true`, `"editor.tabSize": 2`. |
| 2 | `Bucket name already exists` | S3 bucket names must be globally unique across all AWS accounts worldwide. | Use `!Sub '${BucketBaseName}-${AWS::AccountId}-${AWS::Region}'` to guarantee global uniqueness. |
| 3 | `Unrecognized resource type` | Typo in the AWS resource type string. | Check spelling: It is `AWS::S3::Bucket`, not `AWS::S3::bucket` or `AWS::S3::BucketResource`. |
| 4 | `Template format error: At least one Resources member must be defined` | Missed the `Resources:` header or indented it incorrectly. | Ensure `Resources:` starts at column 0 (no leading spaces). |
| 5 | `Circular dependency between resources` | Resource A references Resource B, while Resource B references Resource A. | Break the cycle by passing one reference via parameter or separate policy resource. |
| 6 | `Bucket cannot be deleted because it is not empty` | Attempting to delete a stack with an S3 bucket that contains files. | Empty all objects and version markers in the S3 bucket before deleting the stack. |
| 7 | `Fn::Sub requires a string` | Passed an object or list into `!Sub` where a string was expected. | Ensure string interpolation wraps inside quotes: `!Sub 'name-${Param}'`. |
| 8 | `Value of property Status must be an element of the list` | Typo in enum values (e.g., `status: true` instead of `Status: Enabled`). | Refer to AWS CloudFormation S3 documentation for valid enum strings. |
| 9 | `Missing required property` | Forgot a mandatory property for that AWS resource type. | Review the required properties list in the official AWS CloudFormation user guide. |
| 10 | `YAML Mapping values are not allowed here` | Forgot the space after a colon (`Key:Value` instead of `Key: Value`). | Add a space immediately after the colon. |

---
*Created for TASK Telangana Cloud Software Developer Batch · Nalgonda Training Center*
