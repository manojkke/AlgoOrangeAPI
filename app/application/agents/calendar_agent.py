from app.domain.interfaces import Agent
from app.infrastructure.services.calendar.calendar_service import CalendarService


class CalendarAgent(Agent):
    def __init__(self, calendar_service: CalendarService):
        self.calendar_service = calendar_service

    async def handle_query(self, query: str) -> str:
        # Calendar-specific processing here
        result = self.calendar_service.schedule_event(
            query)  # Use schedule_event method

        return result
