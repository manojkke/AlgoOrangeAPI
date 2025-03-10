from fastapi import logger
from app.domain.interfaces import Agent
from app.infrastructure.services.calendar.calendar_service import CalendarService
import re
from datetime import datetime, timedelta
import groq  # Groq's API
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = 'path/to/service_account.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

class CalendarAgent(Agent):
    def __init__(self, calendar_service: CalendarService):
        self.calendar_service = calendar_service
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    async def handle_query(self, userChatQuery: str, userChatHistory: str) -> str:
        # Determine the type of query (schedule, get, cancel, reschedule)
        if "schedule" in userChatQuery.lower():
            return await self.schedule_event(userChatQuery)
        elif "get" in userChatQuery.lower():
            return await self.get_events(userChatQuery)
        elif "cancel" in userChatQuery.lower():
            return await self.cancel_event(userChatQuery)
        elif "reschedule" in userChatQuery.lower():
            return await self.reschedule_event(userChatQuery)
        else:
            return "Unknown query type."

    async def schedule_event(self, userChatQuery: str) -> str:
        meeting_details = self.parse_meeting_details(userChatQuery)
        if not meeting_details:
            return "Could not parse meeting details from the query."

        result = self.create_calendar_event(
            summary=meeting_details['title'],
            start_time=meeting_details['start_date'],
            end_time=meeting_details['end_date'],
            description=meeting_details['description']
        )
        return result

    def create_calendar_event(self, summary, start_time, end_time, description=""):
        """Creates a new event in Google Calendar."""
        try:
            creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
            service = build("calendar", "v3", credentials=creds)
            event = {
                'summary': summary,
                'location': '1234 Street, City, Country',
                'description': description,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'America/New_York',
                },
                'reminders': {
                    'useDefault': True,
                },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            logger.info(f"Event created: {event.get('htmlLink')}")
            return {"status": "success", "event_link": event.get('htmlLink')}
        except Exception as e:
            logger.error(f"Error creating event: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def get_events(self, userChatQuery: str) -> str:
        # Extract date range from the query
        from_date_pattern = re.search(r'from_date: (.+)', userChatQuery)
        to_date_pattern = re.search(r'to_date: (.+)', userChatQuery)
        from_date = from_date_pattern.group(1) if from_date_pattern else datetime.now().isoformat()
        to_date = to_date_pattern.group(1) if to_date_pattern else (datetime.now() + timedelta(days=1)).isoformat()

        result = self.calendar_service.get_events(from_date, to_date)
        return result

    async def cancel_event(self, userChatQuery: str) -> str:
        event_id_pattern = re.search(r'event_id: (.+)', userChatQuery)
        event_id = event_id_pattern.group(1) if event_id_pattern else None
        if not event_id:
            return "Could not parse event ID from the query."

        result = self.calendar_service.cancel_event(event_id)
        return result

    async def reschedule_event(self, userChatQuery: str) -> str:
        event_id_pattern = re.search(r'event_id: (.+)', userChatQuery)
        start_date_pattern = re.search(r'start_date: (.+)', userChatQuery)
        end_date_pattern = re.search(r'end_date: (.+)', userChatQuery)
        timezone_pattern = re.search(r'timezone: (.+)', userChatQuery)

        event_id = event_id_pattern.group(1) if event_id_pattern else None
        start_date = start_date_pattern.group(1) if start_date_pattern else None
        end_date = end_date_pattern.group(1) if end_date_pattern else None
        timezone = timezone_pattern.group(1) if timezone_pattern else "UTC"

        if not event_id or not start_date or not end_date:
            return "Could not parse event details from the query."

        result = self.calendar_service.reschedule_event(event_id, start_date, end_date, timezone)
        return result

    def parse_meeting_details(self, userChatQuery: str) -> dict:
        """Extracts meeting details from a message using Groq's API."""
        try:
            response = groq.Completion.create(
                engine="text-davinci-003",
                prompt=f"Extract meeting details from the following query: {userChatQuery}",
                max_tokens=150
            )
            details = response.choices[0].text.strip()
            # Assuming the LLM returns a JSON-like string
            meeting_details = eval(details)
            return meeting_details
        except Exception as e:
            return None
