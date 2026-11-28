# Module 5.3 (M5-T3): DynamoDB (Keys, GSI, Locking, TTL, Streams) & Valkey Cache-Aside

**Goal:** Design a DynamoDB table with a partition key, sort key, and Global Secondary Index (GSI), perform Python CRUD & optimistic locking, enable TTL and Streams, and accelerate reads using an Amazon ElastiCache Serverless Valkey cache (cache-aside pattern).

> [!TIP]
> **Windows Git Bash Users:** Use the **Bash** blocks (and use `python` instead of `python3` if needed).  
> **Windows PowerShell Users:** Use the **PowerShell** blocks.

---

## Lab 1: A Table with a Sort Key and a Global Secondary Index (GSI)

**Goal:** Create `corecompute-lab-customer-orders` with partition key `customerId` + sort key `orderDate`, then add `status-index` GSI.

### 1. Create the Table
* **Bash (Git Bash / EC2 / WSL):**
  ```bash
  export AWS_DEFAULT_REGION=us-east-1
  aws dynamodb create-table --table-name corecompute-lab-customer-orders \
    --attribute-definitions AttributeName=customerId,AttributeType=S AttributeName=orderDate,AttributeType=S \
    --key-schema AttributeName=customerId,KeyType=HASH AttributeName=orderDate,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST --query TableDescription.TableStatus --output text
  aws dynamodb wait table-exists --table-name corecompute-lab-customer-orders
  ```
* **PowerShell (Windows):**
  ```powershell
  $env:AWS_DEFAULT_REGION = "us-east-1"
  aws dynamodb create-table --table-name corecompute-lab-customer-orders --attribute-definitions AttributeName=customerId,AttributeType=S AttributeName=orderDate,AttributeType=S --key-schema AttributeName=customerId,KeyType=HASH AttributeName=orderDate,KeyType=RANGE --billing-mode PAY_PER_REQUEST --query TableDescription.TableStatus --output text
  aws dynamodb wait table-exists --table-name corecompute-lab-customer-orders
  ```

### 2. Add the Global Secondary Index (`status-index`)
* **Bash (Git Bash / EC2 / WSL):**
  ```bash
  aws dynamodb update-table --table-name corecompute-lab-customer-orders \
    --attribute-definitions AttributeName=status,AttributeType=S AttributeName=orderDate,AttributeType=S \
    --global-secondary-index-updates '[{"Create":{"IndexName":"status-index","KeySchema":[{"AttributeName":"status","KeyType":"HASH"},{"AttributeName":"orderDate","KeyType":"RANGE"}],"Projection":{"ProjectionType":"ALL"}}}]' \
    --query "TableDescription.GlobalSecondaryIndexes[].IndexStatus" --output text
  ```
* **PowerShell (Windows):**
  ```powershell
  aws dynamodb update-table --table-name corecompute-lab-customer-orders --attribute-definitions AttributeName=status,AttributeType=S AttributeName=orderDate,AttributeType=S --global-secondary-index-updates '[{\"Create\":{\"IndexName\":\"status-index\",\"KeySchema\":[{\"AttributeName\":\"status\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"orderDate\",\"KeyType\":\"RANGE\"}],\"Projection\":{\"ProjectionType\":\"ALL\"}}}]' --query "TableDescription.GlobalSecondaryIndexes[].IndexStatus" --output text
  ```

### 3. Check Index Status
```bash
aws dynamodb describe-table --table-name corecompute-lab-customer-orders --query "Table.GlobalSecondaryIndexes[0].[IndexStatus,Backfilling]" --output text
```
*(Note: On an empty table, if the index stays on `CREATING`, proceed to load data in Lab 2 and check again).*

---

## Lab 2: CRUD and Queries from Python

**Goal:** Batch-load 6 orders, read, update (`UpdateExpression`), query by sort key prefix (`begins_with`), query the GSI, and delete an item.

