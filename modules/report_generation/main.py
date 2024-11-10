import argparse
from settings import config
from utils import utils
from modules import report_generation_module


def load_config_from_py():
    """Load configuration from config.py"""
    try:
        config_dict = {
            "association_results_path": getattr(config, "APP_PATH_ASSOCIATION_RESULTS", None),
            "reports_output_path": getattr(config, "APP_PATH_REPORTS_OUTPUT", None),
            "csv_filename": getattr(config, "APP_REPORT_CSV_FILENAME", "detection_report.csv"),
            "json_filename": getattr(config, "APP_REPORT_JSON_FILENAME", "detection_report.json")
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
    """Main function to orchestrate the report generation process."""
    params = load_config(json_path)
    utils_functions = {
        'ensure_directory': utils.ensure_directory,
        'format_path_for_json': utils.format_path_for_json
    }

    # Call the report generation function in the module
    report_generation_module.run_report_generation(params, utils_functions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orchestrator for report generation module.")
    parser.add_argument("--json-path", help="Path to the JSON config file.")
    args = parser.parse_args()
    main(args.json_path)
