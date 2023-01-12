"""Main file for Elastic-Vectra Python library."""

from elasticsearch import Elasticsearch
from .mapping import map_vectra_to_ecs, get_default_mapping


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
        self.mapping = get_default_mapping()

    def get_info(self):
        """Get Elastic info."""
        return self.client.info()

    def send_detection(self, detection: dict, index: str, pipeline: str = None, mapped: bool = True, extra_fields: dict = None):
        """Send a detection to Elastic.

        Args:
            detection (dict): Vectra detection to send to Elastic
            index (str): Index to send detection to
            pipeline (str): Pipeline to use (optional)
            mapped (bool): If True, map the detection before sending. Otherwise, send as-is.
        """
        # If mapped is True, map the detection
        if mapped:
            detection = map_vectra_to_ecs(detection, self.mapping)
        self.client.index(index=index, document=detection, pipeline=pipeline)
