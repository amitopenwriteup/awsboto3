import boto3

# Initialize session using credentials from ~/.aws/credentials
session = boto3.Session(profile_name='default')  # Replace with your profile name or remove for default
ec2_client = session.client('ec2')

# Step 1: List existing VPCs
print("Existing VPCs:")
vpcs = ec2_client.describe_vpcs()['Vpcs']
for vpc in vpcs:
    print(f"VPC ID: {vpc['VpcId']}, CIDR: {vpc['CidrBlock']}")

# Step 2: Ask user if they want to create a new VPC
choice = input("\nDo you want to create a new VPC? (yes/no): ").strip().lower()

if choice == 'yes':
    cidr_block = input("Enter CIDR block for the new VPC (e.g., 10.0.0.0/16): ").strip()
    
    # Step 3: Create the new VPC
    response = ec2_client.create_vpc(CidrBlock=cidr_block)
    new_vpc_id = response['Vpc']['VpcId']
    
    # Optionally wait until VPC is available
    ec2_client.get_waiter('vpc_available').wait(VpcIds=[new_vpc_id])
    
    print(f"\n✅ New VPC created:")
    print(f"VPC ID: {new_vpc_id}, CIDR Block: {cidr_block}")
else:
    print("No VPC was created.")

