import os


# Path to the root of the project (adjust as necessary)
APP_PATH_ROOT = 'your/root/folder/path'

# Paths to directories
APP_PATH_MODELS = os.path.join(APP_PATH_ROOT, 'models')
APP_PATH_DATA = os.path.join(APP_PATH_ROOT, 'data')
APP_PATH_FRAMES = os.path.join(APP_PATH_DATA, 'frames')
APP_PATH_FACES_OUTPUT = os.path.join(APP_PATH_DATA, 'faces_detected')

# Parameter to create a folder with the model's name
APP_PARAMETER_CREATE_MODEL_FOLDER = True

# Face detection settings using local model
APP_LOCAL_DETECTION = {
    "use_local": False,                         # Defines if the local method will be used
    "model": "hog",                             # Detection model: 'hog' or 'cnn'
    "upscale_factor": 1,
    "number_of_times_to_upsample": 1
}

# Face detection settings using YOLOv8
APP_YOLO_DETECTION = {
    "use_yolo": False,                          # Defines if YOLOv8 will be used
    "yolo_model_path": os.path.join(            # Path to the local YOLOv8 model
        APP_PATH_MODELS,
        'yolov8-face-detection',
        'model.pt'
    )
}

# Settings for using external API
APP_API_DETECTION = {
    "use_api": False,                           # Defines if the API method will be used
    "api_service": None,                        # API service (Azure, Google Vision, AWS, etc.)
    "api_credentials_path": None                # Path to the API credentials file
}
