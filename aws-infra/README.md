# 🚀 Deploy ECS App with New Relic using Terraform

This Terraform configuration provisions the following on AWS:
- ECR repository to store the Docker image
- Docker build and push process
- ECS Task Definition integrated with **New Relic APM**

---

## ⚙️ How to Use

### 1️⃣ Initialize Terraform
```bash
terraform init
```

### 2️⃣ Plan with Variables File
```bash
terraform plan -var-file="newrelic.tfvars"
```

### 3️⃣ Apply Configuration
```bash
terraform apply -var-file="newrelic.tfvars" -auto-approve
```

---

## 🧩 Example `newrelic.tfvars`
```hcl
newrelic_license_key = "YOUR_NEW_RELIC_LICENSE_KEY"
project_name         = "my-demo-app"
region               = "ap-south-1"
image_tag_mutability = "MUTABLE"
scan_on_push         = true
```

---

## 🧹 Cleanup
To destroy all created resources:
```bash
terraform destroy -var-file="newrelic.tfvars" -auto-approve
```

---

✅ **This will:**
- Create an **ECR repository**
- Build and push a Docker image from `../demo-app`
- Create necessary **IAM roles and policies**
- Register an **ECS Task Definition** with New Relic APM environment variables

---

**Author:** New Reli Demo  
**Purpose:** ECS + New Relic Integration using Terraform
