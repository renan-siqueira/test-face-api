import argparse
from settings import config
from utils import utils
from modules import face_detection_module


def load_config_from_py():
    try:
        config_dict = {
            "frames_path": getattr(config, "APP_PATH_FRAMES", None),
            "faces_output_path": getattr(config, "APP_PATH_FACES_OUTPUT", None),
            "create_model_folder": getattr(config, "APP_PARAMETER_CREATE_MODEL_FOLDER", False),
            
            "local_detection": {
                "use_local": getattr(config, "APP_LOCAL_DETECTION", {}).get("use_local", True),
                "model": getattr(config, "APP_LOCAL_DETECTION", {}).get("model", "hog"),
                "upscale_factor": getattr(config, "APP_LOCAL_DETECTION", {}).get("upscale_factor", 1),
                "number_of_times_to_upsample": getattr(config, "APP_LOCAL_DETECTION", {}).get("number_of_times_to_upsample", 1)
            },

            "yolo_detection": {
                "use_yolo": getattr(config, "APP_YOLO_DETECTION", {}).get("use_yolo", False),
                "yolo_model_path": getattr(config, "APP_YOLO_DETECTION", {}).get("yolo_model_path", None)
            },

            "api_detection": {
                "use_api": getattr(config, "APP_API_DETECTION", {}).get("use_api", False),
                "api_service": getattr(config, "APP_API_DETECTION", {}).get("api_service", None),
                "api_credentials_path": getattr(config, "APP_API_DETECTION", {}).get("api_credentials_path", None)
            }
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
        'ensure_directory': utils.ensure_directory,
        'format_path_for_json': utils.format_path_for_json
    }
    face_detection_module.process_all_frames(params, utils=utils_functions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orchestrator for face detection module.")
    parser.add_argument("--json-path", help="Path to the JSON config file.")
    args = parser.parse_args()
    main(args.json_path)
