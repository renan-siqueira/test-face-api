import os

APP_PATH_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

APP_PATH_VENV = os.path.join(APP_PATH_ROOT, '.venv')
APP_PATH_MODULES = os.path.join(APP_PATH_ROOT, 'modules')

APP_PATH_SCRIPT_STEP_1 = os.path.join(APP_PATH_MODULES, 'video_processing')
APP_PATH_SCRIPT_STEP_2 = os.path.join(APP_PATH_MODULES, 'face_detection')
APP_PATH_SCRIPT_STEP_3 = os.path.join(APP_PATH_MODULES, 'data_association')
APP_PATH_SCRIPT_STEP_4 = os.path.join(APP_PATH_MODULES, 'report_generation')

APP_NAME_MAIN_SCRIPT = 'main.py'
