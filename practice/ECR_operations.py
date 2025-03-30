import boto3
import os
import subprocess

# Get session credentials dynamically
session = boto3.Session()
credentials = session.get_credentials()

AWS_REGION = session.region_name  # Automatically detect region
AWS_ACCOUNT_ID = boto3.client("sts").get_caller_identity()["Account"]  # Fetch Account ID

# Initialize Boto3 ECR client
ecr_client = boto3.client("ecr", region_name=AWS_REGION)

# Repository name
repository_name = "my-ecr-repository1"

def create_repository():
    try:
        response = ecr_client.create_repository(repositoryName=repository_name)
        repo_uri = response["repository"]["repositoryUri"]
        print(f"Repository '{repository_name}' created successfully!")
        print(f"Repository URI: {repo_uri}")
        return repo_uri
    except ecr_client.exceptions.RepositoryAlreadyExistsException:
        print(f"Repository '{repository_name}' already exists.")
        return f"{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/{repository_name}"
    except Exception as e:
        print(f"Error creating repository: {e}")
        return None

def authenticate_docker():
    try:
        subprocess.run(
            f"aws ecr get-login-password --region {AWS_REGION} | "
            f"docker login --username AWS --password-stdin {AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com",
            shell=True, check=True
        )
        print("Docker authenticated successfully with AWS ECR")
    except subprocess.CalledProcessError:
        print("Failed to authenticate Docker")
        exit(1)

def build_docker_image(image_name):
    try:
        print(f"Building Docker image: {image_name}")
        subprocess.run(["docker", "build", "-t", image_name, "."], check=True)
        print(f"Docker image '{image_name}' built successfully!")
    except Exception as e:
        print(f"Error building Docker image: {e}")

def push_docker_image(image_name, tag="latest"):
    try:
        registry_url = f"{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/{repository_name}"
        full_image_name = f"{registry_url}:{tag}"
        
        # Tag the image
        subprocess.run(["docker", "tag", f"{image_name}:{tag}", full_image_name], check=True)
        
        # Push the image
        subprocess.run(["docker", "push", full_image_name], check=True)
        
        print(f"Image '{full_image_name}' pushed successfully!")
    except Exception as e:
        print(f"Error pushing image: {e}")

def list_repositories():
    try:
        response = ecr_client.describe_repositories()
        print("ECR Repositories:")
        for repo in response["repositories"]:
            print(f"  - {repo['repositoryName']} ({repo['repositoryUri']})")
    except Exception as e:
        print(f"Error listing repositories: {e}")

def pull_docker_image(image_name, tag="latest"):
    try:
        registry_url = f"{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/{repository_name}"
        full_image_name = f"{registry_url}:{tag}"
    
        print(f"Pulling image: {full_image_name} ...")
        
        # Pull the image
        subprocess.run(["docker", "pull", full_image_name], check=True)
        
        print(f"Image '{full_image_name}' pulled successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Failed to pull image: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def delete_repository():
    try:
        ecr_client.delete_repository(repositoryName=repository_name, force=True)
        print(f"Repository '{repository_name}' deleted successfully!")
    except Exception as e:
        print(f"Error deleting repository: {e}")

if __name__ == "__main__":
    repo_uri = create_repository()
    
    if repo_uri:
        # authenticate_docker()
        # build_docker_image("my-python-app")
        # push_docker_image("my-python-app")
        # list_repositories()
        #pull_docker_image('my-python-app')
        delete_repository()  
