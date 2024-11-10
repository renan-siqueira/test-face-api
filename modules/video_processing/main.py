import argparse

from settings import config
from utils import utils
from modules import video_processing_module


def load_config_from_py():
    try:
        config_dict = {
            "input_videos_path": getattr(config, "APP_PATH_INPUT_VIDEOS_PATH", None),
            "frames_path": getattr(config, "APP_PATH_FRAMES_PATH", None),
            "frame_rate": getattr(config, "APP_PARAMETER_FRAME_RATE", None),
            "use_video_fps": getattr(config, "APP_PARAMETER_USE_VIDEO_FPS", None),
            "interval_in_seconds": getattr(config, "APP_PARAMETER_INTERVAL_IN_SECONDS", None),
            "use_frame_number_as_name": getattr(config, "APP_PARAMETER_USE_FRAME_NUMBER_AS_NAME", None),
            "allowed_extensions": getattr(config, "APP_ALLOWED_EXTENSIONS", None)
        }
        if None in config_dict.values():
            missing_keys = [k for k, v in config_dict.items() if v is None]
            raise ValueError(f"Missing keys in config.py: {', '.join(missing_keys)}")
        return config_dict
    except ImportError:
        raise ImportError("Could not import config.py. Please ensure it exists in the settings directory.")


def load_config(json_path=None):
    if json_path:
        try:
            return utils.load_config_from_json(json_path)
        except FileNotFoundError:
            print(f"JSON config file not found: {json_path}. Trying to load from config.py...")
    try:
        return load_config_from_py()
    except (ImportError, ValueError) as e:
        print(f"Error loading configuration: {e}")
        print("Please provide a valid JSON path or configure the settings in config.py.")
        exit(1)


def main(json_path=None):
    params = load_config(json_path)
    utils_functions = {
        'ensure_directory': utils.ensure_directory
    }
    video_processing_module.process_videos(params, utils=utils_functions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orchestrator for video processing module.")
    parser.add_argument("--json-path", help="Path to the JSON config file.")
    args = parser.parse_args()
    main(args.json_path)
