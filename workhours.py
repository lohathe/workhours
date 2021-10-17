#!/bin/env python3
from pathlib import Path
import argparse
import datetime
import json
import subprocess
import sys
import tarfile
import tempfile


CONFIG_FOLDER = Path.home() / ".config" / "workhours"


def getConfig(key):
    file = CONFIG_FOLDER / "conf"
    if not file.exists():
        print(f"Config file not found or configured!")
        return None
    with open(file, "r") as f:
        data = json.load(f)
    if key not in data:
        print(f"Entry '{key}' not found in config file!")
        return None
    return data[key]


def addStatsParser(subparsers):
    parser = subparsers.add_parser("stats", description="Some statistics")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--days", type=int, help="Group activities by days")
    group.add_argument("-w", "--weeks", type=int, help="Group activities by weeks")
    group.add_argument("-m", "--months", type=int, help="Group activities by months")
    parser.add_argument("START", type=str, nargs="?", help="Starting date. Format dd/mm/yy")
    parser.add_argument("END", type=str, nargs="?", help="End date. Format dd/mm/yy")


def addRemoteParser(subparsers):
    parser = subparsers.add_parser("remote", description="Remote operations")
    parser.add_argument("-p", "--push", action="store_true", help="Push to remote location txt file")


def addActivityParser(subparsers):
    parser = subparsers.add_parser("activity", description="Manage activity")
    parser.add_argument("-l", "--list", action="store_true", help="List all current known activities")
    parser.add_argument("-u", "--update", action="store_true", help="Manually edit the known activities")


def parseArguments():
    parser = argparse.ArgumentParser(description="WorkHours...utility overlay on a simple txt file!\n")
    subparsers = parser.add_subparsers(dest="command", required=True)
    addStatsParser(subparsers)
    addRemoteParser(subparsers)
    addActivityParser(subparsers)
    return parser.parse_args()


def editActivities():
    activity_file = CONFIG_FOLDER / "activities.json"
    editor = getConfig("default_editor")
    if editor is None:
        return 1
    return subprocess.run([editor, str(activity_file)])


def listActivities():
    activity_file = CONFIG_FOLDER / "activities.json"
    if not activity_file.exists():
        print("Activity file non found or configured.")
        return 1
    with open(activity_file, "r") as f:
        data = json.load(f)
    for acronym in data.keys():
        name = data[acronym]["name"]
        descr = data[acronym]["descr"]
        print(f"* [{acronym}] {name} > {descr}")
    return 0


def doStats(args):
    pass


def remotePush():
    remote = getConfig("remote_folder")
    if remote is None:
        print("No remote folder configured. Aborting.")
        return 1
    files_to_archive = []
    file = CONFIG_FOLDER / "hours.txt"
    if not file.exists():
        print("No file containing data has been found. Aborting.")
        return 1
    else:
        files_to_archive.append(file)
    file = CONFIG_FOLDER / "activities.json"
    if not file.exists():
        print("WARNING: No activity file has been found: not archiving it!")
    else:
        files_to_archive.append(file)

    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    target_name = f"{remote}/archived_{year:04d}{month:02d}{day:02d}.tgz"
    with tempfile.NamedTemporaryFile() as f:
        archive = tarfile.open(f.name, "w:gz")
        for file in files_to_archive:
            archive.add(file)
        archive.close()
        cli = ["rsync", "-a", "-z", "-P", f.name, target_name]
        print(">> {}".format(" ".join(cli)))
        proc = subprocess.run(cli)
        return proc.returncode
    return 0


def main():
    args = parseArguments()

    if args.command == "stats":
        return doStats(args)
    if args.command == "remote":
        if args.push:
            return remotePush()
    if args.command == "activity":
        if args.list:
            return listActivities()
        if args.update:
            return editActivities()


if __name__ == "__main__":
    sys.exit(main())
