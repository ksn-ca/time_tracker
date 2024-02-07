from datetime import datetime, timedelta
from pixella import *
from toggl import check_toggl, get_toggl_projects
from toggl_historic import post_csv_to_pixella
import os
import sys
import re
from text_dict import TEXT_DICT
import numpy as np

# OTHER
TODAY = datetime.now().date()
YESTERDAY = datetime.now().date() - timedelta(days=1)
SINCE = datetime.strptime("20231206", "%Y%m%d").date()
TEST_DAY = datetime.strptime("20231206", "%Y%m%d").date()
PIXELLA_USERNAME_REGEX = r'[a-z][a-z0-9-]{1,32}'
PIXELLA_TOKEN_REGEX = r'[ -~]{8,128}'


API_NAMES = {
    "pixella": {"token": "PIXELLA_TOKEN", "name": "PIXELLA_USERNAME"},
    "toggl": {"token": "TOGGL_API_TOKEN", "workspace": "TOGGL_WORKSPACE_ID"},
}

ENV_FILE = "./project/.env"

YES = ["y", "yes"]
NO = ["n", "no"]
YES_AND_NO = list(np.append(YES, NO))

CSV_FILE_FOLDER = "./project/csv/"

def str_range(start, end):
    return [str(i) for i in range(start, end)]

# post_to_pixella_yesterday(YESTERDAY)
# post_to_pixella_since(SINCE)
# def #clear(): os.system('cls' if os.name=='nt' else 'clear')

def edit_env_file(key, new_val):
    pass


def user_input_cs(prompt):
    return input(prompt).strip()

def input_modified(prompt):
    return input(prompt).strip().lower()

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
    while user_input not in str_range(1,3):
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
    pixella_thanks_code = '' # input(TEXT_DICT['PROMPTS']['PIXELLA_THANKS_CODE']).strip()
    response = create_pixella_user(pixella_token, pixella_username, pixella_TOS, pixella_not_minor, pixella_thanks_code)

    if not response['isSuccess']:
        print(TEXT_DICT['ERROR_MESSAGES']['PIXELLA_API_ERROR'])
        print(response['message'])

        user_input = ''
        while user_input not in YES_AND_NO:
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
            while user_input not in YES_AND_NO:
                user_input = input(TEXT_DICT['OTHER']['TRY_AGAIN']).strip().lower()
                if user_input in NO:
                    print(error_message)
                    restart_prompt()
                elif user_input in YES:
                    return handle_user_regex_inputs(regex, prompt, error_message)
                else:
                    print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])


def handle_user_input(prompt, error_message):
    user_input = ''

    while user_input not in YES_AND_NO:
        user_input = input(prompt).strip().lower()
        if user_input in YES:
            return 'yes'
        elif user_input in NO:
            print(error_message)
            user_input = input(TEXT_DICT['OTHER']['TRY_AGAIN']).strip().lower()
            if user_input in NO:
                print(error_message)
                restart_prompt()
            elif user_input in YES:
                return handle_user_input(prompt, error_message)
        else:
            print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])

def provide_pixella_details():
    success = False
    while not success:
        pixella_token = input(TEXT_DICT['PROMPTS']['PIXELLA_EXISTING_TOKEN']).strip()
        pixella_username = input(TEXT_DICT['PROMPTS']['PIXELLA_EXISTING_USERNAME']).strip()
        
        success = check_pixella_user(pixella_username, pixella_token)
        if not success:
            print(TEXT_DICT['ERROR_MESSAGES']['PIXELLA_USER_INCORRECT'])
    return pixella_username, pixella_token, success


def create_env_text(toggl_token, toggl_workspace_id, pixella_token, pixella_username):
    text = f"{API_NAMES['pixella']['token']}={pixella_token}\n"
    text += f"{API_NAMES['pixella']['name']}={pixella_username}\n"
    text += f"{API_NAMES['toggl']['token']}={toggl_token}\n"
    text += f"{API_NAMES['toggl']['workspace']}={toggl_workspace_id}"
    return text

