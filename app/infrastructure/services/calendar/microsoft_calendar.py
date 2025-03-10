from google.oauth2 import service_account
from googleapiclient.discovery import build
from .calendar_service import CalendarService
import os

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/calendar.events"]
SERVICE_ACCOUNT_FILE = os.path.abspath("D:\Algorange Tasks\AlgoOrangeAPI\credentials.json")  # Update the path

class MicrosoftCalendar(CalendarService):
    def __init__(self):
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        self.service = build("calendar", "v3", credentials=creds)

    def schedule_event(self, summary: str, location: str, description: str, start_date: str, end_date: str, reminders: bool, timezone: str, attendees: list):
        try:
            event = {
                'summary': summary,
                'location': location,
                'description': description,
                'start': {
                    'dateTime': start_date,
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_date,
                    'timeZone': timezone,
                },
                'attendees': [{'email': email} for email in attendees],
                'reminders': {
                    'useDefault': reminders,
                },
            }
            self.service.events().insert(calendarId='sachinbfrnd@gmail.com', body=event).execute()
            return "Event scheduled on Google Calendar"
        except Exception as e:
            return f"Exception occurred: {e}"

    def get_events(self, from_date, to_date, event_type=None):
        try:
            events_result = self.service.events().list(
                calendarId='sachinbfrnd@gmail.com', timeMin=from_date, timeMax=to_date, singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])
            return events
        except Exception as e:
            return f"Exception occurred: {e}"

    def cancel_event(self, event_id):
        try:
            self.service.events().delete(calendarId='sachinbfrnd@gmail.com', eventId=event_id).execute()
            return "Event canceled on Google Calendar"
        except Exception as e:
            return f"Exception occurred: {e}"

    def reschedule_event(self, event_id, start_date, end_date, timezone):
        try:
            event = self.service.events().get(calendarId='sachinbfrnd@gmail.com', eventId=event_id).execute()
            event['start']['dateTime'] = start_date
            event['start']['timeZone'] = timezone
            event['end']['dateTime'] = end_date
            event['end']['timeZone'] = timezone
            updated_event = self.service.events().update(calendarId='sachinbfrnd@gmail.com', eventId=event['id'], body=event).execute()
            return "Event rescheduled on Google Calendar"
        except Exception as e:
            return f"Exception occurred: {e}"
