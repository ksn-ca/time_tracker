import requests
from datetime import datetime, timedelta
import json
from dateutil import tz

from toggl import TOGGL_TIME_ENTRY_API, TOGGL_HEADER, TOGGL_PROJECTS_API
from pixella import PIXELLA_HEADER, PIXELLA_GRAPH_URLS

# OTHER
from_zone = tz.gettz("UTC")
to_zone = tz.gettz("America/Montreal")
YESTERDAY = datetime.now().date() - timedelta(days=1)


def get_toggl_entries(date):
    date_to = date + timedelta(days=1)
    time_entry_params = {"start_date": str(date), "end_date": str(date_to)}
    time_entries_response = requests.get(
        TOGGL_TIME_ENTRY_API, headers=TOGGL_HEADER, params=time_entry_params
    )
    time_entries = json.loads(time_entries_response.text)
    return time_entries


def get_toggl_projects():
    projects_response = requests.get(TOGGL_PROJECTS_API, headers=TOGGL_HEADER)
    projects_json = json.loads(projects_response.text)
    projects_dict = {entry["id"]: entry["name"] for entry in projects_json}
    return projects_dict


def get_duration_per_project(entries, projects_dict):
    project_time_dict = {}
    for entry in entries:
        if entry["stop"] != None:
            project = projects_dict[entry["project_id"]]
            duration = entry["duration"]
            utc_date = datetime.strptime(
                entry["start"], "%Y-%m-%dT%H:%M:%S+00:00"
            ).replace(tzinfo=from_zone)
            actual_date = utc_date.astimezone(to_zone).date().strftime("%Y%m%d")
            key = (project, actual_date)
            if key in project_time_dict:
                project_time_dict[key] += duration
            else:
                project_time_dict[key] = duration 
    return project_time_dict


def post_to_pixella(duration_dict):
    
    for key, value in duration_dict.items():
        project = key[0]
        date = key[1]
        duration_min = value // 60

        individual_pixella_post(project, date, duration_min)

def individual_pixella_post(project, date, duration_min):
    if project in PIXELLA_GRAPH_URLS:
        post_params = {"date": date, "quantity": str(duration_min)}
        response = requests.post(
            PIXELLA_GRAPH_URLS[project], json=post_params, headers=PIXELLA_HEADER
        )
        if response.json()['isSuccess'] == False:
            print('RETRYING')
            individual_pixella_post(project, date, duration_min)
        else: print(response.text)






projects_dict = get_toggl_projects()
toggl_entries = get_toggl_entries(YESTERDAY)
duration_dict = get_duration_per_project(toggl_entries, projects_dict)
post_to_pixella(duration_dict)
