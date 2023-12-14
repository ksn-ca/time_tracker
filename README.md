# Purpose
This program posts your time entries from Toggl Track to Pixella so you can visualize your progress just like commits in GitHub.

## Requirements
- An account with Toggl Track and API key
- An account from Pixella and API key
- .env file with defined environment variables
- .csv file if you want to mass upload Toggl data

## .env file
You must create .env file in the project folder. This is how it must look like:

```
PIXELLA_TOKEN=YOURPIXELLATOKEN
PIXELLA_USERNAME=YOURUSERNAME
TOGGL_WORKSPACE_ID=YOURWORKSPACEID
TOGGL_API_TOKEN=YOURTOGGLTOKEN
```

## .csv file
CSV file can be downloaded from the Toggl website. 
1. Go to your workspace 
2. Click "Settings" at the bottom left hand corner
3. Click "Data Export"
4. At the bottom, under "Time Entries", choose the year and click "Export time entries"

Once you have the file, add it to cvs folder and edit the toggl_historic.py FILE_PATH variable to include your file.
Run the toggl_historic.py file

## TODO
1. Function to create Pixella account
2. Interact with the user through console (ask for keys api and store them)
3. Cron job? to run everyday
