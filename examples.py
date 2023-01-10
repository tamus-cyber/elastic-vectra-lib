import json
import time
from rich import print
from tree_walking import search_along_path
from parse_sample import get_sample_detections

def search_path_example():
    detections = get_sample_detections()

    search_results = []

    search_path = 'grouped_details.normal_account_behavior.service_name'

    tic = time.perf_counter()
    for detection in detections:
        search_results.append(search_along_path(detection, search_path))
    toc = time.perf_counter()

    print(search_results)
    print(f'Searched {len(detections)} detections in {toc - tic:0.6f} seconds')

if __name__ == '__main__':
    search_path_example()