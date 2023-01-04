"""Main file for Elastic-Vectra Python library."""

import os
import json
from elasticsearch import Elasticsearch


class ElasticVectra():
    """Elastic-Vectra Python library."""

    # Set the class variables
    # Read in the mapping file
    mapping_file = os.path.join(os.path.dirname(__file__), 'mapping.json')
    with open(mapping_file, encoding='utf-8') as f:
        VECTRA_TO_ECS_MAPPING = json.load(f)

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

    # Create a new detection with ECS keys
    ecs_detection = {}

    # Map the keys
    for key, value in detection.items():
        ecs_detection[ElasticVectra.VECTRA_TO_ECS_MAPPING.get(key, key)] = value

    return ecs_detection
