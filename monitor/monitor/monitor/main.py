import time
import logging
from config import Config
from aws_client import AWSClient
from docker_client import DockerClient
from alerts import send_alert

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    cfg = Config()
    aws = AWSClient(cfg.AWS_REGION)
    docker = DockerClient(cfg.DOCKER_SOCKET)

    logger.info("Starting Cloud Infrastructure & Container Health Monitor...")
    logger.info(f"Polling every {cfg.POLL_INTERVAL_SECONDS} seconds")

    while True:
        try:
            # Check EC2 instances
            statuses = aws.get_instance_status(cfg.EC2_INSTANCE_IDS)
            for status in statuses:
                instance_id = status["InstanceId"]
                state = status["InstanceState"]["Name"]
                system_status = status["SystemStatus"]["Status"]
                instance_status = status["InstanceStatus"]["Status"]

                if state != "running" or system_status != "ok" or instance_status != "ok":
                    msg = f"EC2 Instance {instance_id} unhealthy: state={state}, system={system_status}, instance={instance_status}"
                    logger.warning(msg)
                    send_alert(cfg.ALERT_WEBHOOK_URL, msg, "critical")

                cpu = aws.get_cpu_utilization(instance_id)
                if cpu > cfg.CPU_THRESHOLD:
                    msg = f"High CPU on {instance_id}: {cpu:.1f}% (threshold {cfg.CPU_THRESHOLD}%)"
                    logger.warning(msg)
                    send_alert(cfg.ALERT_WEBHOOK_URL, msg, "warning")

            # Check Docker containers
            containers = docker.list_containers(all=True)
            for c in containers:
                if c["status"] not in ("running", "created"):
                    msg = f"Container {c['name']} ({c['id']}) is {c['status']}"
                    logger.warning(msg)
                    send_alert(cfg.ALERT_WEBHOOK_URL, msg, "critical")

                    if cfg.ENABLE_SELF_HEALING:
                        success = docker.restart_container(c["name"])
                        if success:
                            send_alert(cfg.ALERT_WEBHOOK_URL, f"Self-healed: restarted {c['name']}", "info")

        except Exception as e:
            logger.exception(f"Error in monitoring loop: {e}")

        time.sleep(cfg.POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
