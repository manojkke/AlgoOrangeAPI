from .calendar_service import CalendarService


class MicrosoftCalendar(CalendarService):
    def __init__(self):
        # Initialize Microsoft Calendar API client
        pass

    def schedule_event(self, event_details):
        event = {
            "summary": "test meeting",
            "reminders": {"useDefault": True}
        }
        # event = service.events().insert(calendarId="primary", sendNotifications=True,
        #                                 body=event, conferenceDataVersion=1).execute()
        # Implement Google Calendar scheduling logic here
        # Implement Microsoft Calendar scheduling logic here
        return "Event scheduled on Microsoft Calendar"
