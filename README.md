# Automated Cloud Infrastructure & Container Health Monitor

Lightweight Python tool that continuously monitors AWS EC2 instance health, CPU usage (via CloudWatch), and Docker containers. It can automatically restart stopped containers and send alerts.

## Features

- Monitors EC2 instance health
- Checks CPU utilization
- Monitors Docker container status
- Auto-restarts stopped containers (self-healing)
- Sends alerts (optional)

## Tech Stack

- Python
- boto3 (AWS SDK)
- Docker SDK
- AWS EC2 + CloudWatch
- systemd

## Project Structure

cloud-health-monitor/
├── monitor/
│   ├── main.py
│   ├── aws_client.py
│   ├── docker_client.py
│   ├── alerts.py
│   └── config.py
├── scripts/
│   └── install.sh
├── systemd/
│   └── health-monitor.service
├── requirements.txt
├── .gitignore
└── README.md

## How to Run Locally

```bash
pip install -r requirements.txt
cd monitor
python main.py
```
## Deploy on EC2

chmod +x scripts/install.sh
sudo ./scripts/install.sh

## Check Status:

sudo systemctl status health-monitor

##Author
Chandrasekhar Sai Durga Gummadi
DevOps & Cloud Engineer | AIML Graduate
