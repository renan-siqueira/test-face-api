import argparse

from settings import config
from utils import utils
from modules import data_association_module


def load_config_from_py():
    """Load configuration from config.py"""
    try:
        config_dict = {
            "reference_dataset_path": getattr(config, "APP_PATH_REFERENCE_DATASET", None),
            "detection_results_path": getattr(config, "APP_PATH_DETECTION_RESULTS", None),
            "association_output_path": getattr(config, "APP_PATH_ASSOCIATION_OUTPUT", None),
            "similarity_threshold": getattr(config, "APP_PARAMETER_SIMILARITY_THRESHOLD", 0.6)
        }
        if None in config_dict.values():
            missing_keys = [k for k, v in config_dict.items() if v is None]
            raise ValueError(f"Missing keys in config.py: {', '.join(missing_keys)}")
        return config_dict
    except ImportError:
        raise ImportError("Could not import config.py. Please ensure it exists in the settings directory.")


def load_config(json_path=None):
    """Load configuration from JSON or config.py as fallback."""
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
    """Main function to orchestrate the data association process."""
    params = load_config(json_path)
    utils_functions = {
        'ensure_directory': utils.ensure_directory,
        'format_path_for_json': utils.format_path_for_json
    }

    # Call the orchestrator function in data_association_module.py
    data_association_module.orchestrate_data_association(params, utils_functions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orchestrator for data association module.")
    parser.add_argument("--json-path", help="Path to the JSON config file.")
    args = parser.parse_args()
    main(args.json_path)
