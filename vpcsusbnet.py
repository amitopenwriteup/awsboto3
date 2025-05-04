import boto3
import ipaddress

# Initialize session (default or with profile)
session = boto3.Session(profile_name='default')  # Change/remove as needed
ec2 = session.client('ec2')

# Step 1: List current VPCs
print("Existing VPCs:")
vpcs = ec2.describe_vpcs()['Vpcs']
for vpc in vpcs:
    print(f"VPC ID: {vpc['VpcId']}, CIDR: {vpc['CidrBlock']}")

# Step 2: Ask to create new VPC
choice = input("\nDo you want to create a new VPC? (yes/no): ").strip().lower()

if choice != 'yes':
    print("No VPC was created.")
    exit()

cidr_block = input("Enter CIDR block for the new VPC (e.g., 10.0.0.0/16): ").strip()

# Check for existing VPC with same CIDR
existing_vpc = next((vpc for vpc in vpcs if vpc['CidrBlock'] == cidr_block), None)

if existing_vpc:
    print(f"\n⚠️ VPC with CIDR {cidr_block} already exists (ID: {existing_vpc['VpcId']})")
    delete = input("Do you want to delete and recreate it? (yes/no): ").strip().lower()
    if delete == 'yes':
        ec2.delete_vpc(VpcId=existing_vpc['VpcId'])
        print(f"Deleted VPC: {existing_vpc['VpcId']}")
    else:
        print("VPC not deleted. Exiting.")
        exit()

# Create new VPC
new_vpc = ec2.create_vpc(CidrBlock=cidr_block)
vpc_id = new_vpc['Vpc']['VpcId']
ec2.get_waiter('vpc_available').wait(VpcIds=[vpc_id])
print(f"\n✅ New VPC created: {vpc_id} ({cidr_block})")

# Step 3: Ask to create subnets
subnet_choice = input("\nDo you want to create subnets in this VPC? (yes/no): ").strip().lower()

if subnet_choice == 'yes':
    count = int(input("How many subnets do you want to create?: ").strip())
    
    # Calculate subnet CIDRs
    vpc_network = ipaddress.IPv4Network(cidr_block)
    new_prefix = vpc_network.prefixlen + (count - 1).bit_length()  # Calculate new prefix for equal split
    
    if new_prefix > 28:
        print("Too many subnets requested for this CIDR block.")
        exit()

    subnets = list(vpc_network.subnets(new_prefix=new_prefix))[:count]

    print(f"\nCreating {count} subnets:")
    for i, subnet in enumerate(subnets):
        subnet_resp = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=str(subnet)
        )
        subnet_id = subnet_resp['Subnet']['SubnetId']
        print(f"Subnet {i+1}: {subnet_id}, CIDR: {subnet}")

else:
    print("No subnets created.")

