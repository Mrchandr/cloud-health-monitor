import boto3
from botocore.exceptions import ClientError
from typing import Dict, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AWSClient:
    def __init__(self, region: str):
        self.ec2 = boto3.client("ec2", region_name=region)
        self.cloudwatch = boto3.client("cloudwatch", region_name=region)

    def get_instance_status(self, instance_ids: List[str]) -> List[Dict]:
        if not instance_ids or instance_ids == [""]:
            return []
        try:
            response = self.ec2.describe_instance_status(
                InstanceIds=instance_ids,
                IncludeAllInstances=True
            )
            return response.get("InstanceStatuses", [])
        except ClientError as e:
            logger.error(f"Error fetching EC2 status: {e}")
            return []

    def get_cpu_utilization(self, instance_id: str) -> float:
        try:
            response = self.cloudwatch.get_metric_statistics(
                Namespace="AWS/EC2",
                MetricName="CPUUtilization",
                Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
                StartTime=datetime.utcnow() - timedelta(minutes=5),
                EndTime=datetime.utcnow(),
                Period=300,
                Statistics=["Average"]
            )
            datapoints = response.get("Datapoints", [])
            if datapoints:
                return datapoints[0]["Average"]
            return 0.0
        except ClientError as e:
            logger.error(f"Error fetching CPU metric: {e}")
            return 0.0
