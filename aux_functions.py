# Author: aqeelanwar
# Created: 15 May,2020, 7:03 PM
# Email: aqeel.anwar@gatech.edu
import plotly.graph_objects as go
import chart_studio.plotly as py
from plotly.subplots import make_subplots

ORANGE = "#DD8047"
BLUE = "94B6D2"
GREEN = "#A5AB81"
YELLOW = "#D8B25C"

def plot_stat(x, y1, y2, repo_name, type="offline"):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y1,
            mode="lines",
            name="Clones",
            line=dict(color=ORANGE, width=3),
            marker=dict(size=10, color=ORANGE),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y2,
            mode="lines",
            name="Views",
            line=dict(color=GREEN, width=3),
            marker=dict(size=10, color=GREEN),
        ),
        secondary_y=True,
    )

    fig.update_layout(
        title=repo_name,
        font=dict(color="#7f7f7f"),
        autosize=True,
        legend=dict(x=0, y=1, orientation="v"),
        margin=dict(l=0, r=0, t=40, b=30),
    )
    if type == "offline":
        fig.show()
    elif type == "online":
        url = py.plot(fig, filename=repo_name, sharing="public")
        print(url)


def display_StatTheGit():
    with open("display.txt", "r") as file:
        for line in file:
            print(line, end="")
