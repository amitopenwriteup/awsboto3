from flask import Flask, request, render_template, redirect, url_for
import boto3
import ipaddress

app = Flask(__name__)

# Initialize boto3 EC2 client
session = boto3.Session(profile_name='default')
ec2 = session.client('ec2')

# Function to calculate subnet CIDRs
def calculate_subnet_cidr(vpc_cidr, num_subnets):
    """
    This function calculates and returns a list of subnet CIDR blocks 
    that fit within the provided VPC CIDR.
    """
    network = ipaddress.IPv4Network(vpc_cidr)
    subnet_size = network.prefixlen + (num_subnets - 1).bit_length()  # Calculate subnet size

    subnet_cidrs = list(network.subnets(new_prefix=subnet_size))
    return [str(subnet) for subnet in subnet_cidrs[:num_subnets]]

# Route for creating subnets for the specified VPC
@app.route('/create_subnets', methods=['GET', 'POST'])
def create_subnets_page():
    vpc_id = request.args.get('vpc_id')
    cidr_block = request.args.get('cidr')

    if request.method == 'POST':
        num_subnets = request.form.get('num_subnets')
        
        # Validate the number of subnets input
        if num_subnets and num_subnets.isdigit():
            num_subnets = int(num_subnets)
            
            if num_subnets < 1:
                return "❌ The number of subnets must be at least 1."
            
            # Calculate subnet CIDR blocks
            subnets_cidr = calculate_subnet_cidr(cidr_block, num_subnets)
            
            # Create the subnets
            subnets = create_subnets(vpc_id, subnets_cidr)
            return f"✅ Created {len(subnets)} subnets in VPC {vpc_id}"
        else:
            return "❌ Please provide a valid number for subnets."
    
    return render_template('subnet_creation.html', vpc_id=vpc_id, cidr=cidr_block)

# Function to create subnets in the specified VPC
def create_subnets(vpc_id, subnets_cidr):
    subnets = []
    for subnet_cidr in subnets_cidr:
        new_subnet = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=subnet_cidr,
            AvailabilityZone='us-east-1a'  # Use the correct AZ for your region
        )
        subnets.append(new_subnet)
    return subnets

# Route for managing VPCs (Creating new VPC or confirming deletion of existing ones)
@app.route('/', methods=['GET', 'POST'])
def manage_vpc():
    # List existing VPCs
    existing_vpcs = ec2.describe_vpcs()['Vpcs']
    
    # If a CIDR is passed in query params, check if that CIDR block exists
    cidr_block = request.args.get('cidr', '').strip()

    if request.method == 'POST':
        cidr_block = request.form.get('cidr', '').strip()

        # Validate the CIDR block input
        if not cidr_block:
            return "❌ CIDR block cannot be empty. Please go back and enter a valid one."

        # Check if VPC with given CIDR block exists
        existing_vpcs = ec2.describe_vpcs(Filters=[{'Name': 'cidr-block', 'Values': [cidr_block]}])['Vpcs']

        if existing_vpcs:
            vpc_id = existing_vpcs[0]['VpcId']
            if 'confirm_delete' in request.form:
                if cleanup_vpc(vpc_id):
                    new_vpc = ec2.create_vpc(CidrBlock=cidr_block)
                    # Redirect to the page to create subnets for the new VPC
                    return redirect(url_for('create_subnets_page', vpc_id=new_vpc['Vpc']['VpcId'], cidr=cidr_block))
                else:
                    return "❌ Failed to delete existing VPC due to dependencies."
            else:
                return render_template('vpc_creation.html', exists=True, cidr=cidr_block, vpcs=existing_vpcs)

        # If no VPC exists with the given CIDR block, create a new VPC
        new_vpc = ec2.create_vpc(CidrBlock=cidr_block)
        # Redirect to the page to create subnets for the new VPC
        return redirect(url_for('create_subnets_page', vpc_id=new_vpc['Vpc']['VpcId'], cidr=cidr_block))

    return render_template('vpc_creation.html', exists=False, vpcs=existing_vpcs)

# Function to clean up VPC (delete subnets, security groups, etc.)
def cleanup_vpc(vpc_id):
    try:
        # Describe the VPC to find associated resources
        vpc_info = ec2.describe_vpcs(VpcIds=[vpc_id])['Vpcs'][0]

        # First, delete the subnets within this VPC
        subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['Subnets']
        for subnet in subnets:
            ec2.delete_subnet(SubnetId=subnet['SubnetId'])

        # Delete any security groups (except the default one)
        security_groups = ec2.describe_security_groups(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['SecurityGroups']
        for sg in security_groups:
            if sg['GroupName'] != 'default':
                ec2.delete_security_group(GroupId=sg['GroupId'])

        # Finally, delete the VPC
        ec2.delete_vpc(VpcId=vpc_id)
        return True
    except Exception as e:
        print(f"Error deleting VPC {vpc_id}: {e}")
        return False

if __name__ == '__main__':
   # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)