def create_toggl_env_text(toggl_token, toggl_workspace_id):
    text = f"{API_NAMES['toggl']['token']}={toggl_token}\n"
    text += f"{API_NAMES['toggl']['workspace']}={toggl_workspace_id}\n"
    return text

def create_pixella_env_text(pixella_token, pixella_username):
    text = f"{API_NAMES['pixella']['token']}={pixella_token}\n"
    text += f"{API_NAMES['pixella']['name']}={pixella_username}\n"
    return text

def restart_prompt(prompt=''):
    #clear()
    print(prompt)
    user_input = ''
    while user_input not in str_range(1,3):
        user_input = input(TEXT_DICT['PROMPTS']['RESTART']).strip()

        if user_input == '1':
            #clear()
            start_app()
        elif user_input == '2':
            sys.exit(TEXT_DICT['OTHER']['CLOSING_APP'])
        else:
            #clear()
            print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])


def sync_accounts():
    user_input = ''

    while user_input not in str_range(1,5):
        user_input = input_modified(TEXT_DICT['PROMPTS']['SYNC'])

        if user_input == '1':
            post_to_pixella_yesterday(TODAY)
        elif user_input == '2':
            post_to_pixella_yesterday(YESTERDAY)
        elif user_input == '3':
            cont = True
            while cont:
                date_from = handle_user_date_entry(TEXT_DICT['PROMPTS']['SYNC_FROM_DATE'])
                date_to = handle_user_date_entry(TEXT_DICT['PROMPTS']['SYNC_TO_DATE'])
                try:
                    post_to_pixella_since(date_from, date_to)
                    cont = False
                except:
                    pass

        elif user_input == '4':
            file_path = ''
            while os.path.isfile(file_path) == False:
                file_name = user_input_cs(TEXT_DICT['PROMPTS']['SYNC_FILE'])
                file_path = CSV_FILE_FOLDER + file_name

                if file_name.lower() == 'stop':
                    break

                if not file_path.endswith('.csv'):
                    file_path += '.csv'

                if os.path.isfile(file_path):
                    print(TEXT_DICT['NOTIFICATIONS']['PLZ_WAIT'])
                    post_csv_to_pixella(file_path)
                else:
                    print(f'Sorry, no file with the name {file_name} was found.\nPlease try again or enter "stop."')
        else:
            print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])

    start_app()

def valid_date(datestring):
    try:
        date = datetime.strptime(datestring, '%Y-%m-%d')
        return date.date()
    except ValueError:
        return None
    except:
        return None

def handle_user_date_entry(prompt):
    user_date = None
    while user_date == None:
        user_date = input_modified(prompt)
        user_date = valid_date(user_date)
        if user_date == None:
            print('The date must be in format YYYY-MM-DD. Please try again.')
        else:
            return user_date


def get_japanese_color(prompt):
    switch = {
        'green': 'shibafu',
        'red': 'momiji',
        'blue': 'sora',
        'yellow': 'ichou',
        'purple': 'ajisai',
        'black': 'kuro'
    }

    user_input = ''
    while switch.get(user_input) == None:
        user_input = input_modified(prompt)
    
    return switch.get(user_input)
    
def create_pixella_graphs():
    cont = True
    while cont:

        graphs = get_pixella_graphs()
        toggl_projects = get_toggl_projects()
        print(f'You have the following graphs in Pixella: {", ".join(graphs.keys())}')
        print(f'You have the following projects in Toggl: {", ".join(toggl_projects.values())}')
        pixella_graph_name = user_input_cs(TEXT_DICT['PROMPTS']['PIXELLA_GRAPH_NAME'])
        pixella_graph_id = pixella_graph_name.lower()
        pixella_graph_color = get_japanese_color(TEXT_DICT['PROMPTS']['PIXELLA_GRAPH_COLOR'])
        pixella_graph_timezone = 'America/Montreal'

        response = create_new_graph(pixella_graph_id, pixella_graph_name, color=pixella_graph_color)

        print(f'Graph with name {pixella_graph_name} has been successfully created.')

        user_input = ''
        while user_input not in YES_AND_NO:
            user_input = input_modified('Would you like to create another graph?\nEnter yes or no:   ')
            if user_input in YES:
                pass
            elif user_input in NO: 
                cont = False
            else:
                print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])


    start_app()


