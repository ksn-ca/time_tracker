from datetime import datetime, timedelta
from pixella import post_to_pixella_since, post_to_pixella_yesterday, create_pixella_user
from toggl import check_toggl
import os
import sys
import re
from text_dict import TEXT_DICT

# OTHER
YESTERDAY = datetime.now().date() - timedelta(days=1)
SINCE = datetime.strptime("20231206", "%Y%m%d").date()
TEST_DAY = datetime.strptime("20231206", "%Y%m%d").date()
PIXELLA_USERNAME_REGEX = r'[a-z][a-z0-9-]{1,32}'
PIXELLA_TOKEN_REGEX = r'[ -~]{8,128}'


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
    toggl_token = input(TEXT_DICT['PROMPTS']['TOGGL_API'])
    toggl_response = check_toggl(toggl_token)
    if not toggl_response["success"]:
        while not toggl_response["success"]:
            #clear()
            toggl_token = input(
                f"{toggl_response['message']}\n{TEXT_DICT['ERROR_MESSAGES']['TOGGL_API_ERROR']}").strip()
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
        user_input = input(TEXT_DICT['PROMPTS']['PIXELLA_CHOICE_PROMPT']).strip()

        if user_input == '1':
            pixella_username, pixella_token, success = provide_pixella_details()
            # CHECK if accurate
        elif user_input == '2':
            pixella_username, pixella_token, success = create_new_pixella_account()
            
        else:
            print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])


    return pixella_token, pixella_username, success

def create_new_pixella_account():
    pixella_username = handle_user_regex_inputs(PIXELLA_USERNAME_REGEX, TEXT_DICT['PROMPTS']['PIXELLA_USERNAME'], TEXT_DICT['ERROR_MESSAGES']['PIXELLA_INCORRECT_USERNAME'] )
    pixella_token = handle_user_regex_inputs(PIXELLA_TOKEN_REGEX, TEXT_DICT['PROMPTS']['PIXELLA_TOKEN'], TEXT_DICT['ERROR_MESSAGES']['PIXELLA_INCORRECT_TOKEN'])
    pixella_TOS = handle_user_input(TEXT_DICT['PROMPTS']['PIXELLA_TOS'],  TEXT_DICT['ERROR_MESSAGES']['PIXELLA_INCCORECT_TOS']) 

    pixella_not_minor = handle_user_input(TEXT_DICT['PROMPTS']['PIXELLA_NOT_MINOR'], TEXT_DICT['ERROR_MESSAGES']['PIXELLA_INCORRECT_NOT_MINOR']) 
    pixella_thanks_code = input(TEXT_DICT['PROMPTS']['PIXELLA_THANKS_CODE']).strip()
    response = create_pixella_user(pixella_token, pixella_username, pixella_TOS, pixella_not_minor, pixella_thanks_code)

    if not response['isSuccess']:
        print(TEXT_DICT['ERROR_MESSAGES']['PIXELLA_API_ERROR'])
        print(response['message'])

        user_input = ''
        while user_input not in [YES, NO]:
            user_input = input(TEXT_DICT['OTHER']['TRY_AGAIN']).strip().lower()
            if user_input in YES:
                return create_new_pixella_account()
            elif user_input in NO:
                break
            else:
                print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])

    return pixella_username, pixella_token, response['isSuccess']

def check_against_regex(input, regex):
    return bool(re.match(regex, input))


def handle_user_regex_inputs(regex, prompt, error_message):
    regex_bool = False
    while not regex_bool:
        user_input = input(prompt).strip()
        regex_bool = check_against_regex(user_input, regex)
        if regex_bool: 
            return user_input
        else:
            print(error_message)
            while user_input not in [YES, NO]:
                user_input = input(TEXT_DICT['OTHER']['TRY_AGAIN']).strip().lower()
                if user_input in NO:
                    print(error_message)
                    print('The app now will be restarted.')
                    restart_prompt()
                elif user_input in YES:
                    return handle_user_regex_inputs(regex, prompt, error_message)
                else:
                    print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])






def handle_user_input(prompt, error_message):
    user_input = ''

    while user_input not in [YES, NO]:
        user_input = input(prompt).strip().lower()
        if user_input in YES:
            return 'yes'
        elif user_input in NO:
            print(error_message)
            user_input = input(TEXT_DICT['OTHER']['TRY_AGAIN']).strip().lower()
            if user_input in NO:
                print(error_message)
                print('The app now will be restarted.')
                restart_prompt()
            elif user_input in YES:
                return handle_user_input(prompt, error_message)
        else:
            print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])

def provide_pixella_details():
    pixella_token = input(TEXT_DICT['PROMPTS']['PIXELLA_EXISTING_TOKEN']).strip()
    pixella_username = input(TEXT_DICT['PROMPTS']['PIXELLA_EXISTING_USERNAME']).strip()

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
        user_input = input(TEXT_DICT['PROMPTS']['RESTART']).strip()

        if user_input == '1':
            #clear()
            start_app()
        elif user_input == '2':
            sys.exit(TEXT_DICT['OTHER']['CLOSING_APP'])
        else:
            #clear()
            print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])


def start_app():
    
    if not FILE_EXISTS:
        user_input = input(TEXT_DICT['OTHER']['NO_ENV_FILE']).strip().lower()
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
                    restart_prompt(TEXT_DICT['ERROR_MESSAGES']['PIXELLA_INFO_NOT_PROVIDED'])
            else:
                restart_prompt(TEXT_DICT['ERROR_MESSAGES']['TOGGL_INFO_NOT_PROVIDED'])
                # user declines to provide information
        else:
            restart_prompt(TEXT_DICT['ERROR_MESSAGES']['GENERAL_INFO_NOT_PROVIDED'])

    # FILE EXISTS
    else:
        pass

#clear()
print(TEXT_DICT['OTHER']['WELCOME'])
start_app()
