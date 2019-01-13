from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# File copied mercilessly from
# https://developers.google.com/calendar/quickstart/python

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        # If needed, the credentials.json file needs to be obtained
        # in https://console.developers.google.com/apis/credentials?project=gcalreports-1547134468896&authuser=0
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    today = (datetime.datetime.utcnow().date()).isoformat() + 'T00:00:00.000Z' # 'Z' indicates UTC time
    yesterday = (datetime.datetime.utcnow().date() - datetime.timedelta(1)).isoformat() + 'T00:00:00.000Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=yesterday, timeMax=today,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        # start = event['start'].get('dateTime', event['start'].get('date'))
        # print(start, event['summary'])
        print(event['summary'])

if __name__ == '__main__':
    main()
