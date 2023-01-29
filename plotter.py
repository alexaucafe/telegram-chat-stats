import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from chat import Chat

class Plotter:

    def __init__(self, group_stats) -> None:
        self.group_stats = group_stats

    def plot_members(self, reverse = False):

        # Data
        members = []
        forwards = []
        replies = []
        messages = []

        for member in self.group_stats["members"]:
            members.append(member["first_name"])
            messages.append(member["messages_count"])
            forwards.append(member["forwards_count"])
            replies.append(member["replies_count"])

        messages = np.array(messages)
        forwards = np.array(forwards)
        replies = np.array(replies)

        # Plotting
        fig, ax = plt.subplots()
        p1 = ax.barh(members, messages, color="lightsteelblue")
        p2 = ax.barh(members, forwards, label='forwards', color="royalblue")
        p3 = ax.barh(members, replies, left=forwards, label='replies', color="cornflowerblue")

        # Appearance
        fig.set_figheight(len(members)/2.2)
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        ax.set_xlabel("Messages")
        ax.bar_label(p1, padding = 5)
        ax.xaxis.set_label_position("top")
        # ax.set_title(self.group_stats["name"], loc="left", size=20)
        ax.margins(0.12, 0.01)

        if reverse == True:
            ax.legend(loc = "upper right")
        else:
            ax.legend(loc = "lower right")

        return plt, fig
    
    def plot_days(self, days):

        # Data
        dates = []
        messages = []

        for day in days["days"]:
            dates.append(day["date"])
            messages.append(day["messages_count"])
        
        dates = np.array(dates)
        messages = np.array(messages)

        # Plotting
        fig, ax = plt.subplots()
        ax.plot(dates, messages, color="royalblue")

        # Formatting ticks
        locator = mdates.AutoDateLocator()
        formatter = mdates.ConciseDateFormatter(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.xaxis.set_minor_locator(mdates.DayLocator())

        # Works fine, but isn't universal
        # ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=(1)))
        # ax.xaxis.set_minor_locator(mdates.DayLocator(bymonthday=(10, 20)))
        # ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        # ax.xaxis.set_minor_formatter(mdates.DateFormatter('%d'))

        return plt, fig