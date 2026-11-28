# Module 5.2 (M5-T2): SQS, Dead-Letter Queues, FIFO, SNS Fan-out & DynamoDB Pipeline

**Goal:** Master asynchronous cloud messaging patterns using Amazon SQS (Standard, DLQ, FIFO), Amazon SNS (Fan-out & Filter Policies), and build an idempotent Python consumer pipeline writing into Amazon DynamoDB.

---

## Lab 1: SQS Basics and the Visibility Timeout

**Goal:** Send a message, receive it without deleting it, and observe it reappear after the 30-second visibility timeout with an incremented `ApproximateReceiveCount`.

### 1. Create the Standard Queue
* **PowerShell (Windows):**
  ```powershell
  $env:AWS_DEFAULT_REGION = "us-east-1"
  $Q = aws sqs create-queue --queue-name corecompute-lab-orders --query QueueUrl --output text
  $Q
  ```
* **Bash (EC2 / WSL):**
  ```bash
  export AWS_DEFAULT_REGION=us-east-1
  Q=$(aws sqs create-queue --queue-name corecompute-lab-orders --query QueueUrl --output text)
  echo $Q
  ```

### 2. Send One Order & Receive (Do NOT delete)
* **PowerShell (Windows):**
  ```powershell
  aws sqs send-message --queue-url $Q --message-body '{\"orderId\": 101, \"item\": \"laptop\", \"qty\": 1}'
  aws sqs receive-message --queue-url $Q --attribute-names ApproximateReceiveCount --query "Messages[0].[Body,Attributes.ApproximateReceiveCount]" --output text
  ```
* **Bash (EC2 / WSL):**
  ```bash
  aws sqs send-message --queue-url $Q --message-body '{"orderId": 101, "item": "laptop", "qty": 1}'
  aws sqs receive-message --queue-url $Q --attribute-names ApproximateReceiveCount --query "Messages[0].[Body,Attributes.ApproximateReceiveCount]" --output text
  ```

### 3. Wait 35 Seconds and Receive Again
* **PowerShell (Windows):**
  ```powershell
  Start-Sleep 35
  aws sqs receive-message --queue-url $Q --attribute-names ApproximateReceiveCount --query "Messages[0].[Body,Attributes.ApproximateReceiveCount]" --output text
  ```
* **Bash (EC2 / WSL):**
  ```bash
  sleep 35
  aws sqs receive-message --queue-url $Q --attribute-names ApproximateReceiveCount --query "Messages[0].[Body,Attributes.ApproximateReceiveCount]" --output text
  ```

---

## Lab 2: A Dead-Letter Queue (DLQ)

**Goal:** Automatically move a failing "poison pill" message out of the main queue into a DLQ after `maxReceiveCount = 3`.

### 1. Create DLQ & Attach RedrivePolicy
* **PowerShell (Windows):**
  ```powershell
  $DLQ = aws sqs create-queue --queue-name corecompute-lab-orders-dlq --attributes MessageRetentionPeriod=1209600 --query QueueUrl --output text
  $DA = aws sqs get-queue-attributes --queue-url $DLQ --attribute-names QueueArn --query Attributes.QueueArn --output text
  $rp = @{deadLetterTargetArn=$DA; maxReceiveCount="3"} | ConvertTo-Json -Compress
  @{RedrivePolicy=$rp} | ConvertTo-Json -Compress | Out-File -Encoding ascii redrive.json
  aws sqs set-queue-attributes --queue-url $Q --attributes file://redrive.json
  ```
* **Bash (EC2 / WSL):**
  ```bash
  DLQ=$(aws sqs create-queue --queue-name corecompute-lab-orders-dlq --attributes MessageRetentionPeriod=1209600 --query QueueUrl --output text)
  DA=$(aws sqs get-queue-attributes --queue-url $DLQ --attribute-names QueueArn --query Attributes.QueueArn --output text)
  echo "{\"RedrivePolicy\":\"{\\\"deadLetterTargetArn\\\":\\\"$DA\\\",\\\"maxReceiveCount\\\":\\\"3\\\"}\"}" > redrive.json
  aws sqs set-queue-attributes --queue-url $Q --attributes file://redrive.json
  ```

