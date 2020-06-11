# Author: aqeelanwar
# Created: 10 June,2020, 4:40 PM
# Email: aqeel.anwar@gatech.edu

import os
import numpy as np
import chart_studio
import pandas as pd
import argparse
import datetime
from aux_functions import plot_stat


# Command-line input setup
parser = argparse.ArgumentParser(description="Display GitHub Stats")
parser.add_argument(
    "--username", type=str, default="", help="Chart Studio (Plotly) username",
)
parser.add_argument(
    "--api_key",
    type=str,
    default="",
    help="Chart Studio (Plotly) API Key",
)
parser.add_argument(
    "--stat_folder",
    type=str,
    default="repo_stats/aqeelanwar",
    help="Folder to the GitHub stat csvs",
)
parser.add_argument(
    "--display_type",
    type=str,
    default="offline",
    help="Display the plots",
    choices=["offline", "online"],
)


if __name__ == "__main__":
    args = parser.parse_args()
    # chart_studio.tools.set_credentials_file(
    #     username=args.username, api_key=args.api_key
    # )
    folder = args.stat_folder

    f = []
    _, _, files = os.walk(folder).__next__()

    for file in files:
        if file.endswith(".txt") and "_temp" not in file:
            print("Processing: ", file)
            path = folder + "/" + file
            total_clones = []
            total_traffic = []
            date_array = []
            df = pd.read_csv(path)
            date = df.Date
            clones = df.Clones
            traffic = df.Traffic
            for j in range(len(date)):
                d = (
                    datetime.datetime.strptime(date[j], "%Y-%m-%d")
                    .date()
                    .strftime("%b %d,%Y")
                )
                date_array.append(d)
                total_clones.append(np.sum(np.asarray(clones[0 : j + 1], dtype=int)))
                total_traffic.append(np.sum(np.asarray(traffic[0 : j + 1], dtype=int)))

            plot_stat(
                x=date,
                y1=total_clones,
                y2=total_traffic,
                repo_name=file.split(".")[0],
                type=args.display_type,
            )
