import datetime
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from httpx import HTTPError
from utils import speak  # Updated import


# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/gmail.modify']

# South African timezone
SA_TIMEZONE = 'Africa/Johannesburg'

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_events():
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    # Get the current time in UTC
    now = datetime.datetime.now(datetime.timezone.utc)
    # Convert to South African time
    sa_tz = datetime.timezone(datetime.timedelta(hours=2))  # UTC+2 for South Africa
    now_sa = now.astimezone(sa_tz)
    
    # Set start and end of day in South African time
    start_of_day = now_sa.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    end_of_day = now_sa.replace(hour=23, minute=59, second=59, microsecond=999999).isoformat()

    speak('Getting today\'s events')

    calendar_list = service.calendarList().list().execute()
    events = []

    for calendar_list_entry in calendar_list['items']:
        calendar_id = calendar_list_entry['id']
        events_result = service.events().list(calendarId=calendar_id, timeMin=start_of_day, timeMax=end_of_day,
                                              maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events.extend(events_result.get('items', []))

    if not events:
        speak('No events found for today.')
        return "No events found for today."
    else:
        event_summaries = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            summary = event['summary']
            event_summary = f"At {start}, you have {summary}"
            print(event_summary)
            event_summaries.append(event_summary)
        return "\n".join(event_summaries)

def schedule():
    return get_events()

def get_calendar_service():
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(summary, location, description, start_time, end_time, attendees=None):
    try:
        service = get_calendar_service()
        
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': SA_TIMEZONE,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': SA_TIMEZONE,
            },
        }

        if attendees:
            event['attendees'] = [{'email': attendee} for attendee in attendees]

        event = service.events().insert(calendarId='primary', body=event).execute()
        return f'Event created: {event.get("htmlLink")}'

    except HTTPError as error:
        return f'An error occurred: {error}'