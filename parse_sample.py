import os
import json

DIR_PATH = 'detection_files'

def get_sample_detections():
    """Grabs all the detections from the detection_files folder and returns them as a list of dicts"""
    # get all the jsons from the detection_files folder
    filepaths = [os.path.join(DIR_PATH, filename) for filename in os.listdir(DIR_PATH) if filename.endswith('.json')]
    # read the jsons into a list of dicts
    detections = []
    for filepath in filepaths:
        with open(filepath, 'r') as f:
            detections.append(json.load(f))
    return detections