import requests
from decouple import config

from datetime import datetime, timedelta
from toggl import get_toggl_entries, get_toggl_projects, get_duration_per_project

# PIXELLA GRAPH
PIXELLA_API = "https://pixe.la/v1/users"
PIXELLA_TOKEN = config("PIXELLA_TOKEN")
PIXELLA_USERNAME = config("PIXELLA_USERNAME")
PIXELLA_GRAPH_API = f"{PIXELLA_API}/{PIXELLA_USERNAME}/graphs"
PIXELLA_HEADER = {"X-USER-TOKEN": PIXELLA_TOKEN}

YESTERDAY = datetime.now().date() - timedelta(days=1)


def create_date_range(start_date, end_date):
    delta = timedelta(days=1)

    # Create an array of date objects
    date_array = []
    current_date = start_date
    while current_date < end_date:
        date_array.append(current_date)
        current_date += delta

    return date_array


def create_new_graph(
    id,
    project_name,
    unit="min",
    unit_type="int",
    color="sora",
    timezone="America/Montreal",
):
    graph_params = {
        "id": id,
        "name": project_name,
        "unit": unit,
        "type": unit_type,
        "color": color,
        "timezone": timezone,
    }
    response = requests.post(
        PIXELLA_GRAPH_API, json=graph_params, headers=PIXELLA_HEADER
    )
    print(response.text)


def get_pixella_graphs():
    response = requests.get(PIXELLA_GRAPH_API, headers=PIXELLA_HEADER)
    if "message" in response.json():
        print("RETRYING")
        return get_pixella_graphs()
    else:
        pixella_graph_dict = {
            graph["name"]: graph["id"] for graph in response.json()["graphs"]
        }
        return pixella_graph_dict


def create_pixella_urls():
    pixella_graph_dict = get_pixella_graphs()
    pixella_url_dict = {
        project: f"{PIXELLA_GRAPH_API}/{id}"
        for project, id in pixella_graph_dict.items()
    }
    return pixella_url_dict


def individual_pixella_post(project, date, duration_min):
    pixella_graph_urls = create_pixella_urls()
    if project in pixella_graph_urls:
        post_params = {"date": date, "quantity": str(duration_min)}
        response = requests.post(
            pixella_graph_urls[project], json=post_params, headers=PIXELLA_HEADER
        )
        if response.json()["isSuccess"] == False:
            print("RETRYING")
            individual_pixella_post(project, date, duration_min)
        else:
            print(response.text)


def post_to_pixella(duration_dict):
    for key, value in duration_dict.items():
        project = key[0]
        date = key[1]
        duration_min = value // 60

        individual_pixella_post(project, date, duration_min)


def post_to_pixella_since(since, to=YESTERDAY):
    date_array = create_date_range(since, to)
    projects_dict = get_toggl_projects()
    for date in date_array:
        toggl_entries = get_toggl_entries(date)
        duration_dict = get_duration_per_project(toggl_entries, projects_dict)
        post_to_pixella(duration_dict)
        print("SUCCESS", date)


def post_to_pixella_yesterday(day):
    projects_dict = get_toggl_projects()
    toggl_entries = get_toggl_entries(day)
    duration_dict = get_duration_per_project(toggl_entries, projects_dict)
    post_to_pixella(duration_dict)
    print("SUCCESS")

def create_pixella_user(token, username, agree_TOS, not_minor, thanks_code):
    # delete_pixella_user(username, token)
    params = {'token': token, 'username': username, 'agreeTermsOfService': agree_TOS, 'notMinor': not_minor}
    response = requests.post(PIXELLA_API, json=params)

    return response.json()

def delete_pixella_user(user, token):
    delete_api = f'{PIXELLA_API}/{user}'
    header = {"X-USER-TOKEN": token}

    response = requests.delete(delete_api, headers=header)
    print(response.json())

