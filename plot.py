import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime as dt
import datetime
from collections import Counter
import os


def is_today(date_time):
    border = dt.now() - datetime.timedelta(hours=24)
    return date_time >= border


def minute_precition(date_time):
    t = date_time
    return dt(t.year, t.month, t.day, t.hour, t.minute)


def create_done_plot(notes, user_dir):
    times = [dt.fromtimestamp(note[2]) for note in notes if note[2] != 0]
    # remove entries older than one day
    times = [t for t in times if is_today(t)]
    # remove seconds info in entries
    times = sorted([minute_precition(t) for t in times])

    cnt = Counter(times)
    x = list(cnt)
    y = cnt.values()

    fig, ax = plt.subplots()
    if len(x) > 0:
        ax.stem(x, y)

    labels = [date.strftime('%H:%M') for date in x]
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks done')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    ax.set_title('Task completion chart')

    plot_file_name = os.path.join(user_dir, "plot.png")
    fig.savefig(plot_file_name)
    return plot_file_name
