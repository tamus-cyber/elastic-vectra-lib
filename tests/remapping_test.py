"""Test Vectra to ECS remapping"""
# pylint: disable=wrong-import-position, import-error, too-few-public-methods, no-self-use
# Import the remapping function from __init__.py
from .. import map_vectra_keys_to_ecs


class TestRemapping:
    """ Class for testing Vectra to ECS remapping """

    def test_remapping(self):
        """ Test the map_vectra_keys_to_ecs method """
        test_detection = {
            "id": "test_id",
        }
        remapped_detection = map_vectra_keys_to_ecs(test_detection)
        assert remapped_detection['event']['id'] == "test_id"  # nosec B101
