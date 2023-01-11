"""Vectra to ECS mapping file"""
from typing import Any
from searching import search_detection


def vectra_to_ecs(vectra_detection: dict, vectra_to_ecs_map: dict) -> dict:
    """Convert a Vectra detection to an ECS document"""
    ecs_documnent = {}

    # Map the data that pulls from data in the vectra detection json
    for ecs_destination_path, vectra_source_paths in vectra_to_ecs_map['vectra'].items():
        # Vectra_source_paths can be a list or a single value. This handles both cases.
        if not isinstance(vectra_source_paths, list):
            vectra_source_paths = [vectra_source_paths]

        # Search for data in the Vectra detection json along the specified paths
        search_results = []
        for path in vectra_source_paths:
            search_results.extend(search_detection(vectra_detection, path))

        # If there is no data to add, don't add the key to the ecs_document at all
        if not search_results:
            continue

        # Many fields will only have one value. If so, unwrap it from the list.
        if len(search_results) == 1:
            search_results = search_results[0]
        
        # Add the values to the ecs_document at the specified path
        add_to_ecs_document(ecs_documnent, ecs_destination_path, search_results)

    # Map the static data
    for ecs_destination_path, value in vectra_to_ecs_map['static'].items():
        add_to_ecs_document(ecs_documnent, ecs_destination_path, value)

    return ecs_documnent


def add_to_ecs_document(ecs_document: dict, path: list | str, value: Any):
    """walk through a nested dictionary and set the value at the end of the path"""
    if isinstance(path, str):
        path = path.split('.')

    current_branch = ecs_document
    for key in path[:-1]:
        current_branch = current_branch.setdefault(key, {})

    current_branch[path[-1]] = value