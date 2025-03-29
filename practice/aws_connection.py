import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch credentials from environment variables
access_key_id = os.getenv("AWS_ACCESS_KEY_ID")  # Use string key
secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("AWS_REGION", "us-east-1")  # Default to us-east-1 if not set



# Create S3 client and resource
s3_client = boto3.client('s3', 
                          aws_access_key_id=access_key_id, 
                          aws_secret_access_key=secret_access_key, 
                          region_name=region_name)

s3_resource = boto3.resource('s3', 
                              aws_access_key_id=access_key_id, 
                              aws_secret_access_key=secret_access_key, 
                              region_name=region_name)


# List all buckets  
response = s3_client.list_buckets()
print("S3 Buckets:", [bucket["Name"] for bucket in response["Buckets"]])



