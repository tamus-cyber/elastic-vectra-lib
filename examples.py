import json
import time
from rich import print
from searching import search_detection
from parse_sample import get_sample_detections
from mapping import vectra_to_ecs

def _get_ecs_map():
    with open('ecs_mapping.json', 'r') as f:
        return json.load(f)

def search_path_example():
    detections = get_sample_detections()

    search_results = []

    search_path = 'grouped_details.normal_account_behavior.service_name'

    tic = time.perf_counter()
    for detection in detections:
        search_results.append(search_detection(detection, search_path))
    toc = time.perf_counter()

    print(search_results)
    print(f'Searched {len(detections)} detections in {toc - tic:0.6f} seconds')

def vectra_to_ecs_example():
    # detection = get_sample_detections()[3]

    with open('detection_files/108677.json', 'r') as f:
        detection = json.load(f)

    ecs_map = _get_ecs_map()

    ecs_document = vectra_to_ecs(detection, ecs_map)
    print(ecs_document)


if __name__ == '__main__':
    # search_path_example()
    vectra_to_ecs_example()