from datetime import datetime, timedelta
from pixella import post_to_pixella_since, post_to_pixella_yesterday
from toggl import check_toggl
import os

# OTHER
YESTERDAY = datetime.now().date() - timedelta(days=1)
SINCE = datetime.strptime("20231206", "%Y%m%d").date()
TEST_DAY = datetime.strptime("20231206", "%Y%m%d").date()


API_NAMES = {
    "pixella": {"token": "PIXELLA_TOKEN", "name": "PIXELLA_USERNAME"},
    "toggl": {"token": "TOGGL_API_TOKEN", "workspace": "TOGGL_WORKSPACE_ID"},
}

ENV_FILE = "./project/file.txt"

YES = ["y", "yes"]
NO = ["n", "no"]

FILE_EXISTS = os.path.isfile(ENV_FILE)

# post_to_pixella_yesterday(YESTERDAY)
# post_to_pixella_since(SINCE)


def edit_env_file(key, new_val):
    pass


def create_env_file(text):
    success = False 
    try: 
        with open(ENV_FILE, "w") as file:
            file.write(text)
        success = True
    except:
        pass
    return success


def get_toogl_info():
    success = False
    toggl_workspace_id = None
    toggl_token = input(
        "Please provide details of your Toggl account.\nToggl API token:   "
    )
    toggl_response = check_toggl(toggl_token)
    if toggl_response["success"]:
        toggl_workspace_id = toggl_response["workspace_id"]
        success = True
    else:
        while not toggl_response["success"]:
            toggl_token = input(f"{toggl_response['message']}\nPlease try again or enter 'stop'.\nToggl API token:   ")
            if toggl_token.lower() == 'stop':
                break
            toggl_response = check_toggl(toggl_token)

    return toggl_token, toggl_workspace_id, success


def get_pixella_info():
    success = False
    pixella_token = None
    pixella_username = None
    user_input = input(
        """Please choose the option:
    1. Enter Pixella details manually (if you already have an account).
    2. Create Pixella account now.
    Enter either 1 or 2:   """
    )

    if user_input == '1':
        pixella_token = input('Please provide details of your Pixella account.\nPixella API token:   ')
        pixella_username = input('Pixella username:   ')
        
        success = True
        # CHECK if accurate
    elif user_input == '2':
        pass

    return pixella_token, pixella_username, success




def start_app():
    options = [""]
    available_options = []
    greeting_text = "Welcome to Toggl to Pixella app!\n"
    print(greeting_text)

    if not FILE_EXISTS:
        user_input = input(
            """There's no information about your Toggl or Pixella accounts.
    Would you like to add it? (y/n)   """
        )
        if user_input in YES:
            toggl_token, toggl_workspace_id, toggl_success = get_toogl_info()

            if toggl_success:
                pixella_token, pixella_username, pixella_success = get_pixella_info()
                if pixella_success:
                    text = f"{API_NAMES['pixella']['token']}:{pixella_token}\n"
                    text += f"{API_NAMES['pixella']['name']}:{pixella_username}\n"
                    text += f"{API_NAMES['toggl']['token']}:{toggl_token}\n"
                    text += f"{API_NAMES['toggl']['workspace']}:{toggl_workspace_id}"
                    file_success = create_env_file(text)
                    if file_success:
                        print('File created!')
            else:
                print("Sorry, but without correct information about your Toggl account, this app is unable to fulfill its function.")
                user_input = input('Would you like to:\n1. Restart the app\n2.Close the app\nEnter 1 or 2:   ')
                if user_input == '1':
                    start_app()
                elif user_input == '2':
                    pass
                


# # check if the file exists
# if FILE_EXISTS:
#     with open(ENV_FILE) as file:
#         lines = file.readlines()
#         for line in lines:
#             print(line)

# # if there's no file then get info
# else:
#     user_input = input(
#         "There's no information about your Toggl or Pixella accounts.\nWould you like to add it? (y/n)   "
#     ).lower()
#     if user_input in YES:
#         toggl_token, toggl_workspace_id = get_toogl_info()
#         text = ""

#         print(text)
#     else:
#         print("Sorry, please come back later.")

start_app()
# get_toogl_info()
