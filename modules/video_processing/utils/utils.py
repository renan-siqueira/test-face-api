import os
import json


def load_config_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def ensure_directory(path):
    """Ensure that a directory exists."""
    os.makedirs(path, exist_ok=True)