### 2. Purge Main Queue, Send Bad Message, & Poll 4 Times
* **PowerShell (Windows):**
  ```powershell
  aws sqs purge-queue --queue-url $Q
  Start-Sleep 60
  aws sqs send-message --queue-url $Q --message-body '{\"orderId\": 102, \"item\": \"bad\"}'
  1..4 | ForEach-Object {
    "poll-$_"
    aws sqs receive-message --queue-url $Q --visibility-timeout 0 --attribute-names ApproximateReceiveCount --query "Messages[0].Attributes.ApproximateReceiveCount" --output text
  }
  Start-Sleep 5
  aws sqs get-queue-attributes --queue-url $DLQ --attribute-names ApproximateNumberOfMessages --query Attributes.ApproximateNumberOfMessages --output text
  ```
* **Bash (EC2 / WSL):**
  ```bash
  aws sqs purge-queue --queue-url $Q
  sleep 60
  aws sqs send-message --queue-url $Q --message-body '{"orderId": 102, "item": "bad"}'
  for i in 1 2 3 4; do
    echo "poll-$i"
    aws sqs receive-message --queue-url $Q --visibility-timeout 0 --attribute-names ApproximateReceiveCount --query "Messages[0].Attributes.ApproximateReceiveCount" --output text
  done
  sleep 5
  aws sqs get-queue-attributes --queue-url $DLQ --attribute-names ApproximateNumberOfMessages --query Attributes.ApproximateNumberOfMessages --output text
  ```
*(Result: Poll 4 returns `None` on the main queue, and the DLQ now holds `1` message).*

---

## Lab 3: FIFO Order and Deduplication

**Goal:** Prove that a `.fifo` queue drops duplicate messages within 5 minutes and preserves strict ordering per `MessageGroupId`.

### 1. Create FIFO Queue & Send Messages
* **PowerShell (Windows):**
  ```powershell
  $F = aws sqs create-queue --queue-name corecompute-lab-payments.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true --query QueueUrl --output text
  1..2 | ForEach-Object { aws sqs send-message --queue-url $F --message-group-id customer-A --message-body '{\"pay\": 500}' --query MessageId --output text }
  1..3 | ForEach-Object { aws sqs send-message --queue-url $F --message-group-id customer-B --message-body "step-$_" --query MessageId --output text }
  ```
* **Bash (EC2 / WSL):**
  ```bash
  F=$(aws sqs create-queue --queue-name corecompute-lab-payments.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true --query QueueUrl --output text)
  for i in 1 2; do aws sqs send-message --queue-url $F --message-group-id customer-A --message-body '{"pay": 500}' --query MessageId --output text; done
  for i in 1 2 3; do aws sqs send-message --queue-url $F --message-group-id customer-B --message-body "step-$i" --query MessageId --output text; done
  ```

### 2. Receive & Verify Order + Deduplication
* **PowerShell / Bash:**
  ```bash
  aws sqs receive-message --queue-url $F --max-number-of-messages 10 --visibility-timeout 0 --attribute-names MessageGroupId --query "Messages[].[Attributes.MessageGroupId,Body]" --output text
  ```

---

## Lab 4: SNS Fan-out with a Filter Policy

**Goal:** Publish 1 event to SNS and fan it out to two SQS queues, filtering the analytics queue to receive **only** `order_cancelled` events.

### 1. Create SNS Topic, Two SQS Queues, Policies & Subscriptions
* **PowerShell (Windows):**
  ```powershell
  $T = aws sns create-topic --name corecompute-lab-order-events --query TopicArn --output text
  foreach ($n in "inventory","analytics") {
    $U = aws sqs create-queue --queue-name "corecompute-lab-$n-queue" --query QueueUrl --output text
    $A = aws sqs get-queue-attributes --queue-url $U --attribute-names QueueArn --query Attributes.QueueArn --output text
    $st = @{Effect="Allow"; Principal=@{Service="sns.amazonaws.com"}; Action="sqs:SendMessage"; Resource=$A; Condition=@{ArnEquals=@{"aws:SourceArn"=$T}}}
    $pol = @{Version="2012-10-17"; Statement=@($st)} | ConvertTo-Json -Depth 6 -Compress
    @{Policy=$pol} | ConvertTo-Json -Compress | Out-File -Encoding ascii pol.json
    aws sqs set-queue-attributes --queue-url $U --attributes file://pol.json
    $S = aws sns subscribe --topic-arn $T --protocol sqs --notification-endpoint $A --query SubscriptionArn --output text
    Set-Variable -Name "${n}_SUB" -Value $S
  }
  aws sns list-subscriptions-by-topic --topic-arn $T --query "Subscriptions[].[Protocol,SubscriptionArn]" --output text
  ```
