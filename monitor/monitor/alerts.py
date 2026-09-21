import requests
import logging

logger = logging.getLogger(__name__)

def send_alert(webhook_url: str, message: str, severity: str = "warning"):
    if not webhook_url:
        logger.warning(f"No webhook configured. Alert: [{severity}] {message}")
        return

    payload = {
        "text": f"*[{severity.upper()}]* {message}"
    }
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Alert sent successfully")
    except Exception as e:
        logger.error(f"Failed to send alert: {e}")
