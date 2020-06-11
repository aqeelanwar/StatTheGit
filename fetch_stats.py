# Author: aqeelanwar
# Created: 4 June,2020, 8:02 PM
# Email: aqeel.anwar@gatech.edu

from github import Github
import datetime
import csv
from collections import OrderedDict
from shutil import copy2
import os
from tqdm import tqdm
import argparse

# Command-line input setup
parser = argparse.ArgumentParser(
    description="StatTheGit - Maintain GitHub repository stats for more than 14 days"
)
parser.add_argument(
    "--GitToken",
    type=str,
    default="",
    help="GitHub token to your profile",
)
parser.add_argument(
    "--username", type=str, default="", help="GitHub Username",
)
parser.add_argument(
    "--RepoNames",
    type=str,
    default="PEDRA",
    nargs="+",
    help="Name of repositories seperated by space. Leave it empty and all the repositories will be serviced",
)


if __name__ == "__main__":
    # Parse the command line
    args = parser.parse_args()
    g = Github(args.GitToken)
    repo_names = []

    # Check the repositories
    if "all" not in args.RepoNames:
        repo_names.append(args.RepoNames)
    else:
        for repo in g.get_user().get_repos():
            ccc = repo._full_name.value
            if args.username in repo._full_name.value:
                repo_n = repo._full_name.value
            repo_names.append(repo_n)
    cc = 1
    print(repo_names)

    for repo_n in tqdm(repo_names):
        # Process each repository
        repo_str = args.username + "/" + repo_n
        print("Processing: ", repo_n)
        repo = g.get_repo(repo_str)

        # Get repository clones statistics
        clone_stat = repo.get_clones_traffic()
        clone_stat = clone_stat["clones"]

        # Get repository views statistics
        traffic_stat = repo.get_views_traffic()
        traffic_stat = traffic_stat["views"]

        # The stats fetched from GitHub packaged has date missing where the clones/views are zero.
        # The following lines appends missing dates and orders them.

        if len(clone_stat) > 0:
            # Find the earliest date between the views and clones
            if clone_stat[0].timestamp.date() < traffic_stat[0].timestamp.date():
                earliest_date = clone_stat[0].timestamp.date()
            else:
                earliest_date = traffic_stat[0].timestamp.date()

            date_array = []
            clone_array = {}
            traffic_array = {}

            # Generate array of dates under consideration
            for d in range(14):
                latest_date = str(earliest_date + datetime.timedelta(days=d))
                # Assign zeros to clone and views statistics
                clone_array[latest_date] = 0
                traffic_array[latest_date] = 0

            # Populate the clone statistics for the available date.
            # For unavailable dates, the stat is already initialized to zero
            for c in clone_stat:
                clone_array[str(c.timestamp.date())] = c.count

            for v in traffic_stat:
                traffic_array[str(v.timestamp.date())] = v.count

            # Create the folder of username if it doesn't exists
            path_to_folder = "repo_stats/" + args.username
            if not os.path.exists(path_to_folder):
                os.makedirs(path_to_folder)

            csv_str = "repo_stats/" + repo_str + ".txt"
            csv_str_temp = "repo_stats/" + repo_str + "_temp.txt"

            # Save the stat file as another temp file.
            if os.path.exists(csv_str):
                s = copy2(csv_str, csv_str_temp)

            # Create CSV file.
            csv_file = open(csv_str, "w")
            writer = csv.writer(csv_file)
            # Define header of the CSV file
            writer.writerow(["Date", "Clones", "Traffic"])

            clone_array = OrderedDict(sorted(clone_array.items(), key=lambda t: t[0]))
            traffic_array = OrderedDict(
                sorted(traffic_array.items(), key=lambda t: t[0])
            )

            if os.path.exists(csv_str_temp):
                # copyfile(csv_str, csv_str_temp)
                cc = 1
                with open(csv_str_temp) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=",")
                    line_count = 0
                    for row in csv_reader:
                        if line_count > 0:
                            datetime_obj = datetime.datetime.strptime(
                                row[0], "%Y-%m-%d"
                            ).date()
                            compare_date = datetime.datetime.strptime(
                                str(earliest_date), "%Y-%m-%d"
                            ).date()

                            if datetime_obj < compare_date:
                                writer.writerow([row[0], row[1], row[2]])
                            else:
                                break
                        line_count += 1

            for (key_clone, value_clone), (key_traffic, value_traffic) in zip(
                clone_array.items(), traffic_array.items()
            ):
                writer.writerow([key_clone, value_clone, value_traffic])

            csv_file.close()

            csv_file = open(csv_str_temp, "w")
            writer = csv.writer(csv_file)
            # writer.writerow(["Date", "Clones", "Traffic"])
            with open(csv_str) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                for row in csv_reader:
                    writer.writerow([row[0], row[1], row[2]])
            csv_file.close()

            # Remove temp file.
            os.remove(csv_str_temp)


