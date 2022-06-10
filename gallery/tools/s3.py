import logging
import boto3
from botocore.exceptions import ClientError

# Create a bucket
def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Add an object
def put_object(bucket_name, key, value):
    try:
        s3_client = boto3.client('s3')
        s3_client.put_object(Bucket=bucket_name, Key=key, Body=value)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Get a project
def get_object(bucket_name, key):
    try:
        s3_client = boto3.client('s3')
        result = s3_client.get_object(Bucket=bucket_name, Key=key)
    except ClientError as e:
        logging.error(e)
        return None

    # returns JSON object
    return result
    

def main():
    # create_bucket('edu.au.cc.dzr-0056.image-gallery-2')
    put_object('edu.au.cc.dzr-0056.image-gallery-2', 'banana', 'yellow')

    # Get the data from the JSON object
    print(get_object('edu.au.cc.dzr-0056.image-gallery-2', 'banana')['Body'].read())


if __name__ == '__main__':
    main()

