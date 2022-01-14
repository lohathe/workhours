"""
The whole scripts are build around the "history file".
This history file has a specific format that must be followed.
Since it records tasks performed on specific days, there are 2 kinds of
lines:

 1. Date references
 2. Task entries

All tasks entries inherits the first date reference that precedes it.

Date reference
----------------
A date reference must follow the format 'DD/MM/YYYY'.
For the sake of faster writing, it is possible to omit the year reference using
the shorter format 'DD/MM'. In this case the year reference gets inherited by
any previously fully-defined date reference.

Task entries
----------------
A task entry should represent a short log of a task performed on a specific
day. This short log should contain at least 2 kind of information: the duration
and the kind of activity performed. It is then possible to further detail
what happened by specifying a "reference project" and a free description.
The "kind of activity" written inside the task entry should be the shortcut
written inside the dedicated "activity configuration file".
Note that the actual meaning of the items composing a task entry is very user
specific. The task entry is designed to be easy and fast to write or modify
inside the text file, and its expected format is there just to be able to
automate the extraction of some statistics. Aka: the format of a task entry
has been designed to be simple, light-weight but expressive enough to produce
automatic groups or hierarchies.

The format is:
<duration> '-' <activity type> '|' <project> '>' <free description>

Example:
01:30 - d | WorkHours > add code to perform statistics

"""
from . import common
import datetime
import re
import subprocess
import warnings


class TaskEntry(object):
    def __init__(self, date, line):
        self.date = date
        self.line = line
        self.duration = 0
        self.activity_type = ""
        self.project = ""
        self.content = ""

        matcher = re.compile("^([^-]*)-([^|]*)\|([^>]*)(.*)$")
        m = matcher.match(line)
        if not m:
            warnings.warn(f"problem parsing line '{line}' @ {date}")
        else:
            item = m.group(1).strip()
            if len(item) < 5:
                warnings.warn(f"bad duration for '{line}' @ {date}")
            else:
                tokens = item.split(":")
                self.duration = int(tokens[0])*60 + int(tokens[1])
            item = m.group(2).strip()
            if len(item) == 0:
                warnings.warn(f"bad activity_type for '{line}' @ {date}")
            else:
                self.activity_type = item
            item = m.group(3).strip() if m.group(3) else ""
            if len(item) == 0:
                warnings.warn(f"bad project for '{line}' @ {date}")
            else:
                self.project = item
            self.content = m.group(4).strip() if m.group(4) else ""


def get():
    res = []
    with open(common.HISTORY_FILE, "r") as f:
        current_year = 1970
        current_date = datetime.date(current_year, 1, 1)
        for line in f:
            line = line.strip()
            if not line or line[0] == '#':
                continue
            date = common.parseDate(line, default_year=current_year)
            if date:
                current_date = date
                # we are lazy in writing the year in each entry. However
                # sometimes (it should be once every year :P) we have to write
                # an entry specifying the correct year...from that point onward
                # all subsequent dates should have a different default year!
                current_year = date.year
                continue
            res.append(TaskEntry(current_date, line))
    return res


def edit():
    editor = common.getConfig("default_editor")
    if editor is None:
        raise Exception("Editor not configured. Aborting.")
    proc = subprocess.run([editor, str(common.HISTORY_FILE)])
    return proc.returncode
