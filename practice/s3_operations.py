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

# Initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

# Define bucket name
bucket_name = "emmy-database-1"  # Change this to your bucket name

# List all buckets
def list_buckets():
    try:
        response = s3_client.list_buckets()
        print("S3 Buckets:")
        for bucket in response["Buckets"]:
            print(f"  - {bucket['Name']}")
    except Exception as e:
        print(f"Error listing buckets: {e}")

# Upload a file
def upload_file(local_file, s3_file):
    try:
        s3_client.upload_file(local_file, bucket_name, s3_file)
        print(f"Uploaded '{local_file}' as '{s3_file}' to '{bucket_name}'")
    except Exception as e:
        print(f"Error uploading file: {e}")

# List files in bucket
def list_files():
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if "Contents" in response:
            print("Files in S3 Bucket:")
            for obj in response["Contents"]:
                print(f"  - {obj['Key']}")
        else:
            print("No files found in the bucket.")
    except Exception as e:
        print(f"Error listing files: {e}")

# Download a file
def download_file(s3_file, local_file):
    try:
        s3_client.download_file(bucket_name, s3_file, local_file)
        print(f"Downloaded '{s3_file}' from '{bucket_name}' to '{local_file}'")
    except Exception as e:
        print(f"Error downloading file: {e}")

# Delete a file
def delete_file(s3_file):
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=s3_file)
        print(f"Deleted '{s3_file}' from '{bucket_name}'")
    except Exception as e:
        print(f"Error deleting file: {e}")

# Check if file exists
def file_exists(s3_file):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=s3_file)
        print(f"File '{s3_file}' exists in '{bucket_name}'")
        return True
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print(f"File '{s3_file}' does not exist in '{bucket_name}'")
            return False
        else:
            print(f"Error checking file existence: {e}")
            return False

# Copy file within S3
def copy_file(source_file, destination_file):
    try:
        copy_source = {"Bucket": bucket_name, "Key": source_file}
        s3_client.copy_object(
            CopySource=copy_source, Bucket=bucket_name, Key=destination_file
        )
        print(f"Copied '{source_file}' to '{destination_file}' in '{bucket_name}'")
    except Exception as e:
        print(f"Error copying file: {e}")

# Generate Pre-signed URL for temporary access
def generate_presigned_url(s3_file, expiration=3600):
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": s3_file},
            ExpiresIn=expiration
        )
        print(f"Generated pre-signed URL for '{s3_file}': {url}")
    except Exception as e:
        print(f"Error generating pre-signed URL: {e}")

# Empty the bucket
def empty_bucket():
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        if "Contents" in response:
            print("Deleting all objects in the bucket...")
            for obj in response["Contents"]:
                s3_client.delete_object(Bucket=bucket_name, Key=obj["Key"])
                print(f"Deleted: {obj['Key']}")
        else:
            print("The bucket is already empty.")
    except Exception as e:
        print(f"Error emptying bucket: {e}")

# Delete S3 bucket
def delete_bucket():
    try:
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"S3 bucket '{bucket_name}' deleted successfully!")
    except Exception as e:
        print(f"Error deleting bucket: {e}")

# Test functions one by one
if __name__ == "__main__":
    local_file_path = "/Users/santoshkumar/Downloads/ANN-Overview.pdf"  # Change this to your local file
    s3_upload_file = "ANN-Overview.pdf"  # S3 file name
    local_download_path = "/Users/santoshkumar/Data_science/aws/ANN-Overview-downloaded.pdf"  # Where to save the downloaded file
    # Uncomment one function at a time to test

    # Step 1: List all buckets
    # list_buckets()

    # Step 2: Upload a file (Change the file path)
    # upload_file(local_file_path, s3_upload_file)

    # Step 3: List all files in bucket
    # list_files()

    # Step 4: Download file (Change file names)
    # download_file(s3_upload_file, local_download_path)

    # Step 5: Copy file
    # copy_file(s3_upload_file, "copied-file.pdf")

    # Step 6: delete a file
    # delete_file(s3_upload_file)

    # Step 7: Check if file exists
    # file_exists("uploaded-file.pdf")

    # Step 8: Generate pre-signed URL
    # generate_presigned_url("copied-file.pdf")

    # Empty the bucket
    # empty_bucket()

    # Step 9: Delete bucket
    # delete_bucket()
