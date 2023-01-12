"""Main file for Elastic-Vectra Python library."""

from elasticsearch import Elasticsearch


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

    def send_detection(self, detection: dict, index: str, pipeline: str = None, mapped: bool = True):
        """Send a detection to Elastic.

        Args:
            detection (dict): Vectra detection to send to Elastic
            index (str): Index to send detection to
            pipeline (str): Pipeline to use (optional)
            mapped (bool): If True, map the detection before sending. Otherwise, send as-is.
        """
        # If mapped is True, use the mapped index
        if mapped:
            # TODO: Import mapping function and map
            pass
        self.client.index(index=index, document=detection, pipeline=pipeline)
