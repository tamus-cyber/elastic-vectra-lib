"""Vectra to ECS mapping file"""
import os
import ipaddress
from csv import DictReader
from typing import Any
from searching import search_detection

from loguru import logger
logger.disable(__name__)


def get_default_mapping():
    """Returns the default mapping from the mapping.csv file"""
    MAPPING_FILENAME = 'ecs_mapping.csv'
    parent_filepath = os.path.dirname(__file__)
    path_to_mapping = os.path.join(parent_filepath, MAPPING_FILENAME)
    with open(path_to_mapping, 'r') as file:
        return list(DictReader(file))


def map_vectra_to_ecs(vectra_detection: dict, mapping: list[dict[str, str]]):
    ecs_document = {}

    for map_item in mapping:
        # if the mapping_item is static, then the "source_field" is actually static value to add to every document that uses this mapping
        if map_item['is_static'].lower() == 'true':
            # for static values, the source_field is the value to add
            source_data = map_item['source_field']
        else:
            source_data = search_detection(vectra_detection, map_item['source_field'])

        if not source_data:
            continue

        # format the data as specified by the mapping
        formatted_data = format_data(source_data, map_item['format_action'], strict = False)
        # if the destination_field is not specified, default to keeping the same path as the source
        destination_field: str = map_item['destination_field'] if map_item['destination_field'] != '' else map_item['source_field']
        add_to_ecs_document(ecs_document, destination_field, formatted_data)

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

    # deduplicate items in the leaf if possible
    try:
        leaf = list(set(leaf))
    except TypeError:
        # a TypeError means that the leaf contains unhashable types, so we can't deduplicate
        pass

    # if the leaf has only one value (and force_array is False), unwrap it
    if not force_array and len(leaf) == 1:
        leaf = leaf[0]

    # set the leaf to the ecs_document
    current_branch[path[-1]] = leaf


def format_data(data_points, format_action: str, strict: bool = True):
    """Format the data_points according to the format_action
    
    The formatting here is just so that the JSON we send to Elastic plays nice
    with the data it expects. Elastic will still be interpreting data types on it's end.

    The point of this function is to double check that the data we found in Vectra is
    able to be validly interpreted by Elastic.

    Parameters:
        data (Any): The data to be formatted. Can be a single value or a list of values
        format_action (str): The action to perform on the data
            'to_integer', 'to_string', 'to_boolean': attempt to cast the data to the specified type
            'filter_ip': drop any data that is not a valid IP address
        'strict': If True, drop any data that can not be properly casted. If False, keep any uncastable data as-is

    Returns:
        (Any): the formatted data
    """
    # if there is no format_action, return the data_points as is
    if not format_action:
        return data_points

    # force data_points to be a list so that we can iterate over it
    if not isinstance(data_points, list):
        data_points = [data_points]

    if format_action in ('to_integer', 'to_string', 'to_boolean'):
        # if the format_action is to cast the data to a type, then use the flexible_cast function
        type_ = {'to_integer': int, 'to_string': str, 'to_boolean': bool}[format_action]
        data_points = [_flexible_cast(type_, value) for value in data_points]
        data_points = [value for value in data_points if value is not None]
    
    elif format_action == 'filter_ip':
        data_points = [value for value in data_points if _is_valid_ip(value)]

    if len(data_points) == 1:
        data_points = data_points[0]

    return data_points


def _flexible_cast(type_: type, value: Any, strict: bool = True):
        """Attempts to cast the data to the specified type
        If the cast fails, returns None if strict is True, otherwise returns the data as-is
        """
        try:
            return type_(value)
        except ValueError as e:
            logger.error(f'Failed to cast {value} to {type_}: {e}')
            return None if strict else value


def _is_valid_ip(value: str):
    """Returns True if the value is a valid IP address, otherwise returns False"""
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False