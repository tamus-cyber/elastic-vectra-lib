from typing import Any
import itertools as it

LIST_WILDCARD = '*'


def walk_tree(tree: dict|list):
    """Walks a dictionary and yields the path and value of each leaf node lazily
    Lazily here means it only walks through the first item of a list
    """
    def recursive_walk(tree_: dict|list|Any, path):
        """Main logic of walk_structure
        This recursive subfunction will walk through the structure, one node at a time

        Parameters:
            tree_ (list | dict): stores where we are in the structure as an object reference
            path (list): stores the path to the current as a list of keys (or list_wildcard for lists)

        Yields:
            leaf: a value in the tree that has no more data nested beneath it
            path (list): the path to the leaf
        """
        # sometimes the end of a structure is an empty list, or None
        # yield none to account for that
        if not tree_:
            yield None, path

        # if we are at a dict, walk through each value in the dict
        if isinstance(tree_, dict):
            for key, branch in tree_.items():
                yield from recursive_walk(branch, path + [key])

        # if we are at a list, walk through each item in the list
        elif isinstance(tree_, list):
            for branch in tree_:
                yield from recursive_walk(branch, path + [LIST_WILDCARD])

        else:
            # if we get here, we've reached a leaf node
            yield tree_, path

    yield from recursive_walk(tree, [])


def search_along_path(tree: dict | list, path: list | str) -> list:
    """Walk through a nested dict/list structure based on the given path,
    branching out at lists when it detects them, and return a list of results 
    that match the given path. 
    
    Filter out values that are None, empty lists, empty dicts or empty strings.
    
    Parameters:
        tree (dict | list): a nested structure of dictionaries and lists
        path (list | str): list of keys (or string in dot notation) to follow when walking through the structure
        
    Returns:
        (list): the value at the end of the path, or None if the path doesn't exist
    """
    if isinstance(path, str):
        path = path.split('.')

    def recursive_search(tree_: dict | list | Any, path_: list):
        """Main logic of search_along_path
        This recursive subfunction will walk through the tree, one node at a time
        
        Parameters:
            tree_ (list | dict): stores where we are in the structure as an object reference
            path_ (list): stores the path to search along as a list of keys
        """
        # if we are at a list, branch out and search each item in the list
        if isinstance(tree_, list):
            for branch in tree_:
                yield from search_along_path(branch, path_)

        # if we are at the end of the path (and not a inside a list), we have found the value we are looking for
        elif not path_:
            yield tree_

        # if we are at a dict, continue searching along the path by using the leftmost key in the path
        elif isinstance(tree_, dict):
            # grab the key we need to continue searching along the path
            current_path_key = path_[0]

            # grab the remaining keys from the path to pass to the next recursive_search call
            remaining_path = path_[1:]

            # if the key is in the tree, we can continue searching along the path
            if current_path_key in tree_:
                yield from search_along_path(tree_[current_path_key], remaining_path)

    # return a list of the search results, filtering undesired values
    return [result for result in recursive_search(tree, path) if result not in (None, [], {}, '')]


def get_by_path(tree: dict, path: list | str):
    """walk through a nested dictionary and return the value at the end of the path"""
    if isinstance(path, str):
        path = path.split('.')

    current_branch = tree
    for key in path[:-1]:
        current_branch = current_branch.setdefault(key, {})

    leaf = current_branch.setdefault(path[-1], None)
    return leaf


def set_by_path(tree: dict, path: list | str, value: Any):
    """walk through a nested dictionary and set the value at the end of the path"""
    if isinstance(path, str):
        path = path.split('.')

    current_branch = tree
    for key in path[:-1]:
        current_branch = current_branch.setdefault(key, {})

    current_branch[path[-1]] = value


if __name__ == '__main__':
    pass