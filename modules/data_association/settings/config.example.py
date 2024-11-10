import os

# Path to the root of the project
APP_PATH_ROOT = 'your/root/project/path'

# Paths for the dataset and detection results
APP_PATH_DATA = os.path.join(APP_PATH_ROOT, 'data')
APP_PATH_REFERENCE_DATASET = os.path.join(APP_PATH_DATA, 'reference_dataset')
APP_PATH_DETECTION_RESULTS = os.path.join(APP_PATH_DATA, 'faces_detected')
APP_PATH_ASSOCIATION_OUTPUT = os.path.join(APP_PATH_DATA, 'associations')

# Similarity threshold for matching faces
APP_PARAMETER_SIMILARITY_THRESHOLD = 0.6
