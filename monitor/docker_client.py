import docker
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class DockerClient:
    def __init__(self, socket: str = "unix://var/run/docker.sock"):
        try:
            self.client = docker.DockerClient(base_url=socket)
        except Exception as e:
            logger.error(f"Failed to connect to Docker: {e}")
            self.client = None

    def list_containers(self, all: bool = True) -> List[Dict]:
        if not self.client:
            return []
        containers = self.client.containers.list(all=all)
        return [
            {
                "id": c.short_id,
                "name": c.name,
                "status": c.status,
                "image": c.image.tags[0] if c.image.tags else "unknown"
            }
            for c in containers
        ]

    def restart_container(self, container_name_or_id: str) -> bool:
        if not self.client:
            return False
        try:
            container = self.client.containers.get(container_name_or_id)
            container.restart()
            logger.info(f"Successfully restarted container: {container_name_or_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to restart {container_name_or_id}: {e}")
            return False
