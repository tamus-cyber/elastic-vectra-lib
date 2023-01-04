"""Test Vectra to ECS remapping"""
# pylint: disable=wrong-import-position, import-error, too-few-public-methods, no-self-use
# Import the remapping function from __init__.py
from .. import map_vectra_keys_to_ecs


class TestRemapping:
    """ Class for testing Vectra to ECS remapping """

    def test_remapping(self):
        """ Test the map_vectra_keys_to_ecs method """
        test_detection = {
            "unit_test_key": "unit_test_val"
        }
        remapped_detection = map_vectra_keys_to_ecs(test_detection)
        assert remapped_detection.get('unit_test_key_remapped', False)  # nosec B101
