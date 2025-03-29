import boto3
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

# Validate credentials
if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not AWS_REGION:
    raise ValueError("Missing AWS credentials in .env file!")

# Define bucket name and AWS region
bucket_name = "emmy-database-1"  # Change to a unique name
region = AWS_REGION  # Use actual env variable

# Define IAM Users who should have full access
user_arns = [
    "arn:aws:iam::537124964633:user/emmy"
]

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=region
)

# Create the S3 bucket
try:
    if region == "us-east-1":
        s3_client.create_bucket(Bucket=bucket_name)  # No location constraint for us-east-1
    else:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
    print(f"S3 bucket '{bucket_name}' created successfully!")
except Exception as e:
    print(f"Error creating bucket: {e}")

# Wait for the bucket to be fully available
import time
time.sleep(5)

################################ Provide Policy #############################
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": user_arns},
            "Action": "s3:*",
            "Resource": [
                f"arn:aws:s3:::{bucket_name}",
                f"arn:aws:s3:::{bucket_name}/*"
            ]
        }
    ]
}

# Convert policy to JSON
bucket_policy_json = json.dumps(bucket_policy)

# Attach the bucket policy
try:
    s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy_json)
    print(f"Bucket policy applied successfully to '{bucket_name}'!")
except Exception as e:
    print(f"Error applying bucket policy: {e}")
