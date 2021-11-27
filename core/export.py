from . import taskslist
from . import activity
from . import stats
import collections
import datetime
import warnings

"""
==(01/03/2021)===   05:45
# management        02:00
 * aaa
 * aaa
 * aaa
#
"""
def list(start_date, end_date):
    activities_name = activity.acronymMap()
    def formatDuration(duration):
        return f"{duration//60:02d}:{duration%60:02d}"
    def formatActivity(activity_type):
        return activities_name.get(activity_type, f"other({activity_type})")

    tasks = stats.filterByDate(taskslist.get(), start_date, end_date)
    groups = stats.groupTasksByTimespan(tasks, start_date, granularity="d", quantity=1)
    for group in groups:
        duration = formatDuration(group.totalDuration())
        print(f"==({group.ref_date})====  {duration}")
        for a, ts in group.perActivityType():
            activity_name = formatActivity(a)
            activity_duration = formatDuration(sum([t.duration for t in ts]))
            print(f"#{activity_name:<20s} {activity_duration}")
            for t in ts:
                print(f" * {t.project} {t.content}")
    return 0
