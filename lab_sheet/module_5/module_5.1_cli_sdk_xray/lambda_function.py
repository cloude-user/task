import time
import boto3

sts = boto3.client("sts")  # init code: runs once per environment

def lambda_handler(event, context):
    time.sleep(0.3)  # pretend to do some work
    arn = sts.get_caller_identity()["Arn"]
    return {"statusCode": 200, "body": arn}
