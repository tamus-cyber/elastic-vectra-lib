"""Test Vectra to ECS remapping"""
# pylint: disable=wrong-import-position, import-error, too-few-public-methods, no-self-use
# Import the remapping function from __init__.py
# from elastic_vectra_exporter import map_vectra_to_ecs, get_default_mapping


# class TestRemapping:
#     """ Class for testing Vectra to ECS remapping """

#     def test_remapping(self):
#         """ Test the map_vectra_to_ecs method """
#         test_detection = {
#             "id": "test_id",
#         }
#         remapped_detection = map_vectra_to_ecs(test_detection, get_default_mapping())
#         print(test_detection)
#         assert remapped_detection['event']['id'] == "test_id"  # nosec B101

# Work-in-progress