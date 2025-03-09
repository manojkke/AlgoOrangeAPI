from app.application.agents.medical_agent import MedicalAgent
from app.application.agents.student_agent import StudentAgent
from app.application.agents.social_media_agent import SocialMediaAgent
from app.application.agents.calendar_agent import CalendarAgent
from app.core.di import Container


class Orchestrator:
    def __init__(self, userChatQuery: str):
        self.userChatQuery = userChatQuery

    async def route_query(self, query: str):
        if self.userChatQuery == "medical":
            agent = MedicalAgent()
        elif self.userChatQuery == "student":
            agent = StudentAgent()
        elif self.userChatQuery == "social_media":
            agent = SocialMediaAgent()
        elif self.userChatQuery == "calendar":
            agent = CalendarAgent(Container.calendar_service())
        else:
            return "Agent not found."

        return await agent.handle_query(query)
