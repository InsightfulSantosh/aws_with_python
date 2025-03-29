# AWS Automation with Boto3

This project provides Python scripts to automate AWS services using Boto3. It includes functionalities for managing S3, IAM, EC2, DynamoDB, Lambda, ECR, SageMaker, and more.

---

## Features

### 🚀 **S3 (Simple Storage Service)**
- List all S3 buckets
- Upload a file to an S3 bucket
- List files in a bucket
- Download a file from S3
- Delete a file from S3
- Check if a file exists
- Copy files within S3
- Generate a pre-signed URL for temporary file access
- Empty and delete an S3 bucket

### 🔐 **IAM (Identity and Access Management)**
- Create an IAM user
- Attach policies to an IAM user
- Grant full S3 access to an IAM user
- Create and manage IAM roles

### 💻 **EC2 (Elastic Compute Cloud)**
- List all EC2 instances
- Start and stop EC2 instances
- Terminate an EC2 instance
- Create and attach security groups

### 📦 **ECR (Elastic Container Registry)**
- Create an ECR repository
- Authenticate Docker to AWS ECR
- Push and pull Docker images

### 🧠 **SageMaker**
- Create a SageMaker notebook instance
- Train a machine learning model
- Deploy a trained model as an endpoint
- Invoke the endpoint for inference

### 🔢 **DynamoDB (NoSQL Database)**
- Create a DynamoDB table
- Insert and retrieve data
- Delete records from DynamoDB

### ⚡ **Lambda**
- Deploy and invoke AWS Lambda functions


---

## 🛠 **Prerequisites**

- **Python 3.x** installed
- **AWS CLI** configured with necessary permissions
- Required Python packages installed:
  
  ```bash
  pip install boto3 python-dotenv

