from pathlib import Path
import json


CONFIG_FOLDER = Path.home() / ".config" / "workhours"

CONFIG_FILE = CONFIG_FOLDER / "conf"
ACTIVITIES_FILE = CONFIG_FOLDER / "activities.json"
HISTORY_FILE = CONFIG_FOLDER / "history.txt"


def getConfig(key):
    if not CONFIG_FILE.exists():
        print(f"Config file not found or configured!")
        return None
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    if key not in data:
        print(f"Entry '{key}' not found in config file!")
        return None
    return data[key]