### 1. Save this code as `crud.py`:
```python
import boto3
from boto3.dynamodb.conditions import Key

table = boto3.resource("dynamodb").Table("corecompute-lab-customer-orders")
orders = [
    ("c-101", "2026-09-28", 120, "SHIPPED"),
    ("c-101", "2026-10-01", 250, "PLACED"),
    ("c-101", "2026-10-02", 80, "PLACED"),
    ("c-102", "2026-10-01", 400, "SHIPPED"),
    ("c-102", "2026-10-03", 60, "CANCELLED"),
    ("c-103", "2026-10-02", 999, "PLACED"),
]

with table.batch_writer() as batch:   # groups puts into batches of 25
    for cust, date, total, status in orders:
        batch.put_item(Item={
            "customerId": cust,
            "orderDate": date,
            "total": total,
            "status": status
        })
print("Loaded", len(orders), "orders")

key = {"customerId": "c-101", "orderDate": "2026-10-01"}
item = table.get_item(Key=key).get("Item")
print("GET ", item["customerId"], item["orderDate"], item["status"], item["total"])

table.update_item(
    Key=key,
    UpdateExpression="SET #s = :s, #t = #t + :extra",
    ExpressionAttributeNames={"#s": "status", "#t": "total"},
    ExpressionAttributeValues={":s": "SHIPPED", ":extra": 5}
)
item = table.get_item(Key=key)["Item"]
print("UPDATE ", item["orderDate"], "->", item["status"], item["total"])

cond = Key("customerId").eq("c-101") & Key("orderDate").begins_with("2026-10")
resp = table.query(KeyConditionExpression=cond)
items = resp["Items"]
while "LastEvaluatedKey" in resp:
    resp = table.query(
        KeyConditionExpression=cond,
        ExclusiveStartKey=resp["LastEvaluatedKey"]
    )
    items += resp["Items"]
print("QUERY ", [(i["orderDate"], i["status"]) for i in items])

resp = table.query(
    IndexName="status-index",
    KeyConditionExpression=Key("status").eq("PLACED")
)
print("GSI ", [(i["customerId"], i["orderDate"]) for i in resp["Items"]])

table.delete_item(Key={"customerId": "c-103", "orderDate": "2026-10-02"})
print("DELETE c-103 2026-10-02")
```

### 2. Run it (wait until `status-index` is `ACTIVE`):
```bash
python crud.py
```

---

## Lab 3: Optimistic Locking

**Goal:** Prevent two concurrent writers from overwriting each other using a `version` attribute and `ConditionExpression`.

### 1. Save this code as `lock.py`:
```python
import boto3
from botocore.exceptions import ClientError

table = boto3.resource("dynamodb").Table("corecompute-lab-customer-orders")
key = {"customerId": "c-102", "orderDate": "2026-10-01"}

table.update_item(
    Key=key,
    UpdateExpression="SET #v = :one",
    ExpressionAttributeNames={"#v": "version"},
    ExpressionAttributeValues={":one": 1}
)
print("Start: version 1")

def save(new_total, seen_version):
    table.update_item(
        Key=key,
        UpdateExpression="SET #t = :t, #v = #v + :one",
        ConditionExpression="#v = :seen",
        ExpressionAttributeNames={"#t": "total", "#v": "version"},
        ExpressionAttributeValues={":t": new_total, ":seen": seen_version, ":one": 1}
    )

save(450, 1)
print("Writer A saved total 450 (version 1 -> 2)")

try:
    save(500, 1)   # B still thinks the version is 1
    print("Writer B saved")
except ClientError as e:
    print("Writer B rejected:", e.response["Error"]["Code"])

item = table.get_item(Key=key)["Item"]
print("Final: ", "total", item["total"], "version", item["version"])
```

### 2. Run it:
```bash
python lock.py
```

---

## Lab 4: TTL and Streams

**Goal:** Enable automatic item expiration (`expiresAt`) via TTL and publish all item modifications to a DynamoDB Stream (`NEW_AND_OLD_IMAGES`).

```bash
aws dynamodb update-time-to-live --table-name corecompute-lab-customer-orders --time-to-live-specification Enabled=true,AttributeName=expiresAt
aws dynamodb update-table --table-name corecompute-lab-customer-orders --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES --query TableDescription.StreamSpecification --output text
```

---

## Lab 5: A Valkey Cache in Front of DynamoDB (Cache-Aside)

> [!CAUTION]
> **Cost Warning:** Both the ElastiCache Serverless Cache and the EC2 instance incur hourly charges while running. Run **Lab 6: Clean Up** immediately after completing this lab!

### Step A: Create Security Groups & Serverless Valkey Cache
* **Bash (Git Bash / EC2 / WSL):**
  ```bash
  VPC=$(aws ec2 describe-vpcs --filters Name=is-default,Values=true --query "Vpcs[0].VpcId" --output text)
  CSG=$(aws ec2 create-security-group --group-name corecompute-lab-client-sg --description "Lab cache client" --vpc-id $VPC --query GroupId --output text)
  KSG=$(aws ec2 create-security-group --group-name corecompute-lab-cache-sg --description "Lab Valkey cache" --vpc-id $VPC --query GroupId --output text)

  aws ec2 authorize-security-group-ingress --group-id $KSG --protocol tcp --port 6379 --source-group $CSG
  PL=$(aws ec2 describe-managed-prefix-lists --filters Name=prefix-list-name,Values=com.amazonaws.us-east-1.ec2-instance-connect --query "PrefixLists[0].PrefixListId" --output text)
  aws ec2 authorize-security-group-ingress --group-id $CSG --ip-permissions "IpProtocol=tcp,FromPort=22,ToPort=22,PrefixListIds=[{PrefixListId=$PL}]"

  SUBS=$(aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC Name=availability-zone,Values=us-east-1a,us-east-1b,us-east-1c --query "Subnets[].SubnetId" --output text | tr '\t' ' ')
  aws elasticache create-serverless-cache --serverless-cache-name corecompute-lab-cache --engine valkey --subnet-ids $SUBS --security-group-ids $KSG --query ServerlessCache.Status --output text
  ```
