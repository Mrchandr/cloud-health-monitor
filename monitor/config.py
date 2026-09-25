import os
from dataclasses import dataclass, field
from typing import List

@dataclass
class Config:
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")
    EC2_INSTANCE_IDS: List[str] = field(default_factory=list)
    
    CPU_THRESHOLD: float = float(os.getenv("CPU_THRESHOLD", "80.0"))
    MEMORY_THRESHOLD: float = float(os.getenv("MEMORY_THRESHOLD", "85.0"))
    
    DOCKER_SOCKET: str = os.getenv("DOCKER_SOCKET", "unix://var/run/docker.sock")
    
    ALERT_WEBHOOK_URL: str = os.getenv("ALERT_WEBHOOK_URL", "")
    ENABLE_SELF_HEALING: bool = os.getenv("ENABLE_SELF_HEALING", "true").lower() == "true"
    
    POLL_INTERVAL_SECONDS: int = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))

    def __post_init__(self):
        env_ids = os.getenv("EC2_INSTANCE_IDS", "")
        if env_ids:
            self.EC2_INSTANCE_IDS = [i.strip() for i in env_ids.split(",") if i.strip()]
