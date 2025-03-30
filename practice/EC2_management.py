import boto3

# Initialize EC2 client
ec2 = boto3.client("ec2", region_name="us-east-1")  # Change region if needed

# Function to get the latest Amazon Linux 2 AMI ID (Free Tier)
def get_latest_ami():
    ssm = boto3.client("ssm", region_name="us-east-1")
    response = ssm.get_parameter(Name="/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2")
    return response["Parameter"]["Value"]

# Function to create a Free Tier EC2 instance
def create_instance():
    ami_id = get_latest_ami()
    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType="t2.micro",  # Free Tier eligible
        MinCount=1,
        MaxCount=1,
        KeyName="my_demo",  # Update with your key pair
        SecurityGroups=["default"],   # Update with your security group 
                                      # Allows SSH (22) for remote access.
                                      # Allows HTTP (80) for web applications.
                                      # Allows HTTPS (443) for secure web traffic.
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": "MyFreeTierInstance"}],
            }
        ],
    )
    instance_id = response["Instances"][0]["InstanceId"]
    print(f"EC2 Instance {instance_id} created successfully!")
    return instance_id

# Function to list all EC2 instances
def list_instances():
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")

# Function to start an EC2 instance
def start_instance(instance_id):
    ec2.start_instances(InstanceIds=[instance_id])
    print(f"Instance {instance_id} is starting...")

# Function to stop an EC2 instance
def stop_instance(instance_id):
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Instance {instance_id} is stopping...")

# Function to terminate an EC2 instance
def terminate_instance(instance_id):
    ec2.terminate_instances(InstanceIds=[instance_id])
    print(f"Instance {instance_id} is terminating...")

# Run functions
if __name__ == "__main__":
    #instance_id = create_instance()
    #list_instances()
    #start_instance(instance_id)
    #stop_instance(instance_id='i-0223fadcfe28801ce')
    terminate_instance(instance_id='i-0b9294a5d45b04fc7')
