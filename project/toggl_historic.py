import pandas as pd
from datetime import datetime
from pixella import post_to_pixella

FILE_PATH = "csv/Toggl_time_entries_2023-01-01_to_2023-12-31.csv"

def post_csv_to_pixella(file_path):
    toggl_csv = pd.read_csv(file_path)


    toggl_dict = {}
    for index, row in toggl_csv.iterrows():
        project = row["Project"]
        start_date = row["Start date"]
        orig_duration = row["Duration"]

        date = datetime.strptime(start_date, "%Y-%m-%d").date().strftime("%Y%m%d")
        duration_array = [int(val) for val in orig_duration.split(":")]
        duration = (
            (duration_array[0] * 60 * 60) + (duration_array[1] * 60) + duration_array[2]
        )
        # print(project, date, duration)

        key = (project, date)
        if key in toggl_dict:
            toggl_dict[key] += duration
        else:
            toggl_dict[key] = duration


    post_to_pixella(toggl_dict)
    print(f'Successfully posted the information provided in the Toggl file {file_path} to Pixella.')

# post_csv_to_pixella(FILE_PATH)
