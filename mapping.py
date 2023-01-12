"""Vectra to ECS mapping file"""
from typing import Any
from searching import search_detection


def map_vectra_to_ecs(vectra_detection, mapping):
    ecs_document = {}

    # Iterate over each mapping_item in the mapping
    for map_item in mapping:

        # if the mapping_item is static, we don't need to search for it just add the value to the ecs_document
        if map_item['is_static']:
            # for static values, the source_field is the value to add
            static_value = map_item['source_field']
            formatted_static_value = format_data(static_value, map_item['format_action'])
            add_to_ecs_document(ecs_document, map_item['destination_field'], formatted_static_value)

        # search for the data
        search_results = search_detection(vectra_detection, map_item['source_field'])

        # if there is no data to add, skip this mapping_item
        if not search_results:
            continue

        # format the data as needed
        formatted_results = format_data(search_results, map_item['format_action'])

        # add the data to the ecs_document
        add_to_ecs_document(ecs_document, map_item['destination_field'], formatted_results)

    return ecs_document


def add_to_ecs_document(ecs_document: dict, path: str | list, data_points: Any | list, force_array: bool = False):

    # handle the case where the path is a string in dot notation
    if isinstance(path, str):
        path = path.split('.')
    # handle the case where the data_points is a single value
    if not isinstance(data_points, list):
        data_points = [data_points]

    # walk through the path to the leaf
    current_branch = ecs_document
    for key in path[:-1]:
        current_branch = current_branch.setdefault(key, {})
    # grab the leaf, or make in an empty list if it doesn't exist yet
    leaf = current_branch.setdefault(path[-1], [])

    # the leaf already existed as a single value convert it to a list
    if not isinstance(leaf, list):
        leaf = [leaf]
    # add the data_points to the leaf
    leaf.extend(data_points)
    # if the leaf has only one value (and force_array is False), unwrap it
    if not force_array and len(leaf) == 1:
        leaf = leaf[0]

    # set the leaf to the ecs_document
    current_branch[path[-1]] = leaf



def format_data(data_points, format_action: str):
    """Format the data_points according to the format_action
    
    The formatting here is just so that the JSON we send to Elastic plays nice
    with the data it expects. Elastic will still be interpreting data types on it's end.

    The point of this function is to double check that the data we found in Vectra is
    able to be validly interpreted by Elastic.

    Parameters:
        data (Any): the data to be formatted. Can be a single value or a list of values
        format_action (str): the action to perform on the data
            'to_integer', 'to_string', 'to_boolean': ensure the data to the specified type, if it is not already
            'to_array': forces the output to be a list
                (normally, if there is only one value, it will be returned as a single value)
            'parse_timestamp': convert the data to a timestamp

    Returns:
        (Any): the formatted data
    """
    # if there is no format_action, return the data_points as is
    if not format_action:
        return data_points

    # force data_points to be a list so that we can iterate over it
    if not isinstance(data_points, list):
        data_points = [data_points]

    if format_action == 'to_integer':
        data_points = [int(data_point) for data_point in data_points]
    elif format_action in ('to_string', 'parse_timestamp'):
        data_points = [str(data_point) for data_point in data_points]
    elif format_action == 'to_boolean':
        data_points = [bool(data_point) for data_point in data_points]
    
    if format_action != 'to_array' and len(data_points) == 1:
        data_points = data_points[0]
