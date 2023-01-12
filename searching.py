from typing import Any

def search_detection(tree: dict | list, path: list | str) -> list:
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
        """Main logic of search_detection
        This recursive subfunction will walk through the tree, one node at a time
        
        Parameters:
            tree_ (list | dict): stores where we are in the structure as an object reference
            path_ (list): stores the path to search along as a list of keys
        """
        # if we are at a list, branch out and search each item in the list
        if isinstance(tree_, list):
            for branch in tree_:
                yield from search_detection(branch, path_)

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
                yield from search_detection(tree_[current_path_key], remaining_path)

    # get a list of the search results, filter undesired values
    results = [result for result in recursive_search(tree, path) if result not in (None, [], {}, '')]

    # attempt to remove duplicates
    try:
        results = list(set(results))
    except TypeError:
        # a TypeError means that the leaf contains unhashable types, so we can't deduplicate. Return the results as is
        pass

    return results
