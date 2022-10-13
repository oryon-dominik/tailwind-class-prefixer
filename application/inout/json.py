import logging
import json
import sys
from pathlib import Path


log = logging.getLogger("application")


def load_json_from_file(path: Path) -> dict | list:
    """
    Load a json file.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        log.error(f"FileNotFoundError: {e}")
    except json.decoder.JSONDecodeError as e:
        log.error(f"JSONDecodeError {e}")
    except PermissionError as e:
        log.error(f"PermissionError: {e}")
    sys.exit(1)


def write_json_to_file(path: Path, content: dict | list) -> dict | list:
    """
    Write content to a json file.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=4)
        return load_json_from_file(path)
    except FileNotFoundError as e:
        log.error(f"FileNotFoundError: {e}")
    except json.decoder.JSONDecodeError as e:
        log.error(f"JSONDecodeError {e}")
    except PermissionError as e:
        log.error(f"PermissionError: {e}")
    sys.exit(1)
