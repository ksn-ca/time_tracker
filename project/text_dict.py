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
        "Please try again or enter 'stop'.\nToggl API token:   "
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
        'PIXELLA_EXISTING_USERNAME': 'Pixella username:   '
    },
    'NOTIFICATIONS': {
        'INPUT_NOT_SUPPORTED': 'This input is not supported.',
        'RESTART_APP': 'The app now will be restarted.',
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
