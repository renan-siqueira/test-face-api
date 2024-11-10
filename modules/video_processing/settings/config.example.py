import os

# Root path of the project
APP_PATH_ROOT = 'your/root/project/path'

# Specific paths
APP_PATH_DATA = os.path.join(APP_PATH_ROOT, 'data')
APP_PATH_INPUT_VIDEOS_PATH = os.path.join(APP_PATH_DATA, 'input_videos')
APP_PATH_FRAMES_PATH = os.path.join(APP_PATH_DATA, 'frames')

# Configuration parameters
APP_ALLOWED_EXTENSIONS = ['.mp4', '.avi', '.mov', '.webm']      # Defines the allowed extensions for processing
APP_PARAMETER_FRAME_RATE = 10                                   # Sets extraction to every 10 frames
APP_PARAMETER_USE_VIDEO_FPS = True                              # Determines if the video's FPS should be used
APP_PARAMETER_INTERVAL_IN_SECONDS = 5                           # Extracts a frame every 5 seconds (used when USE_VIDEO_FPS = True)
APP_PARAMETER_USE_FRAME_NUMBER_AS_NAME = True                   # Uses the frame number in the filename
