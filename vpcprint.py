import boto3

#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpcs.html#

# Use AWS credentials from the default profile or specify profile_name
session = boto3.Session(profile_name='default')  # omit profile_name to use default

# Create EC2 client
ec2_client = session.client('ec2')

# Describe all VPCs
response = ec2_client.describe_vpcs()

# Print each VPC ID and its CIDR block
print("Available VPCs:")
for vpc in response['Vpcs']:
    vpc_id = vpc['VpcId']
    cidr_block = vpc['CidrBlock']
    print(f"VPC ID: {vpc_id}, CIDR Block: {cidr_block}")

