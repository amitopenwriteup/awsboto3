import boto3

# Create a boto3 session (use profile_name if needed)
session = boto3.Session()  # Or: boto3.Session(profile_name='your-profile')

# Get available resources
resources = session.get_available_resources()

# Print available resources
print("Available Boto3 Resources:")
for resource in resources:
    print(resource)
