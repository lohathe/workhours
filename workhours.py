#!/bin/env python3
from core import activity
from core import common
from core import export
from core import remote
from core import setup
from core import stats
from core import taskslist
import argparse
import datetime
import sys


def addStatsParser(subparsers):
    parser = subparsers.add_parser("stats", description="Some statistics")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--days", type=int, default=None, help="Group activities by days")
    group.add_argument("-w", "--weeks", type=int, default=None, help="Group activities by weeks")
    group.add_argument("-m", "--months", type=int, default=None, help="Group activities by months")
    parser.add_argument("-g", "--graph", action="store_true", default=False, help="Use graph to show results")
    parser.add_argument("START", type=str, nargs="?", default=None, help="Starting date. Format dd/mm/yy")
    parser.add_argument("END", type=str, nargs="?", default=None, help="End date. Format dd/mm/yy")


def addExportParser(subparsers):
    parser = subparsers.add_parser("export", description="Export deatils of history")
    parser.add_argument("START", type=str, nargs="?", default=None, help="Starting date. Format dd/mm/yy")
    parser.add_argument("END", type=str, nargs="?", default=None, help="End date. Format dd/mm/yy")


def addRemoteParser(subparsers):
    parser = subparsers.add_parser("remote", description="Remote operations")
    parser.add_argument("-p", "--push", action="store_true", help="Push to remote location txt file")


def addActivityParser(subparsers):
    parser = subparsers.add_parser("activity", description="Manage activity")
    parser.add_argument("-l", "--list", action="store_true", help="List all current known activities")
    parser.add_argument("-u", "--update", action="store_true", help="Manually edit the known activities")


def addSetupParser(subparsers):
    parser = subparsers.add_parser("setup", description="Manage installation of 'WorkHours'")
    parser.add_argument("-i", "--info", action="store_true", help="Show current configurations")


def addHistoryParser(subparsers):
    parser = subparsers.add_parser("history", description="Manage history/tasks-list file")
    parser.add_argument("-u", "--update", action="store_true", help="Manually edit the history/tasts-list file")


def parseArguments():
    parser = argparse.ArgumentParser(description="WorkHours...utility overlay on a simple txt file!\n")
    subparsers = parser.add_subparsers(dest="command", required=True)
    addStatsParser(subparsers)
    addExportParser(subparsers)
    addRemoteParser(subparsers)
    addActivityParser(subparsers)
    addHistoryParser(subparsers)
    addSetupParser(subparsers)
    return parser.parse_args()


def todayDate():
    today = datetime.datetime.today()
    return f"{today.day}/{today.month}/{today.year}"


def main():
    args = parseArguments()

    if args.command == "stats":
        current_year = datetime.datetime.today().year
        start_date = common.parseDate(args.START or todayDate(), default_year=current_year)
        end_date = common.parseDate(args.END, default_year=current_year) if args.END else None
        group_by = ("d", 1)
        if args.days:
            group_by = ("d", args.days)
        elif args.weeks:
            group_by = ("w", args.weeks)
        elif args.months:
            group_by = ("m", args.months)

        if args.graph:
            return stats.graph(start_date, end_date, None, group_by)
        else:
            return stats.aggregated(start_date, end_date, None, group_by)

    if args.command == "export":
        current_year = datetime.datetime.today().year
        start_date = common.parseDate(args.START or todayDate(), default_year=current_year)
        end_date = common.parseDate(args.END, default_year=current_year) if args.END else None
        return export.list(start_date, end_date)

    if args.command == "remote":
        if args.push:
            return remote.push()

    if args.command == "activity":
        if args.list:
            return activity.list()
        if args.update:
            return activity.edit()

    if args.command == "history":
        if args.update:
            return taskslist.edit()

    if args.command == "setup":
        if args.info:
            return setup.info()
        else:
            return setup.install()


if __name__ == "__main__":
    sys.exit(main())
