TEXT_DICT = {
    'ERROR_MESSAGES': {
        'PIXELLA_INFO_NOT_PROVIDED':
        'Sorry, but without information about your Pixella account, this app is unable to fulfill its function.',
        'TOGGL_INFO_NOT_PROVIDED':
        'Sorry, but without correct information about your Toggl account, this app is unable to fulfill its function.',
        'GENERAL_INFO_NOT_PROVIDED':
        'Sorry, but without information about your accounts, this app is unable to fulfill its function.',
        'PIXELLA_INCORRECT_USERNAME':
        'Sorry. The username must follow the following pattern: [a-z][a-z0-9-]{1,32}.',
        'PIXELLA_INCORRECT_TOKEN':
        'Sorry. The token must follow the following pattern: [ -~]{8,128}.',
        'PIXELLA_INCORRECT_NOT_MINOR':
        'Sorry, but minors (or minors without parental consent) are not allowed to use Pixella.',
        'PIXELLA_INCCORECT_TOS':
        'Sorry, without agreeing to terms of service, this app is unable to create an account for you.',
        'PIXELLA_API_ERROR':
        'There was an error while making your account. The error from Pixella is:',
        'TOGGL_API_ERROR':
        "Please try again or enter 'stop'.\nToggl API token:   ",
        'PIXELLA_NO_WANT_GRAPH':
        'Sorry, you need to have Pixella graphs for this app to function.',
        'PIXELLA_NO_GRAPHS':
        'You have no graphs.',
        'PIXELLA_USER_INCORRECT':
        'This user or token are incorrent. Please try again.'
    },
    'PROMPTS': {
        'PIXELLA_USERNAME':
        'The username must follow the following pattern: [a-z][a-z0-9-]{1,32}. Enter desired username:   ',
        'PIXELLA_TOKEN':
        'You must create your own token.\nA token string used to authenticate as a user to be created. \nThe token string is hashed and saved. Validation rule: [ -~]{8,128}.\nEnter desired token:   ',
        'PIXELLA_TOS':
        'Specify yes or no whether you agree to the terms of service. Enter yes or no:   ',
        'PIXELLA_NOT_MINOR':
        'Specify yes or no as to whether you are not a minor or if you are a minor and you have the parental consent of using this service. Enter yes or no:   ',
        'PIXELLA_THANKS_CODE':
        'If you are a Pixella Patreon supporter, then please enter the thanks code. Otherwise, click enter:   ',
        'RESTART':
        'Would you like to:\n1. Restart the app\n2. Close the app\nEnter 1 or 2:   ',
        'TOGGL_API':
        "Please provide details of your Toggl account.\nToggl API token:   ",
        'PIXELLA_CHOICE_PROMPT':
        "Please choose the option:\n1. Enter Pixella details manually (if you already have an account).\n2. Create Pixella account now.\nEnter either 1 or 2:   ",
        'PIXELLA_EXISTING_TOKEN':
        'Please provide details of your Pixella account.\nPixella API token:   ',
        'PIXELLA_EXISTING_USERNAME':
        'Pixella username:   ',
        'MAIN_APP':
        'What would you like to do?\n1. Sync Toggl and Pixella \n2. Create new Pixella graphs \n3. Delete Pixella graphs \n4. Delete your Pixella account \n5.Close the app \nEnter a number:   ',
        'PIXELLA_CREATE_GRAPH':
        'You currently have no Pixella graphs. You need graphs in order for this app to function.\nWould you like to create one?\nEnter yes or no:   ',
        'PIXELLA_DELETE_USER':
        'This action cannot be undone. Your Pixella account will be deleted. Your .env file will be deleted as well as the app requires both Pixella and Toggl to function.\nAre you sure you want to delete your account?\nEnter yes or no:   ',
        'PIXELLA_DELETE_ANOTHER_GRAPH':
        'Would you like to:\n1. Delete another graph\n2. Return to main menu\nEnter a number:   ',
        'PIXELLA_DELETE_GRAPH':
        'Which graph do you want to delete? Enter a name:   ',
        'PIXELLA_GRAPH_NAME':
        'Enter a name for your graph. For Toggl to successfully sync with Pixella, the name of the graph MUST match corresponding Toggl Project name.\nEnter graph name:   ',
        'PIXELLA_GRAPH_COLOR':
        'Which colour do you want your graph to be? Choose green, red, blue, yellow, purple or black:   ',
        'SYNC':
        'Choose an option to sync Toggl and Pixella.\n1. Sync for today only\n2. Sync for yesterday only\n3. Sync from DATE to DATE\n4. Sync .csv file \nEnter a number:   ',
        'SYNC_FROM_DATE':
        'Enter a FROM date in format YYYY-MM-DD:   ',
        'SYNC_TO_DATE':
        'Enter a TO date in format YYYY-MM-DD:   ',
        'SYNC_FILE':
        'You must have a Toggl exported file in csv folder of this project for this function to run.\nPlease provide the name of the file:   ',
        'PIXELLA_CREATE_ANOTHER_GRAPH':
        'Would you like to create another graph?\nEnter yes or no:   '
    },
    'NOTIFICATIONS': {
        'INPUT_NOT_SUPPORTED': 'This input is not supported.',
        'RESTART_APP': 'The app now will be restarted.',
        'FILE_CREATED':
        'Your information about Pixella and Toggl was successfully saved. (Locally of course!)',
        'PIXELLA_USER_DELETED':
        'Your account has been deleted. Your .env file has been deleted.',
        'PLZ_WAIT': 'Please wait as it may take a while.'
    },
    'OTHER': {
        'CLOSING_APP':
        'Sorry to see you go. Come back later!',
        'WELCOME':
        "Welcome to Toggl to Pixella app!",
        'TRY_AGAIN':
        'Would you like to try again? Enter yes or no:   ',
        'NO_ENV_FILE':
        "There's no information about your Toggl or Pixella accounts.\nWould you like to add it?\nEnter yes or no:   "
    }
}
