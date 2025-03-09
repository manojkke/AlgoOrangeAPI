from abc import ABC, abstractmethod


class CalendarService(ABC):
    @abstractmethod
    def schedule_event(self, event_details):
        pass
