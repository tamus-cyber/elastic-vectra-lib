"""Main file for Elastic-Vectra Python library."""

from elasticsearch import Elasticsearch


class ElasticVectra(object):
    """Elastic-Vectra Python library."""

    def __init__(self, host, username, password, verify_certs=True):
        """Initialize Elastic-Vectra Python library."""
        self.host = host
        self.username = username
        self.password = password
        self.client = Elasticsearch(
            self.host,
            basic_auth=(self.username, self.password),
            verify_certs=verify_certs,
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