def delete_pixella_graph():
    
    graphs = get_pixella_graphs()
    if len(graphs) == 0:
        print(TEXT_DICT['ERROR_MESSAGES']['PIXELLA_NO_GRAPHS'])
        start_app()
    else:
        print(f'You have the following graphs: {", ".join(graphs.keys())}')
        user_input = user_input_cs(TEXT_DICT['PROMPTS']['PIXELLA_DELETE_GRAPH'])
        if user_input in graphs.keys():
            graph_to_delete = user_input
            while user_input not in YES_AND_NO:
                user_input = input_modified(f'This action cannot be undone. All your information in pixella regarding this graph will be deleted.\nAre you sure you want to delete graph "{user_input}"?\nEnter yes or no:   ')
                if user_input in YES:
                    delete_pixella_graph_by_id(graphs[graph_to_delete])
                    print(f'Your graph {graph_to_delete} has been successfully deleted.')
                    delete_another_graph_prompt()
                elif user_input in NO:
                    delete_another_graph_prompt()
                else:
                    print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])
        else:
            print(f"There is no graph with the name {user_input}. Please try again.")
            delete_pixella_graph()



def delete_another_graph_prompt():
    user_input = ''
    while user_input not in str_range(1,3):
        user_input = input_modified(TEXT_DICT['PROMPTS']['PIXELLA_DELETE_ANOTHER_GRAPH'])
        if user_input == '1':
            delete_pixella_graph()
        elif user_input == '2':
            start_app()
        else:
            print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])

def delete_user_prompt():
    user_input = ''
    while user_input not in YES_AND_NO:
        user_input = input_modified(TEXT_DICT['PROMPTS']['PIXELLA_DELETE_USER'])

        if user_input in YES:
            success = delete_pixella_user_env()
            if success:
                os.remove(ENV_FILE)
                print(TEXT_DICT['NOTIFICATIONS']['PIXELLA_USER_DELETED'])
        elif user_input in NO:
            start_app()
        else:
            print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])




def start_app():
    if not os.path.isfile(ENV_FILE):
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
                        print(TEXT_DICT['NOTIFICATIONS']['FILE_CREATED'])
                        start_app()
                else:
                    restart_prompt(TEXT_DICT['ERROR_MESSAGES']['PIXELLA_INFO_NOT_PROVIDED'])
            else:
                restart_prompt(TEXT_DICT['ERROR_MESSAGES']['TOGGL_INFO_NOT_PROVIDED'])
                # user declines to provide information
        else:
            restart_prompt(TEXT_DICT['ERROR_MESSAGES']['GENERAL_INFO_NOT_PROVIDED'])

    # FILE EXISTS
    else:
        no_graphs = len(get_pixella_graphs()) == 0

        if no_graphs:
            user_input = ''
            while user_input not in YES_AND_NO:
                user_input = input_modified(TEXT_DICT['PROMPTS']['PIXELLA_CREATE_GRAPH'])
                if user_input in YES:
                    create_pixella_graphs()
                elif user_input in NO:
                    restart_prompt(TEXT_DICT['ERROR_MESSAGES']['PIXELLA_NO_WANT_GRAPH'])
                else:
                    print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])


        user_input = ''
        while user_input not in str_range(1,5):
            user_input = input_modified(TEXT_DICT['PROMPTS']['MAIN_APP'])
            if user_input == '1':
                sync_accounts()
            elif user_input == '2':
                create_pixella_graphs()
            elif user_input == '3':
                delete_pixella_graph()
            elif user_input == '4':
                delete_user_prompt()
            else:
                print(TEXT_DICT['NOTIFICATIONS']['INPUT_NOT_SUPPORTED'])
        

#clear()
print(TEXT_DICT['OTHER']['WELCOME'])

start_app()
