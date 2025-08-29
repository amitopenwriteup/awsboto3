
# AWS VPC Automation with Python

This repository contains Python scripts and templates to automate **AWS VPC creation, subnet management, and resource configuration**.  
It helps in provisioning cloud infrastructure programmatically instead of manual setup.

## 📂 Repository Structure

```

.
├── templates/              # HTML templates (if using Flask/Django UI)
├── app.py                  # Main application file
├── availableresource.py    # Script to check available AWS resources
├── createvpc.py            # Script to create a VPC
├── vpcoverwrite.py         # Script for VPC overwrite/update
├── vpcprint.py             # Script to print VPC details
├── vpcsusbnet.py           # Script for creating/managing subnets
├── awsconfigure/           # AWS configuration files
├── requirements.txt        # Python dependencies
├── Dockerfile              # Containerization file
├── kubernetes-manifest.yaml# Kubernetes deployment file
├── Jenkinsfile             # Jenkins pipeline
├── cloudbuild.yaml         # GCP Cloud Build pipeline
└── README.md               # Project documentation (you are here!)

````

## 🚀 Features

- Create and manage AWS VPCs using Python.
- Automate subnet creation and resource allocation.
- CLI-based scripts for AWS networking.
- Docker & Kubernetes support for deployment.
- CI/CD integration with Jenkins & Cloud Build.
- SonarQube + Slack integration for code quality and notifications.

## ⚙️ Prerequisites

- Python 3.8+
- AWS CLI configured (`aws configure`)
- Boto3 (`pip install boto3`)
- Docker (optional, for containerized runs)
- Kubernetes (optional, for k8s deployments)

## 📦 Installation

```bash
git clone https://github.com/amitopenwriteup/<your-repo>.git
cd <your-repo>
pip install -r requirements.txt
````

## ▶️ Usage

### Create a VPC

```bash
python createvpc.py
```

### List VPCs

```bash
python vpcprint.py
```

### Create Subnet

```bash
python vpcsusbnet.py
```

## 🐳 Run with Docker

```bash
docker build -t aws-vpc-automation .
docker run --rm aws-vpc-automation
```

## ☸️ Deploy on Kubernetes

```bash
kubectl apply -f kubernetes-manifest.yaml
```

## 🔄 CI/CD Integration

* **Jenkins** → Uses `Jenkinsfile`
* **Google Cloud Build** → Uses `cloudbuild.yaml`
* **SonarQube + Slack** → For code scanning & notifications

## 📌 Roadmap

* Add support for Security Groups and Route Tables.
* Implement Terraform/CloudFormation templates.
* Build a simple web UI for managing VPCs.

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

## 📜 License

This project is licensed under the MIT License.

```
