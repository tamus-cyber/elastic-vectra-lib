"""Main file for Elastic-Vectra Python library."""

from elasticsearch import Elasticsearch


class ElasticVectra():
    """Elastic-Vectra Python library."""

    def __init__(self, username=None, password=None, verify_certs=True, host=None, cloud_id=None):
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
