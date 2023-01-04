"""Vectra to ECS mapping file"""
import json
from collections import defaultdict


def _nested_default_dict():
    """Dictionary that creates an empty dictionary if the key doesn't exist"""
    return defaultdict(_nested_default_dict)


def _map_vectra_keys_to_ecs(detection: dict) -> dict:
    """Map Vectra keys to ECS keys.

    Args:
        detection (dict): Converts the keys of a Vectra detection to ECS keys.

    Returns:
        dict: A detection with ECS keys.
    """
    # Initialize the mapping
    ecs_mapping = _nested_default_dict()

    # Map the keys
    ecs_mapping['event']['id'] = detection['id']

    # Convert all of the defaultdicts to dicts
    ecs_mapping = json.loads(json.dumps(ecs_mapping))

    return ecs_mapping
