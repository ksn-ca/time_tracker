# Purpose
This program posts your time entries from Toggl Track to Pixella so you can visualize your progress just like commits in GitHub.

## Requirements
- An account with Toggl Track and an API key
- Install packages from setup.py 

## Overview
This is the 2.0 version of the app! You can now interact with the app through the console by answering basic prompts. 

Things you can now do:
- Create a .env file with your Toggl and Pixella information (it will be stored locally on your device!)
- Create a Pixella account if you don't have one
- Create Pixella graphs
- Sync your Toggl data to Pixella (NOTE: your Toggl project name MUST be the same as the Pixella graph name for them to sync)
- Sync your .csv file from Toggl to Pixella
- Delete your Pixella graphs
- Delete your Pixella account (NOTE: this will also delete the .env file)

## Important notes
- This app interacts ONLY with official Toggl Track and Pixella APIs
- Your API keys are stored locally in the .env file
- You must know your Toggl API key because there's no way to create a Toggl account other than through the official website

### Toggl API Key
This is how you can find your Toggl API key:
1. Go to https://track.toggl.com/
2. Click "Profile"
3. Scroll to the bottom, you should find "API Token"
4. Click "click to reveal" and copy the key

Additionally, here's the official Toggl page for this: https://support.toggl.com/en/articles/3116844-where-is-my-api-key-located

### .env file
You must have a .env file in the project folder for this app to function. 
This is how the app can get your Toggl data and send it to Pixella.
There's no need to create one yourself, the app will prompt you to create it.
You may create it yourself if you wish.
This is what it must look like:

```
PIXELLA_TOKEN=YOURPIXELLATOKEN
PIXELLA_USERNAME=YOURUSERNAME
TOGGL_WORKSPACE_ID=YOURWORKSPACEID
TOGGL_API_TOKEN=YOURTOGGLTOKEN
```

### .csv file
CSV file can be downloaded from the Toggl website
1. Go to your workspace
2. Click "Settings" at the bottom left-hand corner
3. Click "Data Export"
4. At the bottom, under "Time Entries", choose the year and click "Export time entries"

Once you have the file, add it to the "csv" folder and run the app. You will find the option to sync the file under the "Sync Toggl and Pixella" prompt.

## TODO
1. Documentation
2. Tests
3. Cron job? to run every day
