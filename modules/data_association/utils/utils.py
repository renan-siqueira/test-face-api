import os
import json


def ensure_directory(path):
    """Ensure that a directory exists."""
    os.makedirs(path, exist_ok=True)


def load_config_from_json(json_path):
    """Load configuration from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_path_for_json(path):
    """Convert Windows-style paths to Unix-style paths for JSON compatibility."""
    return path.replace("\\", "/")
