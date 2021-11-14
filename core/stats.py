from . import taskslist
from . import activity
import collections
import datetime
import warnings


def filterByDate(tasks, start_date=None, end_date=None):
    after_start = lambda x: start_date is None or start_date <= x.date
    before_end = lambda x: end_date is None or x.date <= end_date
    return [task for task in tasks if after_start(task) and before_end(task)]


def filterByActivity(tasks, activity):
    return [task for task in tasks if task.activity_type == activity]


def advanceDate(date, granularity, quantity):
    if granularity == "d":
        pass
    elif granularity == "w":
        quantity *= 7
    elif granularity == "m":
        quantity *= 365/12.
    return date + datetime.timedelta(quantity)


class TasksGroup:
    def __init__(self, ref_date, tasks=None):
        self.ref_date = ref_date
        self.tasks = tasks or []

    def collapsed(self):
        if len(self.tasks) == 0:
            return (self.ref_date, 0, {}, {})
        total_time = sum(task.duration for task in self.tasks)
        activities = collections.defaultdict(list)
        for task in self.tasks:
            activities[task.activity_type].append(task)
        result_absolute = {}
        result_percentage = {}
        for k in sorted(activities):
            t = sum(task.duration for task in activities[k])
            p = float(t) / total_time
            result_absolute[k] = t
            result_percentage[k] = p
        return (self.ref_date, total_time, result_absolute, result_percentage)


def groupTasksByTimespan(tasks, start_date, granularity="d", quantity=1):
    """
    Note: start date is not necessary the date of the first entry inside tasks!
    """
    res = [TasksGroup(start_date)]
    next_group_start_date = advanceDate(start_date, granularity, quantity)
    for task in tasks:
        while task.date >= next_group_start_date:
            res.append(TasksGroup(next_group_start_date))
            next_group_start_date = advanceDate(
                next_group_start_date, granularity, quantity)
        res[-1].tasks.append(task)
    return res


def aggregated(start_date, end_date=None, filter_by=None, group_by=("d", 1)):
    if start_date is None:
        raise Exception("stats.list must have a start date!")
    tasks = taskslist.get()
    tasks = filterByDate(tasks, start_date, end_date)
    if filter_by is not None:
        if filter_by[0] == "activity":
            tasks = filterByActivity(tasks, filter_by[1])
        else:
            warnings.warn("not implemented: can only filter by activity")
    groups = groupTasksByTimespan(tasks, start_date, group_by[0], group_by[1])
    activities_name = activity.get()
    for group in groups:
        ref_date, total_time, absolute, percentage = group.collapsed()
        if total_time <= 0:
            continue
        print(f"==({ref_date})==============")
        for k in sorted(absolute):
            a = absolute[k]
            p = percentage[k]
            n = activities_name.get(k, f"other({k})")
            print(f" {n:>16s}: {p: >3.0%} > {a/60.:.1f}h")
        print(f"------------------------ {total_time/60.:.1f}h")
        print()
    return 0


def graph():
    pass