* **Bash (EC2 / WSL):**
  ```bash
  T=$(aws sns create-topic --name corecompute-lab-order-events --query TopicArn --output text)
  for n in inventory analytics; do
    U=$(aws sqs create-queue --queue-name corecompute-lab-$n-queue --query QueueUrl --output text)
    A=$(aws sqs get-queue-attributes --queue-url $U --attribute-names QueueArn --query Attributes.QueueArn --output text)
    python3 -c "import json,sys; print(json.dumps({'Policy': json.dumps({'Version':'2012-10-17','Statement':[{'Effect':'Allow','Principal':{'Service':'sns.amazonaws.com'},'Action':'sqs:SendMessage','Resource':sys.argv[1],'Condition':{'ArnEquals':{'aws:SourceArn':sys.argv[2]}}}]})}))" $A $T > pol.json
    aws sqs set-queue-attributes --queue-url $U --attributes file://pol.json
    S=$(aws sns subscribe --topic-arn $T --protocol sqs --notification-endpoint $A --query SubscriptionArn --output text)
    eval "${n}_SUB=$S"
  done
  aws sns list-subscriptions-by-topic --topic-arn $T --query "Subscriptions[].[Protocol,SubscriptionArn]" --output text
  ```

### 2. Add Filter Policy to Analytics Subscription
* **PowerShell (Windows):**
  ```powershell
  aws sns set-subscription-attributes --subscription-arn $analytics_SUB --attribute-name FilterPolicy --attribute-value '{\"eventType\": [\"order_cancelled\"]}'
  ```
* **Bash (EC2 / WSL):**
  ```bash
  aws sns set-subscription-attributes --subscription-arn $analytics_SUB --attribute-name FilterPolicy --attribute-value '{"eventType": ["order_cancelled"]}'
  ```

### 3. Publish Two Messages & Verify Queue Counts
* **PowerShell (Windows):**
  ```powershell
  aws sns publish --topic-arn $T --subject "Order placed" --message '{\"orderId\": 301, \"status\": \"placed\"}' --message-attributes '{\"eventType\":{\"DataType\":\"String\",\"StringValue\":\"order_placed\"}}'
  aws sns publish --topic-arn $T --subject "Order cancelled" --message '{\"orderId\": 302, \"status\": \"cancelled\"}' --message-attributes '{\"eventType\":{\"DataType\":\"String\",\"StringValue\":\"order_cancelled\"}}'
  ```
* **Bash (EC2 / WSL):**
  ```bash
  aws sns publish --topic-arn $T --subject "Order placed" --message '{"orderId": 301, "status": "placed"}' --message-attributes '{"eventType":{"DataType":"String","StringValue":"order_placed"}}'
  aws sns publish --topic-arn $T --subject "Order cancelled" --message '{"orderId": 302, "status": "cancelled"}' --message-attributes '{"eventType":{"DataType":"String","StringValue":"order_cancelled"}}'
  ```

*(Verify in **AWS Console → SQS → Queues**: `inventory` has 2 messages, `analytics` has 1 message).*

---

## Lab 5: A Python Pipeline into DynamoDB

**Goal:** Batch-send 5 orders to SQS and build an idempotent consumer using DynamoDB conditional writes (`attribute_not_exists(orderId)`).

### 1. Create the DynamoDB Table
* **PowerShell / Bash:**
  ```bash
  aws dynamodb create-table --table-name corecompute-lab-processed-orders --attribute-definitions AttributeName=orderId,AttributeType=N --key-schema AttributeName=orderId,KeyType=HASH --billing-mode PAY_PER_REQUEST --query TableDescription.TableStatus --output text
  ```

