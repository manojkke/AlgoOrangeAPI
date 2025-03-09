from app.application.agents.medical_agent import MedicalAgent
from app.application.agents.student_agent import StudentAgent
from app.application.agents.social_media_agent import SocialMediaAgent
from app.application.agents.calendar_agent import CalendarAgent


class Orchestrator:
    def __init__(self, agent: str):
        self.agent = agent

    async def route_query(self, query: str):
        if self.agent == "medical":
            agent = MedicalAgent()
        elif self.agent == "student":
            agent = StudentAgent()
        elif self.agent == "social_media":
            agent = SocialMediaAgent()
        elif self.agent == "calendar":
            agent = CalendarAgent()
        else:
            return "Agent not found."

        return await agent.handle_query(query)
