#!/bin/env python3
from core import activity
from core import common
from core import remote
from core import stats
import argparse
import datetime
import sys


def addStatsParser(subparsers):
    parser = subparsers.add_parser("stats", description="Some statistics")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--days", type=int, default=None, help="Group activities by days")
    group.add_argument("-w", "--weeks", type=int, default=None, help="Group activities by weeks")
    group.add_argument("-m", "--months", type=int, default=None, help="Group activities by months")
    parser.add_argument("START", type=str, nargs="?", default=None, help="Starting date. Format dd/mm/yy")
    parser.add_argument("END", type=str, nargs="?", default=None, help="End date. Format dd/mm/yy")


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


def main():
    args = parseArguments()

    if args.command == "stats":
        today = datetime.datetime.today()
        unparsed_start_date = args.START or f"{today.day}/{today.month}/{today.year}"
        start_date = common.parseDate(unparsed_start_date)
        end_date = common.parseDate(args.END) if args.END else None
        group_by = ("d", 1)
        if args.days:
            group_by = ("d", args.days)
        elif args.weeks:
            group_by = ("w", args.weeks)
        elif args.months:
            group_by = ("m", args.months)
        return stats.aggregated(start_date, end_date, None, group_by)
    if args.command == "remote":
        if args.push:
            return remote.push()
    if args.command == "activity":
        if args.list:
            return activity.list()
        if args.update:
            return activity.edit()


if __name__ == "__main__":
    sys.exit(main())
