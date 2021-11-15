# WORK HOURS

Simple program to annotate how work hours are spent.

Main abilities:
 1. perform statistics
 2. archive and remote storage

It stores the interim data inside a standard configuration folder. Inside this
folder there are 3 important files:

 - `config.json` -> the file storing the configuration of the program, like the
    default editor to use to modify the files, the URL for the remote backup, etc
 - `activities.json` -> a simple json database storing the "macro activities"
    performed. The main goal for this database is to group everyday tasks based
    on the kind of work done: it should help focusing which activity is more
    time-hungry (e.g., the activity "meetings" which is valid for different
    projects but identifies a generic task)
 - `history.txt` -> the main database, where each performed task should be
    annotated. The more details in here, the more useful the statics will
    become and the more insight one can get from its own work pattern


## Requirements

 * python 3.8 (could work with lower versions, not tested)
 * `rsync` executable reachable through `$PATH`. Used to perform remote backup
 * the `matplotlib` module. Used to create graphs


## Setup

Just execute

```
$ ./workhour.py setup
```

and then remember to add the `workhour.py` script to `$PATH` (or create a
symlink inside a folder already available to `$PATH`).


## Syntax

### The history file

The main database for this program is a simple text file. Such text file is
expected to be updated manually using an arbitrary text editor (aka there are
no fancy GUI). It's syntax should be:

 - expressive enough to perform some automated and useful statistics on it
 - simple to `grep`, `sed`, "put your preferred unix utility here"
 - quick to write/type

Example:

```txt
01/08/2021
02:20 - w | commuting > driving to/from clients
01:15 - w | project A > fixing bug 510043
01:00 - r | hobby > reading a book
03:00 - r | project B > reading the new documentation of sw XYZ

03/08
08:00 - w | project B > implementing new feature
```

There are 2 kinds of lines:

 - date reference. The format is `dd/mm[/yyyy]`. If the year is omitted, then
    it is inferred from any previous complete date (or by the current date)
 - task description. The format is `<time span> '-' <activity type> '|' [<project>] ['>' <description>]`
    which should be self-explanatory. The `<activity type>` should be the
    acronym of an activity listed in the appropriate file `activities.json`,
    but even if it is not, everything should work fine (it will just be less
    meaningful)

### The activities file

The `activities.json` database is another simple database, but it is json (so
mind the commas!). It contains the kinds of macro activity normally performed
while working. This file is not strictly necessary, but if its content matches
the corresponding entries inside `history.txt`, the final statistics, graphs,
exports will have nicer names. But even if not necessary, it is a good exercise
to think about "the kind of tasks normally performed at works", such to be able
to recognize which are the tasks that takes most of the time, the tasks that
are more easy or satisfying to tackle, etc... just some insight on your own
work for free!

Example:

```json
{
    "w": {
        "name": "work",
        "descr": "generic work not categorized anywhere else, a catchall."
    },
    "r": {
        "name": "reading",
        "descr": "time spent reading books, documentation, news, etc."
    }
}
```