* **PowerShell (Windows):**
  ```powershell
  $VPC = aws ec2 describe-vpcs --filters Name=is-default,Values=true --query "Vpcs[0].VpcId" --output text
  $CSG = aws ec2 create-security-group --group-name corecompute-lab-client-sg --description "Lab cache client" --vpc-id $VPC --query GroupId --output text
  $KSG = aws ec2 create-security-group --group-name corecompute-lab-cache-sg --description "Lab Valkey cache" --vpc-id $VPC --query GroupId --output text

  aws ec2 authorize-security-group-ingress --group-id $KSG --protocol tcp --port 6379 --source-group $CSG
  $PL = aws ec2 describe-managed-prefix-lists --filters Name=prefix-list-name,Values=com.amazonaws.us-east-1.ec2-instance-connect --query "PrefixLists[0].PrefixListId" --output text
  aws ec2 authorize-security-group-ingress --group-id $CSG --ip-permissions "IpProtocol=tcp,FromPort=22,ToPort=22,PrefixListIds=[{PrefixListId=$PL}]"

  $SUBS = (aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC" "Name=availability-zone,Values=us-east-1a,us-east-1b,us-east-1c" --query "Subnets[].SubnetId" --output text) -split "\s+"
  aws elasticache create-serverless-cache --serverless-cache-name corecompute-lab-cache --engine valkey --subnet-ids $SUBS --security-group-ids $KSG --query ServerlessCache.Status --output text
  ```

Wait until Status is `AVAILABLE` and copy the endpoint address:
```bash
aws elasticache describe-serverless-caches --serverless-cache-name corecompute-lab-cache --query "ServerlessCaches[0].[Status,Endpoint.Address]" --output text
```

### Step B: Launch EC2 Client Instance in the Same VPC
* **Bash (Git Bash / EC2 / WSL):**
  ```bash
  echo '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}' > ec2tr.json
  aws iam create-role --role-name corecompute-lab-ec2-ddb-role --assume-role-policy-document file://ec2tr.json
  aws iam attach-role-policy --role-name corecompute-lab-ec2-ddb-role --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess
  aws iam create-instance-profile --instance-profile-name corecompute-lab-ec2-ddb-role
  aws iam add-role-to-instance-profile --instance-profile-name corecompute-lab-ec2-ddb-role --role-name corecompute-lab-ec2-ddb-role
  sleep 12

  AMI=$(aws ssm get-parameter --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 --query Parameter.Value --output text)
  SUB1=$(echo $SUBS | cut -d" " -f1)
  IID=$(aws ec2 run-instances --image-id $AMI --instance-type t3.micro --subnet-id $SUB1 --security-group-ids $CSG --associate-public-ip-address --iam-instance-profile Name=corecompute-lab-ec2-ddb-role --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=corecompute-lab-cache-client}]" --query "Instances[0].InstanceId" --output text)
  echo $IID
  ```
* **PowerShell (Windows):**
  ```powershell
  '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"ec2.amazonaws.com"},"Action":"sts:AssumeRole"}]}' | Out-File -Encoding ascii ec2tr.json
  aws iam create-role --role-name corecompute-lab-ec2-ddb-role --assume-role-policy-document file://ec2tr.json
  aws iam attach-role-policy --role-name corecompute-lab-ec2-ddb-role --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess
  aws iam create-instance-profile --instance-profile-name corecompute-lab-ec2-ddb-role
  aws iam add-role-to-instance-profile --instance-profile-name corecompute-lab-ec2-ddb-role --role-name corecompute-lab-ec2-ddb-role
  Start-Sleep 12

  $AMI = aws ssm get-parameter --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 --query Parameter.Value --output text
  $IID = aws ec2 run-instances --image-id $AMI --instance-type t3.micro --subnet-id $SUBS[0] --security-group-ids $CSG --associate-public-ip-address --iam-instance-profile Name=corecompute-lab-ec2-ddb-role --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=corecompute-lab-cache-client}]" --query "Instances[0].InstanceId" --output text
  $IID
  ```

### Step C: Connect to EC2 via EC2 Instance Connect & Run Cache Scripts
In **EC2 Console → Instances → Select `corecompute-lab-cache-client` → Connect → EC2 Instance Connect**:

