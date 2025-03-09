from dependency_injector import containers, providers
# Ensure the correct import path
from app.infrastructure.db.mongo_db import MongoDB
# Ensure the correct import path
from app.infrastructure.db.sqlite_db import SQLite
from app.core.config import Settings
from app.infrastructure.services.calendar.google_calendar import GoogleCalendar
from app.infrastructure.services.calendar.microsoft_calendar import MicrosoftCalendar
from app.infrastructure.services.calendar.calendar_service import CalendarService
from app.application.agents.calendar_agent import CalendarAgent


class Container(containers.DeclarativeContainer):
    config = providers.Singleton(Settings)
    database = providers.Factory(MongoDB)  # Dynamically switch based on config
    # Inject MicrosoftCalendar for CalendarService
    calendar_service = providers.Factory(MicrosoftCalendar)
    # Provide CalendarService to CalendarAgent
    calendar_agent = providers.Factory(
        CalendarAgent, calendar_service=calendar_service)
