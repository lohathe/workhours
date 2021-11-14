from . import common
import json
import subprocess


def edit():
    editor = common.getConfig("default_editor")
    if editor is None:
        raise Exception("Editor not configured. Aborting.")
    proc = subprocess.run([editor, str(common.ACTIVITIES_FILE)])
    return proc.returncode


def get():
    if not common.ACTIVITIES_FILE.exists():
        raise Exception("Activity file non found. Aborting.")
    with open(common.ACTIVITIES_FILE, "r") as f:
        data = json.load(f)
    return data


def list():
    data = get()
    for acronym in data.keys():
        name = data[acronym]["name"]
        descr = data[acronym]["descr"]
        print(f"* [{acronym}] {name} > {descr}")
    return 0
