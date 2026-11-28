# Module 5.1 (M5-T1): AWS CLI, Credentials, Python `boto3` & Lambda X-Ray

**Goal:** Master the AWS CLI, understand where credentials come from, write resilient Python code with `boto3`, and trace cold vs. warm Lambda invocations with AWS X-Ray.

> [!TIP]
> **Windows PowerShell vs. Linux/EC2 Bash:** Every step below provides **both** Windows PowerShell and Bash commands so you can follow along regardless of whether you are on your laptop or an EC2 instance.

---

## Lab 1: The AWS CLI & S3 Bucket

**Goal:** Verify your AWS identity, list regions using `--query` (JMESPath), create an S3 bucket, and upload a file.

### 1. Check Identity & Regions
* **PowerShell (Windows):**
  ```powershell
  $env:AWS_DEFAULT_REGION = "us-east-1"
  aws sts get-caller-identity
  aws ec2 describe-regions --query "Regions[].RegionName" --output text
  ```
* **Bash (EC2 / WSL):**
  ```bash
  export AWS_DEFAULT_REGION=us-east-1
  aws sts get-caller-identity
  aws ec2 describe-regions --query "Regions[].RegionName" --output text
  ```

### 2. Create a Unique S3 Bucket & Upload a File
* **PowerShell (Windows):**
  ```powershell
  $AC = aws sts get-caller-identity --query Account --output text
  $BUCKET = "corecompute-lab-m5-$AC-" + (Get-Random -Maximum 99999)
  aws s3 mb "s3://$BUCKET"
  "hello module 5" | Out-File -Encoding ascii hello.txt
  aws s3 cp hello.txt "s3://$BUCKET/"
  aws s3 ls "s3://$BUCKET/"
  ```
* **Bash (EC2 / WSL):**
  ```bash
  AC=$(aws sts get-caller-identity --query Account --output text)
  BUCKET=corecompute-lab-m5-$AC-$RANDOM
  aws s3 mb s3://$BUCKET
  echo "hello module 5" > hello.txt
  aws s3 cp hello.txt s3://$BUCKET/
  aws s3 ls s3://$BUCKET/
  ```

*(Open **AWS Console → S3 → General purpose buckets** to confirm `hello.txt` is there).*

---

## Lab 2: Where Do My Credentials Come From?

**Goal:** Inspect the AWS Credential Provider Chain in your environment.

* **PowerShell (Windows):**
  ```powershell
  aws configure list
  Get-ChildItem Env: | Where-Object Name -like "AWS_*" | ForEach-Object { $_.Name + "=..." }
  ```
* **Bash (EC2 / WSL):**
  ```bash
  aws configure list
  env | grep ^AWS_ | sed 's/=.*/=.../'
  ```

> **Key Takeaway:** On your laptop, `aws configure list` shows `shared-credentials-file`. On EC2, it shows `iam-role`. In Lambda, it uses the execution role. **Your Python code never changes!**

---

## Lab 3: Calling AWS from Python with `boto3`

**Goal:** Write a script using retries, a paginator (`list_objects_v2`), and `ClientError` handling.

### 1. Save this code as `sdk1_demo.py`:
```python
import sys
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

bucket = sys.argv[1]
cfg = Config(retries={"max_attempts": 5, "mode": "standard"})
s3 = boto3.client("s3", config=cfg)

print("Running as:", boto3.client("sts").get_caller_identity()["Arn"])

for i in range(25):
    s3.put_object(Bucket=bucket, Key=f"logs/file-{i:02}.txt", Body=f"line {i}")
print("Uploaded 25 objects")

pages = s3.get_paginator("list_objects_v2").paginate(
    Bucket=bucket, Prefix="logs/", PaginationConfig={"PageSize": 10}
)
for n, page in enumerate(pages, start=1):
    print(f"Page {n}: {len(page.get('Contents', []))} objects")

try:
    s3.head_object(Bucket=bucket, Key="missing.txt")
except ClientError as e:
    print("Handled error, code:", e.response["Error"]["Code"])
```

### 2. Run the script:
* **PowerShell (Windows):**
  ```powershell
  python sdk1_demo.py $BUCKET
  ```
