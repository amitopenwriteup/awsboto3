import boto3

# Initialize session (default or specific profile)
session = boto3.Session(profile_name='default')  # Or omit for default
ec2_client = session.client('ec2')

# Step 1: List existing VPCs
print("Existing VPCs:")
vpcs = ec2_client.describe_vpcs()['Vpcs']
for vpc in vpcs:
    print(f"VPC ID: {vpc['VpcId']}, CIDR: {vpc['CidrBlock']}")

# Step 2: Prompt user to create new VPC
choice = input("\nDo you want to create a new VPC? (yes/no): ").strip().lower()

if choice == 'yes':
    cidr_block = input("Enter CIDR block for the new VPC (e.g., 10.0.0.0/16): ").strip()
    
    # Step 3: Check for existing VPC with same CIDR
    existing_vpc = next((vpc for vpc in vpcs if vpc['CidrBlock'] == cidr_block), None)
    
    if existing_vpc:
        print(f"\n⚠️ A VPC with CIDR {cidr_block} already exists (VPC ID: {existing_vpc['VpcId']})")
        delete_choice = input("Do you want to delete and recreate it? (yes/no): ").strip().lower()
        
        if delete_choice == 'yes':
            # Delete the existing VPC
            ec2_client.delete_vpc(VpcId=existing_vpc['VpcId'])
            print(f"Deleted VPC: {existing_vpc['VpcId']}")
            
            # Optional: wait for VPC deletion to complete
            # (no direct waiter for VPC deletion; may need sleep/retry for production use)
        else:
            print("VPC not deleted. Exiting.")
            exit()
    
    # Step 4: Create new VPC
    new_vpc = ec2_client.create_vpc(CidrBlock=cidr_block)
    new_vpc_id = new_vpc['Vpc']['VpcId']
    ec2_client.get_waiter('vpc_available').wait(VpcIds=[new_vpc_id])
    print(f"\n✅ New VPC created:")
    print(f"VPC ID: {new_vpc_id}, CIDR Block: {cidr_block}")
else:
    print("No VPC was created.")

