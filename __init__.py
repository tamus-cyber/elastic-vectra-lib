"""Main file for Elastic-Vectra Python library."""

from elasticsearch import Elasticsearch
from .mapping import _map_vectra_keys_to_ecs


class ElasticVectra():
    """Elastic-Vectra Python library."""

    def __init__(self, username=None, password=None, verify_certs=True, host=None, cloud_id=None):  # pylint: disable=too-many-arguments
        """Initialize Elastic-Vectra Python library."""

        self.host = host
        self.cloud_id = cloud_id
        self.username = username
        self.password = password
        # If cloud_id is set, use it
        if cloud_id:
            self.client = Elasticsearch(
                http_auth=(self.username, self.password),
                cloud_id=cloud_id
            )
        # Otherwise, use host
        else:
            self.client = Elasticsearch(
                basic_auth=(self.username, self.password),
                verify_certs=verify_certs,
                hosts=[self.host]
            )

    def get_info(self):
        """Get Elastic info."""
        return self.client.info()

    def send_detection(self, detection: dict, index: str, pipeline: str):
        """Send a detection to Elastic."""
        self.client.index(index=index, document=detection, pipeline=pipeline)

    def send_detections(self, detections: list, index: str, pipeline: str):
        """Send a list of detections to Elastic."""
        for detection in detections:
            self.send_detection(detection, index, pipeline)

def map_vectra_keys_to_ecs(detection: dict) -> dict:
    """Map Vectra keys to ECS keys.

    Args:
        detection (dict): Converts the keys of a Vectra detection to ECS keys.

    Returns:
        dict: A detection with ECS keys.
    """

    return _map_vectra_keys_to_ecs(detection)
