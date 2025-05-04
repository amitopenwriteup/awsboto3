from flask import Flask, render_template, request, redirect, url_for
import boto3
import ipaddress

app = Flask(__name__)
session = boto3.Session(profile_name='default')
ec2 = session.client('ec2')

def list_vpcs():
    return ec2.describe_vpcs()['Vpcs']

@app.route('/')
def index():
    vpcs = list_vpcs()
    return render_template('index.html', vpcs=vpcs)

@app.route('/create-vpc', methods=['GET', 'POST'])
def create_vpc():
    if request.method == 'POST':
        cidr_block = request.form['cidr']
        vpcs = list_vpcs()
        existing_vpc = next((v for v in vpcs if v['CidrBlock'] == cidr_block), None)
        if existing_vpc:
            if request.form.get('confirm') == 'yes':
                ec2.delete_vpc(VpcId=existing_vpc['VpcId'])
            else:
                return render_template('create_vpc.html', exists=True, cidr=cidr_block)

        new_vpc = ec2.create_vpc(CidrBlock=cidr_block)
        ec2.get_waiter('vpc_available').wait(VpcIds=[new_vpc['Vpc']['VpcId']])
        return redirect(url_for('create_subnets', vpc_id=new_vpc['Vpc']['VpcId'], cidr=cidr_block))
    return render_template('create_vpc.html')

@app.route('/create-subnets', methods=['GET', 'POST'])
def create_subnets():
    vpc_id = request.args.get('vpc_id')
    cidr_block = request.args.get('cidr')

    if request.method == 'POST':
        count = int(request.form['count'])
        vpc_network = ipaddress.IPv4Network(cidr_block)
        new_prefix = vpc_network.prefixlen + (count - 1).bit_length()
        subnets = list(vpc_network.subnets(new_prefix=new_prefix))[:count]

        subnet_list = []
        for subnet in subnets:
            response = ec2.create_subnet(VpcId=vpc_id, CidrBlock=str(subnet))
            subnet_list.append((response['Subnet']['SubnetId'], str(subnet)))

        return render_template('create_subnets.html', vpc_id=vpc_id, subnets=subnet_list)

    return render_template('create_subnets.html', vpc_id=vpc_id, cidr=cidr_block)

if __name__ == '__main__':
    app.run(debug=True)