* **Bash (EC2 / WSL):**
  ```bash
  python3 sdk1_demo.py $BUCKET
  ```

---

## Lab 4: Tracing a Lambda Function with X-Ray

**Goal:** Deploy a Lambda function with X-Ray Active tracing and compare **Cold Start** vs. **Warm** call latencies.

### 1. Save this code as `lambda_function.py`:
```python
import time
import boto3

sts = boto3.client("sts")  # init code: runs once per environment

def lambda_handler(event, context):
    time.sleep(0.3)  # pretend to do some work
    arn = sts.get_caller_identity()["Arn"]
    return {"statusCode": 200, "body": arn}
```

### 2. Package, Create Role, and Deploy Lambda
* **PowerShell (Windows):**
  ```powershell
  # Create trust policy
  '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' | Out-File -Encoding ascii tr.json

  # Zip the function
  Compress-Archive -Path lambda_function.py -DestinationPath x.zip -Force

  # Create IAM Role and attach policies
  $RA = aws iam create-role --role-name corecompute-lab-xray-role --assume-role-policy-document file://tr.json --query Role.Arn --output text
  aws iam attach-role-policy --role-name corecompute-lab-xray-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
  aws iam attach-role-policy --role-name corecompute-lab-xray-role --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess

  # Wait 12 seconds for IAM propagation
  Start-Sleep -Seconds 12

  # Create Lambda function
  aws lambda create-function --function-name corecompute-lab-xray --runtime python3.13 --handler lambda_function.lambda_handler --role $RA --zip-file fileb://x.zip --tracing-config Mode=Active --query "[FunctionName,Runtime,TracingConfig.Mode]" --output text
  ```
* **Bash (EC2 / WSL):**
  ```bash
  echo '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' > tr.json
  python3 -c "import zipfile; z=zipfile.ZipFile('x.zip','w'); z.write('lambda_function.py'); z.close()"
  RA=$(aws iam create-role --role-name corecompute-lab-xray-role --assume-role-policy-document file://tr.json --query Role.Arn --output text)
  aws iam attach-role-policy --role-name corecompute-lab-xray-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
  aws iam attach-role-policy --role-name corecompute-lab-xray-role --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess
  sleep 12
  aws lambda create-function --function-name corecompute-lab-xray --runtime python3.13 --handler lambda_function.lambda_handler --role $RA --zip-file fileb://x.zip --tracing-config Mode=Active --query "[FunctionName,Runtime,TracingConfig.Mode]" --output text
  ```

### 3. Invoke 5 Times (1 Cold + 4 Warm)
* **PowerShell (Windows):**
  ```powershell
  1..5 | ForEach-Object { aws lambda invoke --function-name corecompute-lab-xray out.json --query StatusCode --output text }
  Get-Content out.json
  ```
* **Bash (EC2 / WSL):**
  ```bash
  for i in 1 2 3 4 5; do aws lambda invoke --function-name corecompute-lab-xray out.json --query StatusCode --output text; done
  cat out.json
  ```

*(Open **AWS Console → CloudWatch → Application Signals (APM) → Traces** to inspect the Init segment on the cold start vs. the fast warm calls).*

---

## Lab 5: Clean Up

Always delete resources when finished to avoid charges:

* **PowerShell (Windows):**
  ```powershell
  aws s3 rb "s3://$BUCKET" --force
  aws lambda delete-function --function-name corecompute-lab-xray
  aws logs delete-log-group --log-group-name /aws/lambda/corecompute-lab-xray
  aws iam detach-role-policy --role-name corecompute-lab-xray-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
  aws iam detach-role-policy --role-name corecompute-lab-xray-role --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess
  aws iam delete-role --role-name corecompute-lab-xray-role
  ```
* **Bash (EC2 / WSL):**
  ```bash
  aws s3 rb s3://$BUCKET --force
  aws lambda delete-function --function-name corecompute-lab-xray
  aws logs delete-log-group --log-group-name /aws/lambda/corecompute-lab-xray
  aws iam detach-role-policy --role-name corecompute-lab-xray-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
  aws iam detach-role-policy --role-name corecompute-lab-xray-role --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess
  aws iam delete-role --role-name corecompute-lab-xray-role
  ```
