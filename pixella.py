import requests
from decouple import config

# PIXELLA GRAPH
PIXELLA_API = "https://pixe.la/v1/users"
PIXELLA_TOKEN = config("PIXELLA_TOKEN")
PIXELLA_USERNAME = config("PIXELLA_USERNAME")
PIXELLA_GRAPH_API = f"{PIXELLA_API}/{PIXELLA_USERNAME}/graphs"
PIXELLA_HEADER = {"X-USER-TOKEN": PIXELLA_TOKEN}


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
        get_pixella_graphs()
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


PIXELLA_GRAPH_URLS = create_pixella_urls()
