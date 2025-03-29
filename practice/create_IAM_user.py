import boto3

# Create an IAM client
iam_client = boto3.client('iam')

# Define user
user_name = "emmy"

# AWS Admin Policy ARN
admin_policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"

try:
    # Create the IAM user
    response = iam_client.create_user(UserName=user_name)
    print(f"IAM User '{user_name}' created successfully!")
except Exception as e:
    print(f"Error creating user '{user_name}': {e}")

########################## attach policy ##############################
try:
    # Attach Admin policy to the user
    iam_client.attach_user_policy(UserName=user_name, PolicyArn=admin_policy_arn)
    print(f"Administrator access granted to '{user_name}'")
except Exception as e:
    print(f"Error attaching admin policy to '{user_name}': {e}")
