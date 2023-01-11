"""Vectra to ECS mapping file"""
import json
from collections import defaultdict
from tree_utils import search_along_path, set_by_path


def _map_vectra_keys_to_ecs(vectra_detection: dict, vectra_to_ecs_map: dict) -> dict:
    ecs_documnent = {}

    # Map the data that pulls from data in the vectra detection json
    for ecs_destination_path, vectra_source_paths in vectra_to_ecs_map['vectra'].items():
        # Vectra_source_paths can be a list or a single value. This handles both cases.
        if not isinstance(vectra_source_paths, list):
            vectra_source_paths = [vectra_source_paths]

        # Grab data from all the source paths and combine them into one list
        values_to_add = []
        for vectra_source_path in vectra_source_paths:
            values_to_add.extend(search_along_path(vectra_detection, vectra_source_path))

        # If there is no data to add, don't add the key to the ecs_document at all
        if not values_to_add:
            continue

        # If there is only one value, don't wrap it in a list
        if len(values_to_add) == 1:
            values_to_add = values_to_add[0]
        
        # Add the values to the ecs_document at the specified path
        set_by_path(ecs_documnent, ecs_destination_path, values_to_add)

    # Map the static data
    for ecs_destination_path, value in vectra_to_ecs_map['static'].items():
        set_by_path(ecs_documnent, ecs_destination_path, value)

    return ecs_documnent
