# Google calendar class

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

class GCalendar:
    # Setup the Calendar API
    def setup (self):
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('calendar', 'v3', http=creds.authorize(Http()))


    # Call the Calendar API
    def callapi (self):
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])



# event = {
#   'summary': 'Google I/O 2015',
#   #'location': '800 Howard St., San Francisco, CA 94103',
#   'description': 'A chance to hear more about Google\'s developer products.',
#   'start': {
#     'dateTime': '2018-07-28T09:00:00-07:00',
#     #'timeZone': 'America/Los_Angeles',
#   },
#   'end': {
#     'dateTime': '2018-07-28T17:00:00-07:00',
#     #'timeZone': 'America/Los_Angeles',
#   },
#   # 'recurrence': [
#   #   'RRULE:FREQ=DAILY;COUNT=2'
#   # ],
#   # 'attendees': [
#   #   {'email': 'lpage@example.com'},
#   #   {'email': 'sbrin@example.com'},
#   # ],
#   'reminders': {
#     'useDefault': False,
#     'overrides': [
#       # {'method': 'email', 'minutes': 24 * 60},
#       # {'method': 'popup', 'minutes': 10},
#     ],
#   },
# }
# event = self.service.events().insert(calendarId='primary', body=event).execute()
# print('Event created: %s' % (event.get('htmlLink')))
