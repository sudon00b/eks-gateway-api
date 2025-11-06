# 🚀 Demo Python App on AWS ECS with New Relic Monitoring

This repository contains a demo **Python application** deployed on **AWS ECS (Elastic Container Service)** and monitored using **New Relic APM**. It demonstrates how to containerize, deploy, and monitor a simple service in a cloud-native environment.

---

## 🧩 Overview

- **Application**: Python (Flask-based) demo app  
- **Containerization**: Docker  
- **Deployment**: AWS ECS (Fargate)  
- **Monitoring**: New Relic APM integrated via the Python agent  

---

## 🏗️ Architecture

User → ECS Service → Flask App (with New Relic Agent) → New Relic Dashboard

- The app runs in a Docker container managed by ECS.  
- Metrics, logs, and traces are sent to **New Relic** for visibility and performance insights.

---

## ⚙️ Prerequisites

- AWS Account with ECS and ECR access  
- Docker installed and running  
- AWS CLI configured (`aws configure`)  
- New Relic account and **license key**  
- IAM role with ECS task execution permissions  

---

## 🔧 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/ecs-python-newrelic-demo.git
   cd ecs-python-newrelic-demo
   ```

2. **Configure New Relic**
   - Obtain your **license key** from the New Relic dashboard.  
   - Add it to your configuration file or as an environment variable in ECS.  

3. **Build and Push Docker Image**
   - Build the image locally.  
   - Tag and push it to your **AWS ECR repository**.  

4. **Deploy to ECS**
   - Register a new ECS task definition using your pushed image.  
   - Create an ECS service to run the task on Fargate or EC2.  

---

## 📈 Verify Monitoring

- Access your app through the ECS service public endpoint.  
- Open **New Relic → APM → Applications** to see your app’s metrics, transactions, and logs.  
- You’ll find details such as response times, throughput, and distributed traces.

---

## 🧰 Troubleshooting

| Issue | Cause | Resolution |
|-------|--------|-------------|
| App not visible in New Relic | Missing/invalid license key | Check your key and agent initialization |
| Task failing | Role or image issue | Verify IAM permissions and ECR image URL |
| Delayed data | New Relic agent warm-up | Wait a few minutes after traffic starts |

---

## 📚 References

- [New Relic Python Agent Docs](https://docs.newrelic.com/docs/apm/agents/python-agent/)
- [AWS ECS Developer Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)
- [Docker Documentation](https://docs.docker.com/)
- [Flask Framework](https://flask.palletsprojects.com/)

---

## 🧾 Summary

| Component | Description |
|------------|-------------|
| **Language** | Python |
| **Framework** | Flask |
| **Container** | Docker |
| **Deployment** | AWS ECS |
| **Monitoring** | New Relic APM |

---

### 💡 Author
**Maintainer:** _Sudhakar Irrinki_  
**Purpose:** Demo setup for ECS deployment and APM monitoring using New Relic.

