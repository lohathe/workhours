#!/bin/env python3

from pathlib import Path
import sys
import os
import json
import shutil


def main():
    print("Installing 'WorkHours'")

    config_folder = Path.home() / ".config" / "workhours"
    config_file = config_folder / "conf"

    if not config_folder.exists():
        print(f"Creating config folder '{config_folder}'")
        config_folder.mkdir(parents=True)

        if shutil.which("rsync") is None:
            print("Cannot find 'rsync': backup on remote server will probably fail")
        else:
            print("'rsync' available: expecting private keys up-to-date")
        data = {}
        data["remote_folder"] = input("Backup folder where to store the history: ")
        data["default_editor"] = input("The editor to use to modify the history: ")
        with open(config_file, "w") as f:
            json.dump(data, f)
    else:
        print(f"Config folder '{config_folder}' already exists.")
        with open(config_file, "r") as f:
            data = json.load(f)
        if "remote_folder" not in data:
            print("No remote folder found in config file. Main program may not work correctly.")
        else:
            print(f"Remote folder: {data['remote_folder']}")

        if "default_editor" not in data:
            print("No default editor found in config file. Main program may not work correctly.")
        else:
            print(f"Default editor: {data['default_editor']}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

