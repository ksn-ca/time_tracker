from base64 import b64encode
from decouple import config

# TOGGL TIME TRACKER
TOGGL_WORKSPACE_ID = config("TOGGL_WORKSPACE_ID")

TOGGL_ME_URL = "https://api.track.toggl.com/api/v9/me"
TOGGL_TIME_ENTRY_API = "https://api.track.toggl.com/api/v9/me/time_entries"
TOGGL_PROJECTS_API = (
    f"https://api.track.toggl.com/api/v9/workspaces/{TOGGL_WORKSPACE_ID}/projects"
)
TOGGL_API_TOKEN = config("TOGGL_API_TOKEN")

toggl_api_encoded = (f"{TOGGL_API_TOKEN}:api_token").encode("ascii")
TOGGL_BYTE_API = b""
TOGGL_BYTE_API += toggl_api_encoded

TOGGL_HEADER = {
    "content-type": "application/json",
    "Authorization": "Basic %s" % b64encode(TOGGL_BYTE_API).decode("ascii"),
}
