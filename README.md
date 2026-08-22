# Python Application with Docker & GitHub Actions CI/CD to AWS EC2

This repository contains a modern **Python (Flask)** web application configured with **Docker containerization** and a **GitHub Actions CI/CD pipeline** for automated deployment to an **AWS EC2 instance**.

---

## 📁 Repository Structure

```text
.
├── app.py                      # Flask web application & API endpoints
├── test_app.py                 # Pytest unit tests for CI validation
├── Dockerfile                  # Docker build instructions using Gunicorn
├── requirements.txt            # Python dependencies (Flask, Gunicorn, Pytest)
├── .dockerignore               # Docker ignore configuration
├── .gitignore                  # Git ignore rules
├── templates/
│   └── index.html              # Modern dashboard UI with live test widgets
├── static/
│   └── css/style.css           # Glassmorphism aesthetic styles
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline definition
└── README.md                   # Complete documentation & setup instructions
```

---

## 🚀 Quick Start (Local Setup)

### 1. Run with Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run unit tests
pytest -v

# Start application server
python app.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

### 2. Run with Docker Locally
```bash
# Build Docker image
docker build -t python-ec2-app .

# Run container
docker run -p 5000:5000 python-ec2-app
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## ☁️ AWS EC2 & GitHub Actions Deployment Setup

### Step 1: Launch an AWS EC2 Instance
1. Log into your **AWS Management Console** and navigate to **EC2**.
2. Click **Launch Instance**:
   - **AMI**: Ubuntu 22.04 LTS or Amazon Linux 2023.
   - **Instance Type**: `t2.micro` (Free Tier eligible).
   - **Key Pair**: Select or create an SSH key pair (e.g., `ec2-key.pem`).
3. Under **Network Settings** (Security Group rules), add the following inbound rules:
   - **SSH (Port 22)**: Source `0.0.0.0/0` (or your IP).
   - **HTTP (Port 80)**: Source `0.0.0.0/0` (Allows web access).

---

### Step 2: Configure Docker on EC2
Connect to your EC2 instance via SSH:
```bash
ssh -i /path/to/ec2-key.pem ubuntu@<YOUR-EC2-PUBLIC-IP>
```

Run the following commands on the EC2 server:
```bash
# Update system packages
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
sudo apt-get install -y docker.io git

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add ubuntu user to docker group (so sudo is not required)
sudo usermod -aG docker ubuntu

# Apply group changes without logging out
newgrp docker

# Verify docker installation
docker --version
```

---

### Step 3: Configure GitHub Repository Secrets
1. In your GitHub repository, go to **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret** and add the following 3 secrets:

| Secret Name | Description / Value |
| :--- | :--- |
| `EC2_HOST` | The **Public IPv4 Address** or Public DNS of your EC2 instance (e.g., `54.210.xx.xx`). |
| `EC2_USERNAME` | The SSH username for your EC2 AMI (`ubuntu` for Ubuntu, `ec2-user` for Amazon Linux). |
| `EC2_SSH_KEY` | The full private SSH key content (`.pem` file contents including `-----BEGIN RSA PRIVATE KEY-----`). |

---

### Step 4: Trigger CI/CD Pipeline
1. Commit and push code to your GitHub repository on the `main` branch:
   ```bash
   git add .
   git commit -m "Deploy initial Python app to EC2"
   git push origin main
   ```
2. Navigate to **Actions** tab in GitHub to watch the pipeline execute:
   - **Test Job**: Runs `pytest` unit tests.
   - **Deploy Job**: Connects via SSH to EC2, pulls latest changes, builds the Docker image, and starts the container on **Port 80**.

3. Access your live application at:
   `http://<YOUR-EC2-PUBLIC-IP>`

---

## 🔍 Verifying Deployments & Changes
When you make updates to `app.py` or `index.html` and push to GitHub:
1. GitHub Actions will automatically re-test and re-deploy your app.
2. Visit `http://<YOUR-EC2-PUBLIC-IP>` to see updated version info, server uptime, and test API endpoints live!
