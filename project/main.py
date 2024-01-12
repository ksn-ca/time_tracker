from datetime import datetime, timedelta
from pixella import post_to_pixella_since, post_to_pixella_yesterday, create_pixella_user
from toggl import check_toggl
import os
import sys

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
# def #clear(): os.system('cls' if os.name=='nt' else 'clear')

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
    #clear()
    toggl_workspace_id = None
    toggl_token = input(
        "Please provide details of your Toggl account.\nToggl API token:   "
    )
    toggl_response = check_toggl(toggl_token)
    if not toggl_response["success"]:
        while not toggl_response["success"]:
            #clear()
            toggl_token = input(
                f"{toggl_response['message']}\nPlease try again or enter 'stop'.\nToggl API token:   ").strip()
            if toggl_token.lower() == 'stop':
                break
            toggl_response = check_toggl(toggl_token)
    return toggl_token, toggl_response["workspace_id"], toggl_response['success']


def get_pixella_info():
    #clear()
    success = False
    pixella_token = None
    pixella_username = None
    user_input = ''
    while user_input not in ['1', '2']:
        user_input = input(
            """Please choose the option:
        1. Enter Pixella details manually (if you already have an account).
        2. Create Pixella account now.
        Enter either 1 or 2:   """
        ).strip()

        if user_input == '1':
            pixella_username, pixella_token, success = provide_pixella_details()
            # CHECK if accurate
        elif user_input == '2':
            pixella_username, pixella_token, success = create_new_pixella_account()
            
        else:
            print('Sorry, this input is not supported.')


    return pixella_token, pixella_username, success

def create_new_pixella_account():
    pixella_username = input('The username must follow the following pattern: [a-z][a-z0-9-]{1,32}. Enter desired username:   ').strip()
    pixella_token = input("""You must create your own token. 
    A token string used to authenticate as a user to be created. 
    The token string is hashed and saved. Validation rule: [ -~]{8,128}
    Enter desired token:   """).strip()
    pixella_TOS_prompt = 'Specify yes or no whether you agree to the terms of service. Enter yes or no:   '
    pixella_TOS_error_message = 'Sorry, without agreeing to terms of service, this app is unable to create an account for you.'
    pixella_TOS = handle_user_iput(pixella_TOS_prompt, pixella_TOS_error_message) 

    pixella_not_minor_prompt = 'Specify yes or no as to whether you are not a minor or if you are a minor and you have the parental consent of using this service. Enter yes or no:   '
    pixella_not_minor_error_message = 'Sorry, but minors (or minors without parental consent) are not allowed to use Pixella.'
    pixella_not_minor = handle_user_iput(pixella_not_minor_prompt, pixella_not_minor_error_message) 
    pixella_thanks_code = input('If you are a Pixella Patreon supporter, then please enter the thanks code. Otherwise, click enter:   ').strip()
    response = create_pixella_user(pixella_token, pixella_username, pixella_TOS, pixella_not_minor, pixella_thanks_code)

    if not response['isSuccess']:
        print('There was an error while making your account. The error from Pixella is:')
        print(response['message'])

        user_input = ''
        while user_input not in [YES, NO]:
            user_input = input('Would you like to try again? Enter yes or no:   ').strip().lower()
            if user_input in YES:
                return create_new_pixella_account()
            elif user_input in NO:
                break
            else:
                print('This input is not supported.')

    return pixella_username, pixella_token, response['isSuccess']


def handle_user_iput(prompt, error_message):
    user_input = ''

    while user_input not in [YES, NO]:
        user_input = input(prompt).strip().lower()
        if user_input in YES:
            return 'yes'
        elif user_input in NO:
            print(error_message)
            user_input = input('Would you like to try again? Enter yes or no:   ').strip().lower()
            if user_input in NO:
                print(error_message)
                print('The app now will be restarted.')
                restart_prompt()
            elif user_input == 'yes':
                return incorrect_input(prompt, error_message)
        else:
            print('This input is not supported.')

def provide_pixella_details():
    pixella_token = input(
        'Please provide details of your Pixella account.\nPixella API token:   ').strip()
    pixella_username = input('Pixella username:   ').strip()

    success = True
    return pixella_username, pixella_token, success


def create_env_text(toggl_token, toggl_workspace_id, pixella_token, pixella_username):
    text = f"{API_NAMES['pixella']['token']}:{pixella_token}\n"
    text += f"{API_NAMES['pixella']['name']}:{pixella_username}\n"
    text += f"{API_NAMES['toggl']['token']}:{toggl_token}\n"
    text += f"{API_NAMES['toggl']['workspace']}:{toggl_workspace_id}"
    return text

def create_toggl_env_text(toggl_token, toggl_workspace_id):
    text = f"{API_NAMES['toggl']['token']}:{toggl_token}\n"
    text += f"{API_NAMES['toggl']['workspace']}:{toggl_workspace_id}\n"
    return text

def create_pixella_env_text(pixella_token, pixella_username):
    text = f"{API_NAMES['pixella']['token']}:{pixella_token}\n"
    text += f"{API_NAMES['pixella']['name']}:{pixella_username}\n"
    return text

def restart_prompt(prompt=''):
    #clear()
    print(prompt)
    user_input = ''
    while user_input not in ['1', '2']:
        user_input = input(
            """Would you like to:
            1. Restart the app
            2. Close the app
            Enter 1 or 2:   """).strip()

        if user_input == '1':
            #clear()
            start_app()
        elif user_input == '2':
            sys.exit('Sorry to see you go. Come back later!')
        else:
            #clear()
            print('Sorry, this input is not supported.')


def start_app():
    
    if not FILE_EXISTS:
        user_input = input(
            """There's no information about your Toggl or Pixella accounts.
    Would you like to add it? (y/n)   """
        ).strip().lower()
        if user_input in YES:
            toggl_token, toggl_workspace_id, toggl_success = get_toogl_info()

            if toggl_success:
                pixella_token, pixella_username, pixella_success = get_pixella_info()
                if pixella_success:
                    text = create_env_text(
                        toggl_token, toggl_workspace_id, pixella_token, pixella_username)
                    file_success = create_env_file(text)

                    if file_success:
                        print('File created!')
                else:
                    prompt = "Sorry, but without information about your Pixella account, this app is unable to fulfill its function."
                    restart_prompt(prompt)
            else:
                prompt = "Sorry, but without correct information about your Toggl account, this app is unable to fulfill its function."
                restart_prompt(prompt)
                # user declines to provide information
        else:
            prompt = 'Sorry, but without information about your accounts, this app is unable to fulfill its function.'
            restart_prompt(prompt)

    # FILE EXISTS
    else:
        pass

#clear()
print("Welcome to Toggl to Pixella app!\n")
start_app()
