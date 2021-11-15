from . import common
import datetime
import json
import shutil


def check_dependencies():
    if shutil.which("rsync") is None:
        print("Cannot find 'rsync': backup on remote server will probably fail!")
    else:
        print("'rsync' available: expecting private keys up-to-date!")

    try:
        import matplotlib.pyplot
    except ImportError:
        print("Cannot find 'matplotlib': graphs for statistics will probably fail!")


def install():
    print("Installing 'WorkHours'...")

    if common.CONFIG_FOLDER.exists():
        print("'WorkHours' seems already installed...aborting!")
        print(f"If you need to update something: everything is inside '{common.CONFIG_FOLDER}'.")
        return 1

    print(f"Creating configuration folder '{common.CONFIG_FOLDER}'")
    common.CONFIG_FOLDER.mkdir(parents=True)

    data = {}
    data["remote_folder"] = input("Backup folder in remote server where to store the history: ")
    data["default_editor"] = input("The editor to use to modify the text files: ")
    with open(common.CONFIG_FILE, "w") as f:
        json.dump(data, f)

    default_activity = {
        "wm": {
            "name": "workstation management",
            "descr": "time spent updating, installing, managing the PC.",
        }
    }
    with open(common.ACTIVITIES_FILE, "w") as f:
        json.dump(default_activity, f)
    print("Remember to update the activity file! It can be done using the 'activity' subcommand.")

    with open(common.HISTORY_FILE, "a") as f:
        today = datetime.date.today()
        f.write(f"{today.day}/{today.month}/{today.year}\n")
        f.write("00:10 - wm | workhours > installing 'WorkHours'\n")
    print("Remember to update the history file! It can be done using the 'tasklist' subcommand.")

    check_dependencies()
    print("Remember to update $PATH or create the necessary symlink to use 'WorkHours' with ease!")
    return 0


def info():
    print("==( stored configuration )==========")
    if not common.CONFIG_FOLDER.exists():
        print("'WorkHours' seems not installed yet...aborting!")
        return 1
    if not common.CONFIG_FILE.exists():
        print("'WorkHours' seems to be broken...aborting!")
        return 1

    remote_folder = common.getConfig("remote_folder")
    if remote_folder is None:
        print("No remote folder found in config file. Main program may not work correctly.")
    else:
        print(f"Remote folder for backups: '{remote_folder}'.")

    default_editor = common.getConfig("default_editor")
    if default_editor is None:
        print("No default editor found in config file. Main program may not work correctly.")
    else:
        print(f"Default editor: '{default_editor}'.")

    check_dependencies()
    return 0
