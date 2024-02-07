from base64 import b64encode
from datetime import datetime, timedelta
from dateutil import tz
import json
import requests
from decouple import config
from dotenv import load_dotenv

from_zone = tz.gettz("UTC")
to_zone = tz.gettz("America/Montreal")

# TOGGL TIME TRACKER
# TOGGL_WORKSPACE_ID = config("TOGGL_WORKSPACE_ID")

TOGGL_ME_URL = "https://api.track.toggl.com/api/v9/me"
TOGGL_TIME_ENTRY_API = "https://api.track.toggl.com/api/v9/me/time_entries"
# TOGGL_PROJECTS_API = (
#     f"https://api.track.toggl.com/api/v9/workspaces/{TOGGL_WORKSPACE_ID}/projects"
# )
# TOGGL_API_TOKEN = config("TOGGL_API_TOKEN", default='')

# toggl_api_encoded = (f"{TOGGL_API_TOKEN}:api_token").encode("ascii")
# TOGGL_BYTE_API = b""
# TOGGL_BYTE_API += toggl_api_encoded

# TOGGL_HEADER = {
#     "content-type": "application/json",
#     "Authorization": "Basic %s" % b64encode(TOGGL_BYTE_API).decode("ascii"),
# }

def get_toggl_workspace_id():
    load_dotenv()
    return config("TOGGL_WORKSPACE_ID")

def get_toggl_api_token():
    load_dotenv()
    return config("TOGGL_API_TOKEN")

def get_toggl_projects_api():
    return f"https://api.track.toggl.com/api/v9/workspaces/{get_toggl_workspace_id()}/projects"

def get_toggl_header():
    toggl_api_encoded = (f"{get_toggl_api_token()}:api_token").encode("ascii")
    toggl_byte_api = b""
    toggl_byte_api += toggl_api_encoded

    return {
        "content-type": "application/json",
        "Authorization": "Basic %s" % b64encode(toggl_byte_api).decode("ascii"),
    }


def check_toggl(api_key):
    success = False
    api_key_encoded = (f"{api_key}:api_token").encode("ascii")
    api_key_encoded = b"" + api_key_encoded

    toggl_header = {
        "content-type": "application/json",
        "Authorization": "Basic %s" % b64encode(api_key_encoded).decode("ascii"),
    }
    try:
        response = requests.get(TOGGL_ME_URL, headers=toggl_header)
        response.raise_for_status()
        success = True
        return {'success': success, 'message': 'API key is correct.', 'workspace_id': response.json()['default_workspace_id']}

    except requests.exceptions.HTTPError:
        return {'success': success, 'message': 'The API key is incorrect.', 'workspace_id': None}
    except:
        return {'success': success, 'message': 'There was an error in processing the request.', 'workspace_id': None}

    

def get_toggl_entries(date):
    date_to = date + timedelta(days=1)
    time_entry_params = {"start_date": str(date), "end_date": str(date_to)}
    time_entries_response = requests.get(
        TOGGL_TIME_ENTRY_API, headers=get_toggl_header(), params=time_entry_params
    )

    # time_entries = json.loads(time_entries_response.text)
    return time_entries_response.json()


def get_toggl_projects():
    projects_response = requests.get(get_toggl_projects_api(), headers=get_toggl_header())
    projects_json = json.loads(projects_response.text)
    projects_dict = {entry["id"]: entry["name"] for entry in projects_json}
    return projects_dict


def get_duration_per_project(entries, projects_dict):
    project_time_dict = {}
    try:
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
    except:
        print(str(entries).capitalize())
