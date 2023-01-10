import os
import json
import tree_walking as tw
from rich import print
import time

LIST_WILDCARD = '<<LIST_WILDCARD>>'

def combine_keys(dicts: list[dict]):
    combined = {}
    for d in dicts:
        for path, value in tw.walk_tree(d):
            reference = combined
            for key in path[:-1]:
                if key not in reference or reference[key] is None:
                    reference[key] = {}
                reference = reference[key]
            if path[-1] not in reference:
                reference[path[-1]] = value
    return combined