#!/bin/bash
set -e

echo "Installing Cloud Health Monitor..."

sudo mkdir -p /opt/cloud-health-monitor
sudo cp -r monitor/ /opt/cloud-health-monitor/
sudo cp requirements.txt /opt/cloud-health-monitor/
sudo pip3 install -r /opt/cloud-health-monitor/requirements.txt

sudo cp systemd/health-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable health-monitor
sudo systemctl start health-monitor

echo "Monitor installed and started as systemd service."
echo "Check status: sudo systemctl status health-monitor"