### 2. Create `producer.py`:
```python
import json
import boto3

sqs = boto3.client("sqs")
url = sqs.get_queue_url(QueueName="corecompute-lab-orders")["QueueUrl"]
entries = [{"Id": str(i), "MessageBody": json.dumps({"orderId": 200 + i})}
           for i in range(5)]
resp = sqs.send_message_batch(QueueUrl=url, Entries=entries)
print("Sent", len(resp["Successful"]), "messages in one API call")
```

### 3. Create `consumer.py`:
```python
import json
import boto3
from botocore.exceptions import ClientError

sqs = boto3.client("sqs")
url = sqs.get_queue_url(QueueName="corecompute-lab-orders")["QueueUrl"]
table = boto3.resource("dynamodb").Table("corecompute-lab-processed-orders")

def save(order):
    table.put_item(Item={"orderId": order["orderId"], "status": "PROCESSED"},
                   ConditionExpression="attribute_not_exists(orderId)")

while True:
    resp = sqs.receive_message(QueueUrl=url, MaxNumberOfMessages=10,
                               WaitTimeSeconds=20)   # long polling
    messages = resp.get("Messages", [])
    if not messages:
        print("Queue empty, stopping.")
        break
    for m in messages:
        try:
            order = json.loads(m["Body"])
            save(order)
            print("Saved order", order["orderId"])
        except ClientError as e:
            if e.response["Error"]["Code"] != "ConditionalCheckFailedException":
                raise
            print("Duplicate order", order["orderId"], "- already saved")
        except (ValueError, KeyError):
            print("Bad message, leaving it for the DLQ:", m["Body"][:30])
            continue
        sqs.delete_message(QueueUrl=url, ReceiptHandle=m["ReceiptHandle"])
```

### 4. Purge Orders Queue & Run Pipeline Twice
> [!IMPORTANT]
> Wait 60 seconds after purging `corecompute-lab-orders` so old test messages from Labs 1 & 2 are gone.

* **PowerShell (Windows):**
  ```powershell
  aws sqs purge-queue --queue-url $Q
  Start-Sleep 60
  python producer.py
  python consumer.py
  python producer.py   # send the same five again
  python consumer.py   # prints Duplicate for each
  aws dynamodb scan --table-name corecompute-lab-processed-orders --select COUNT --query Count --output text
  ```
* **Bash (EC2 / WSL):**
  ```bash
  aws sqs purge-queue --queue-url $Q
  sleep 60
  python3 producer.py
  python3 consumer.py
  python3 producer.py  # send the same five again
  python3 consumer.py  # prints Duplicate for each
  aws dynamodb scan --table-name corecompute-lab-processed-orders --select COUNT --query Count --output text
  ```

---

## Lab 6: Clean Up

Delete all queues, SNS topic, subscriptions, and the DynamoDB table:

* **PowerShell (Windows):**
  ```powershell
  aws sqs delete-queue --queue-url $Q
  aws sqs delete-queue --queue-url $DLQ
  aws sqs delete-queue --queue-url $F
  aws sqs delete-queue --queue-url (aws sqs get-queue-url --queue-name corecompute-lab-inventory-queue --query QueueUrl --output text)
  aws sqs delete-queue --queue-url (aws sqs get-queue-url --queue-name corecompute-lab-analytics-queue --query QueueUrl --output text)
  aws sns delete-topic --topic-arn $T
  aws dynamodb delete-table --table-name corecompute-lab-processed-orders
  ```
* **Bash (EC2 / WSL):**
  ```bash
  aws sqs delete-queue --queue-url $Q
  aws sqs delete-queue --queue-url $DLQ
  aws sqs delete-queue --queue-url $F
  aws sqs delete-queue --queue-url $(aws sqs get-queue-url --queue-name corecompute-lab-inventory-queue --query QueueUrl --output text)
  aws sqs delete-queue --queue-url $(aws sqs get-queue-url --queue-name corecompute-lab-analytics-queue --query QueueUrl --output text)
  aws sns delete-topic --topic-arn $T
  aws dynamodb delete-table --table-name corecompute-lab-processed-orders
  ```
