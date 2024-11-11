import argparse
import subprocess
import sys
import os
import json

from settings import config


def load_config_from_json(json_path):
    """Load configuration settings from a JSON file."""
    with open(json_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def activate_venv():
    """Activate the virtual environment."""
    venv_activate_script = os.path.join(config.APP_PATH_VENV, 'Scripts', 'activate.bat' if sys.platform == 'win32' else 'activate')
    command = f'"{venv_activate_script}" && echo "Virtual environment activated"'
    return command


def run_step(module_path, main_script_name, step_name):
    """Run a specific step in the pipeline within the virtual environment."""
    print(f"Starting {step_name}...")

    script_path = os.path.join(module_path, main_script_name)
    command = f"{activate_venv()} && python \"{script_path}\""
    subprocess.run(command, shell=True, check=True)
    print(f"{step_name} completed.")


def main(json_path=None):
    """Main function to orchestrate the complete video processing pipeline."""
    # Load configuration from JSON if provided
    if json_path:
        config_data = load_config_from_json(json_path)
        main_script_name = config_data.get("main_script_name", config.APP_NAME_MAIN_SCRIPT)
        script_paths = {
            "video_processing": config_data.get("video_processing_module", config.APP_PATH_SCRIPT_STEP_1),
            "face_detection": config_data.get("face_detection_module", config.APP_PATH_SCRIPT_STEP_2),
            "data_association": config_data.get("data_association_module", config.APP_PATH_SCRIPT_STEP_3),
            "report_generation": config_data.get("report_generation_module", config.APP_PATH_SCRIPT_STEP_4)
        }
    else:
        # Use default paths from the config module
        main_script_name = config.APP_NAME_MAIN_SCRIPT
        script_paths = {
            "video_processing": config.APP_PATH_SCRIPT_STEP_1,
            "face_detection": config.APP_PATH_SCRIPT_STEP_2,
            "data_association": config.APP_PATH_SCRIPT_STEP_3,
            "report_generation": config.APP_PATH_SCRIPT_STEP_4
        }

    # Passo 1 - Processamento de Vídeo
    run_step(script_paths["video_processing"], main_script_name, "Video processing")

    # Passo 2 - Detecção Facial
    run_step(script_paths["face_detection"], main_script_name, "Face detection")

    # Passo 3 - Associação de Dados
    run_step(script_paths["data_association"], main_script_name, "Data association")

    # Passo 4 - Geração de Relatórios
    run_step(script_paths["report_generation"], main_script_name, "Report generation")

    print("Pipeline complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Main orchestrator for the complete video processing pipeline."
    )
    parser.add_argument("--json-path", help="Path to the JSON config file.")
    args = parser.parse_args()
    main(args.json_path)
