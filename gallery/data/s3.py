import logging
import boto3
from botocore.exceptions import ClientError
import os

S3_BUCKET = "edu.au.cc.dzr-0056.image-gallery-2"

def add_image(file_name, path):
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.put_object(Body=file_name, Bucket=S3_BUCKET, Key=path)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_image(path):
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.get_object(Key=path, Bucket=S3_BUCKET)
    except ClientError as e:
        logging.error(e)
        return False
    return True
