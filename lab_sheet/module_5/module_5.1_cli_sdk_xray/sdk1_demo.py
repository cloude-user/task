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