1. **Install packages and ping Valkey:**
   ```bash
   sudo dnf install -y python3-pip
   pip3 install boto3 valkey
   EP=<your-cache-endpoint>
   python3 -c "import valkey; print(valkey.Valkey(host='$EP', port=6379, ssl=True).ping())"
   ```

2. **Save and run `structures.py`:**
   ```python
   import sys
   import valkey

   r = valkey.Valkey(host=sys.argv[1], port=6379, ssl=True, decode_responses=True)
   r.set("page:home", "<html>home</html>", ex=60)
   print("GET page:home ", r.get("page:home"))
   print("TTL page:home ", r.ttl("page:home"), "s")
   print("INCR views:home", r.incr("views:home"))
   r.hset("session:u42", mapping={"name": "Asha", "cart": "3"})
   print("HGETALL session", r.hgetall("session:u42"))
   r.zadd("leaderboard", {"asha": 120, "ravi": 95, "meera": 140})
   print("TOP 2 players ", r.zrevrange("leaderboard", 0, 1, withscores=True))
   ```
   ```bash
   python3 structures.py $EP
   ```

3. **Save and run `cache_aside.py`:**
   ```python
   import sys, json, time, random
   import boto3, valkey

   r = valkey.Valkey(host=sys.argv[1], port=6379, ssl=True, decode_responses=True)
   table = boto3.resource("dynamodb", region_name="us-east-1").Table("corecompute-lab-customer-orders")

   def get_order(cust, date):
       k = f"order:{cust}:{date}"
       cached = r.get(k)
       if cached is not None:
           return json.loads(cached), "HIT "
       item = table.get_item(Key={"customerId": cust, "orderDate": date}).get("Item")
       if item:
           r.set(k, json.dumps(item, default=str), ex=300 + random.randint(0, 60))
       return item, "MISS"

   for i in range(3):
       start = time.perf_counter()
       item, source = get_order("c-101", "2026-10-02")
       ms = (time.perf_counter() - start) * 1000
       print(f"{source} {ms:7.1f} ms {item}")
   print("TTL left:", r.ttl("order:c-101:2026-10-02"), "s")
   ```
   ```bash
   python3 cache_aside.py $EP
   ```

---

## Lab 6: Clean Up (Run Immediately After Lab 5!)

Delete the ElastiCache cache, EC2 instance, security groups, IAM role/profile, and DynamoDB table:

* **Bash (Git Bash / EC2 / WSL):**
  ```bash
  # 1. Delete Valkey serverless cache & terminate EC2 client
  aws elasticache delete-serverless-cache --serverless-cache-name corecompute-lab-cache
  aws ec2 terminate-instances --instance-ids $IID
  aws ec2 wait instance-terminated --instance-ids $IID

  # 2. Delete DynamoDB table
  aws dynamodb delete-table --table-name corecompute-lab-customer-orders

  # 3. Clean up IAM role & instance profile
  aws iam remove-role-from-instance-profile --instance-profile-name corecompute-lab-ec2-ddb-role --role-name corecompute-lab-ec2-ddb-role
  aws iam delete-instance-profile --instance-profile-name corecompute-lab-ec2-ddb-role
  aws iam detach-role-policy --role-name corecompute-lab-ec2-ddb-role --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess
  aws iam delete-role --role-name corecompute-lab-ec2-ddb-role

  # 4. Wait for Valkey cache ENIs to release, then delete Security Groups
  aws ec2 delete-security-group --group-id $KSG
  aws ec2 delete-security-group --group-id $CSG
  ```
* **PowerShell (Windows):**
  ```powershell
  # 1. Delete Valkey serverless cache & terminate EC2 client
  aws elasticache delete-serverless-cache --serverless-cache-name corecompute-lab-cache
  aws ec2 terminate-instances --instance-ids $IID
  aws ec2 wait instance-terminated --instance-ids $IID

  # 2. Delete DynamoDB table
  aws dynamodb delete-table --table-name corecompute-lab-customer-orders

  # 3. Clean up IAM role & instance profile
  aws iam remove-role-from-instance-profile --instance-profile-name corecompute-lab-ec2-ddb-role --role-name corecompute-lab-ec2-ddb-role
  aws iam delete-instance-profile --instance-profile-name corecompute-lab-ec2-ddb-role
  aws iam detach-role-policy --role-name corecompute-lab-ec2-ddb-role --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess
  aws iam delete-role --role-name corecompute-lab-ec2-ddb-role

  # 4. Wait for Valkey cache ENIs to release, then delete Security Groups
  aws ec2 delete-security-group --group-id $KSG
  aws ec2 delete-security-group --group-id $CSG
  ```
*(Note: If `delete-security-group` says `DependencyViolation` on `$KSG`, wait ~1-2 minutes for the serverless Valkey cache to finish deleting and re-run the `delete-security-group` commands).*
