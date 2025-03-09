from abc import ABC, abstractmethod


class CalendarService(ABC):
    @abstractmethod
    def schedule_event(self, summary: str, location: str, description: str, start_date: str, end_date: str, reminders: bool, timezone: str, attendees: list):
        pass

    @abstractmethod
    def get_events(self, from_date, to_date, event_type):
        pass

    @abstractmethod
    def cancel_event(self, event_details):
        pass

    @abstractmethod
    def reschedule_event(self, event_details):
        pass
