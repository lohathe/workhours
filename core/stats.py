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
        raise Exception("stats.aggregated must have a start date!")
    tasks = taskslist.get()
    tasks = filterByDate(tasks, start_date, end_date)
    if filter_by is not None:
        if filter_by[0] == "activity":
            tasks = filterByActivity(tasks, filter_by[1])
        else:
            warnings.warn("not implemented: can only filter by activity")
    groups = groupTasksByTimespan(tasks, start_date, group_by[0], group_by[1])
    activities_name = activity.acronymMap()
    for group in groups:
        ref_date, total_time, absolute, percentage = group.collapsed()
        if total_time <= 0:
            continue
        print(f"==({ref_date})==============")
        for k in sorted(absolute):
            a = absolute[k]
            p = percentage[k]
            n = activities_name.get(k, f"other({k})")
            print(f" {n: >16s}: {p: >3.0%} > {a/60.:.1f}h")
        print(f"------------------------ {total_time/60.:.1f}h")
        print()
    return 0


def graph(start_date, end_date=None, filter_by=None, group_by=("d", 1)):
    if start_date is None:
        raise Exception("stats.graph must have a start date!")
    tasks = taskslist.get()
    tasks = filterByDate(tasks, start_date, end_date)
    if filter_by is not None:
        if filter_by[0] == "activity":
            tasks = filterByActivity(tasks, filter_by[1])
        else:
            warnings.warn("not implemented: can only filter by activity")
    groups = groupTasksByTimespan(tasks, start_date, group_by[0], group_by[1])
    activities_name = activity.acronymMap()
    used_activities = {t.activity_type for t in tasks}

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.set_ylim([-0.1, 1.0])
    lines = []
    for a in used_activities:
        data = [(g.ref_date, g.collapsed()[3].get(a, 0)) for g in groups]
        xs, ys = zip(*data)
        label = activities_name.get(a, f"other({a})")
        line = ax.plot(xs, ys, lw=2, label=label)
        lines.append(line)
    legend = ax.legend(fancybox=True, shadow=True, bbox_to_anchor=(1,1), loc="upper left")
    lines_map = {}
    for legend_line, original_line in zip(legend.get_lines(), lines):
        legend_line.set_picker(True)
        lines_map[legend_line] = original_line
    def on_picker(event):
        legend_line = event.artist
        original_line = lines_map[legend_line][0]
        visible = not original_line.get_visible()
        original_line.set_visible(visible)
        legend_line.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw()
    fig.canvas.mpl_connect("pick_event", on_picker)
    plt.show()
    return 0
