# 🚀 GitHub Actions & DevSecOps Master Interview Revision Guide

> **Target Role:** DevOps Administrator / GitHub Actions Enterprise Specialist  
> **Repository Baseline:** Python Flask App + Docker + AWS EC2 + 6-Stage DevSecOps Pipeline

---

## 📌 Table of Contents
1. [Core Repository & App Architecture](#1-core-repository--app-architecture)
2. [The 6-Stage DevSecOps CI/CD Pipeline](#2-the-6-stage-devsecops-cicd-pipeline)
3. [DevSecOps Tool Matrix (SAST, SCA, Linters & CSPM)](#3-devsecops-tool-matrix)
4. [GitHub Actions Concepts: Basic, Intermediate & Advanced](#4-github-actions-concepts-hierarchy)
5. [Enterprise Concepts: OIDC Keyless Cloud Auth](#5-enterprise-concept-openid-connect-oidc)
6. [Azure DevOps (ADO) to GitHub Migration Strategy](#6-azure-devops-ado-to-github-migration-strategy)
7. [Self-Hosted Runners & Kubernetes ARC](#7-self-hosted-runners--actions-runner-controller-arc)
8. [Top 12 Interview Scenarios & Senior Answers](#8-top-12-interview-scenarios--senior-answers)

---

## 1. Core Repository & App Architecture

### Stack Components:
- **Application**: Flask Python Web App (`app.py`) with health check (`/health`), system metadata (`/api/info`), and interactive state counter (`/api/counter`).
- **Production Server**: Gunicorn WSGI Server running inside Docker.
- **Base Image**: `python:3.11-slim` containerized via `Dockerfile`.
- **Testing**: `pytest` unit test suite in `test_app.py`.

---

## 2. The 6-Stage DevSecOps CI/CD Pipeline

Defined in `.github/workflows/deploy.yml`:

```text
               ┌─────────────────────────────────────┐
               │ 🔍 1. Code Quality & Syntax (Flake8) │
               └─────────────────────────────────────┘
                                  │
                                  ▼
               ┌─────────────────────────────────────┐
               │ 🧪 2. Automated Unit Testing (Pytest)│
               └─────────────────────────────────────┘
                                  │
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
┌───────────────────────────┐             ┌───────────────────────────┐
│ 🛡️ 3. Code Security SAST  │             │ 📦 4. Dependency SCA Audit│
│       Scan (Bandit)       │             │       Scan (Snyk)         │
└───────────────────────────┘             └───────────────────────────┘
         │                                                 │
         └────────────────────────┬────────────────────────┘
                                  ▼
               ┌─────────────────────────────────────┐
               │ 🐳 5. Container Image Build & Test  │
               └─────────────────────────────────────┘
                                  │
                                  ▼
               ┌─────────────────────────────────────┐
               │ 🚀 6. Production AWS EC2 Deployment │
               └─────────────────────────────────────┘
```

### Stage Summary Table:

| Stage # & Job Name | Trigger / Tool | Primary Purpose |
| :--- | :--- | :--- |
| **1. `lint`** | `flake8` | Validates Python code formatting & syntax rules. |
| **2. `unit_test`** | `pytest` | Executes automated functional unit tests. |
| **3. `sast_scan`** | `bandit -r app.py -s B104` | Scans custom Python source code for security vulnerabilities. |
| **4. `sca_scan`** | `snyk/actions/python` | Audits `requirements.txt` dependencies and monitors snapshots on Snyk Dashboard. |
| **5. `container_scan`** | `docker build` | Builds & verifies Docker container layer integrity. |
| **6. `prod_deploy`** | `appleboy/ssh-action` | Auto-provisions Docker on EC2 (if needed) & deploys container to HTTP Port 80 over SSH. |

---

## 3. DevSecOps Tool Matrix

### Multi-Language Linter Matrix:
| Language / Tech | Primary Linter Tool | What It Checks |
| :--- | :--- | :--- |
| **Python** | `flake8` / `Ruff` | PEP 8 styling, syntax errors, unused imports. |
| **Java** | `Checkstyle` / `PMD` / `SpotBugs` | Java coding standards, code smells, bug patterns. |
| **Node.js (JavaScript)** | `ESLint` | Standard JS syntax and logic checks. |
| **React.js** | `ESLint` (`eslint-plugin-react`) | React Hooks rules, JSX syntax, prop validation. |
| **TypeScript** | `ESLint` (`@typescript-eslint`) | Type checking, strict TS rules. |
| **Docker** | `Hadolint` | Dockerfile best practices & syntax. |
| **Terraform (IaC)** | `tflint` / `Checkov` | Infrastructure as Code misconfigurations. |

### Security Tools Comparison:
| Tool | Security Category | Target Scanned | Real-World Vulnerability Fixed |
| :--- | :--- | :--- | :--- |
| **Bandit** | **SAST** (Static Code Security) | Custom Python code (`app.py`) | Flagged `debug=True` in `app.run()`. |
| **Snyk (SCA)** | **SCA** (Software Composition) | 3rd-party packages (`requirements.txt`) | Upgraded `Flask` to `3.1.3` & `gunicorn` to `23.0.0` (Fixed HTTP Smuggling CVE). |
| **Snyk (Container)** | **Container Security** | `Dockerfile` & OS packages | Scans base OS image for Linux CVEs. |
| **Orca Security** | **CSPM / CWPP** (Cloud Security) | AWS EC2 / Azure Cloud Infrastructure | Agentless cloud scanning for misconfigured Security Groups & open ports. |

---

## 4. GitHub Actions Concepts Hierarchy

### 🟢 Basic Concepts:
- **Workflows**: YAML files under `.github/workflows/`.
- **Triggers (`on:`)**: Events like `push`, `pull_request`, `schedule`, `workflow_dispatch`.
- **Jobs & Steps**: `jobs:` contain sequential `steps:` (`uses:` or `run:`).
- **Runners**: Cloud VMs (`runs-on: ubuntu-latest`).

### 🟡 Intermediate Concepts:
- **Secrets vs Variables**: `${{ secrets.SNYK_TOKEN }}` (Encrypted sensitive data) vs `${{ vars.EC2_HOST }}` (Plaintext metadata).
- **DAG Job Dependencies (`needs:`)**: Building multi-stage visual pipeline graphs (`needs: [sast_scan, sca_scan]`).
- **Conditionals (`if:`)**: Controlling step/job execution (`if: github.ref == 'refs/heads/main'`).
- **Matrix Strategy (`strategy.matrix`)**: Running tests across multiple OS or language versions in parallel.
- **Environments & Reviewers**: `environment: production` requiring manual reviewer sign-off before deployment.

### 🔴 Advanced Concepts:
- **OpenID Connect (OIDC)**: Keyless cloud authentication (no long-lived AWS keys stored in secrets).
- **Centralized Reusable Workflows (`workflow_call`)**: Shared template workflows across an enterprise GitHub Organization.
- **Actions Runner Controller (ARC)**: Auto-scaling ephemeral Kubernetes runners.

---

## 5. Enterprise Concept: OpenID Connect (OIDC)

### **The Problem with Traditional Cloud Credentials:**
Storing permanent AWS Access Keys (`AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY`) in GitHub Secrets introduces security risks if keys are leaked or rotated improperly.

### **The OIDC Solution (Keyless Security):**
1. GitHub Actions runner requests a short-lived OIDC JWT token from GitHub's Identity Provider (`token.actions.githubusercontent.com`).
2. AWS IAM / Azure AD trusts GitHub's Identity Provider.
3. AWS grants a **temporary 1-hour IAM Role session** to the runner.

```yaml
name: Deploy via AWS OIDC
on:
  push:
    branches: [main]

permissions:
  id-token: write  # Grants permission to request the OIDC JWT token
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsEC2DeployRole
          aws-region: us-east-1

      - name: Deploy to Cloud
        run: |
          aws ec2 describe-instances
```

---

## 6. Azure DevOps (ADO) to GitHub Migration Strategy

### 3-Phase Migration Framework:

```text
┌────────────────────────────────┐
│ Phase 1: Repository Migration  │ ──► Use `gh-ado2gh` (GitHub Enterprise Importer)
└────────────────────────────────┘     to preserve commit history, branches & metadata.

┌────────────────────────────────┐
│ Phase 2: Pipeline Conversion   │ ──► Map ADO `azure-pipelines.yml` to GitHub `.github/workflows/*.yml`.
└────────────────────────────────┘     Convert ADO Variable Groups ➔ GitHub Secrets/Variables.
                                       Convert ADO Service Connections ➔ OIDC Authentication.

┌────────────────────────────────┐
│ Phase 3: Governance & Sunset   │ ──► Standardize Reusable Workflows in `.github` org repo.
└────────────────────────────────┘     Enforce Branch Protection Rules & sunset ADO projects.
```

---

## 7. Self-Hosted Runners & Kubernetes ARC

### **When to use Self-Hosted Runners:**
- Applications requiring access to private AWS VPCs / Azure VNets without public exposure.
- Custom hardware requirements (GPUs, high-memory builds).

### **Enterprise Best Practice: Actions Runner Controller (ARC)**
- **What it is**: Kubernetes operator that deploys self-hosted runners as auto-scaling pods on EKS/AKS.
- **Ephemeral Pods**: Each runner pod processes exactly **one job** and terminates immediately, eliminating cross-job file contamination.

---

## 8. Top 12 Interview Scenarios & Senior Answers

### **Q1: How did you fix the Bandit SAST scan failure in your Python project?**
> *"Bandit flagged `debug=True` and `host='0.0.0.0'` in `app.py`. I changed `debug=True` to `debug=False` for production security and passed `-s B104` to Bandit in GitHub Actions to ignore container 0.0.0.0 binding false positives while maintaining full code security scanning."*

### **Q2: How did you remediate Snyk dependency vulnerabilities?**
> *"Snyk Open Source detected a High Severity HTTP Request Smuggling CVE in `gunicorn 21.2.0` and a Low Severity cache issue in `Flask 3.0.2`. I upgraded `requirements.txt` to `gunicorn 23.0.0` and `Flask 3.1.3`, reducing total vulnerabilities to 0."*

### **Q3: How do you trigger live updates on the Snyk Web Dashboard from GitHub Actions?**
> *"By default, `snyk test` only outputs to CI logs. Adding `command: monitor` to `snyk/actions/python` pushes live dependency snapshots to `snyk.io` on every pipeline run."*

### **Q4: What is the difference between GitHub Secrets and Variables?**
> *"Secrets (`secrets.*`) store encrypted credentials like SSH keys (`EC2_SSH_KEY`) or API tokens (`SNYK_TOKEN`). Variables (`vars.*`) store non-sensitive configuration metadata like server IP addresses (`vars.EC2_HOST`) and usernames (`vars.EC2_USERNAME`)."*

### **Q5: How do you build a multi-stage visual pipeline in GitHub Actions?**
> *"By using job dependencies (`needs:`). Splitting the pipeline into modular jobs (`lint`, `unit_test`, `sast_scan`, `sca_scan`, `container_scan`, `prod_deploy`) causes GitHub Actions GUI to render a visual DAG graph."*

### **Q6: How do you automate Docker installation on fresh EC2 servers in CI/CD?**
> *"Inside the SSH deployment script, we added a shell check: `if ! command -v docker &> /dev/null; then sudo apt install -y docker.io ... fi`. If Docker is missing, GitHub Actions installs and enables it automatically."*

### **Q7: What is the difference between SAST and SCA?**
> *"SAST (Bandit) scans developer-written custom source code (`app.py`) for security logic flaws. SCA (Snyk) scans third-party open-source dependencies (`requirements.txt`) for published CVE vulnerabilities."*

### **Q8: What linters do you use for Java and React.js?**
> *"For Java, we use `Checkstyle` or `PMD`. For React.js and Node.js, we use `ESLint` with `eslint-plugin-react`."*

### **Q9: Why is OIDC better than GitHub Secrets for AWS/Azure credentials?**
> *"OIDC eliminates permanent access keys. It uses short-lived JWT tokens signed by GitHub's Identity Provider to request temporary 1-hour cloud IAM roles, eliminating key leakage risks."*

### **Q10: How do you enforce manual deployment approvals in GitHub Actions?**
> *"By configuring GitHub Environments (e.g. `environment: production`) with **Required Reviewers**. The deployment job pauses until a designated team member approves it in the GitHub UI."*

### **Q11: How do you prevent broken builds on feature branches from deploying?**
> *"By using job conditionals (`if: github.ref == 'refs/heads/main'`). Feature branches run unit tests and security scans, but only pushes to `main` execute the deployment job."*

### **Q12: How do you migrate pipelines from Azure DevOps to GitHub?**
> *"We use `gh-ado2gh` for repo history migration, translate `azure-pipelines.yml` to GitHub Actions YAML workflows, map ADO Variable Groups to GitHub Secrets/Variables, and replace ADO Service Connections with OIDC."*
