from __future__ import print_function

from datetime import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CALENDAR_ID = 'umbc.edu_dqqvhth689kisqrvnp2pf85614@group.calendar.google.com' # modify this if the ID ever changes


def generateToken():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def getEvents(start_date, end_date, name, creds):
    workdays = []

    try:
        start_date = datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.strptime(end_date, "%m/%d/%Y")

        time_min = start_date.isoformat()  + 'Z'
        time_max = end_date.isoformat()  + 'Z'

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=time_min, 
                                              timeMax = time_max, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            if event['summary'].lower() == name.lower():    
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                
                start_dt = datetime.fromisoformat(start)
                end_dt = datetime.fromisoformat(end)

                formatted_date = start_dt.strftime("%m/%d/%Y")
                formatted_start = start_dt.strftime("%I:%M%p")
                formatted_end = end_dt.strftime("%I:%M%p")

                if formatted_start[0] == '0':
                    formatted_start = formatted_start[1:]

                if formatted_end[0] == '0':
                    formatted_end = formatted_end[1:]

                workdays.append([formatted_date, formatted_start, formatted_end])




    except HttpError as error:
        print('An error occurred: %s' % error)

    return workdays