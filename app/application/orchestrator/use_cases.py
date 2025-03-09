import openai
from app.application.agents.medical_agent import MedicalAgent
from app.application.agents.student_agent import StudentAgent
from app.application.agents.social_media_agent import SocialMediaAgent
from app.application.agents.calendar_agent import CalendarAgent
from app.core.di import Container


class Orchestrator:
    def __init__(self, userChatQuery: str, chatHistory: str):
        self.userChatQuery = userChatQuery
        self.chatHistory = chatHistory

    async def route_query(self, userChatQuery: str):
        # Send the query to OpenAI LLM to decide which agent to call
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=(
                "Based on the following user query and chat history, determine the most appropriate agent to handle it: "
                f"Query: {userChatQuery}. Chat History: {self.chatHistory}. The options are: "
                "medical (specializes in healthcare-related queries), "
                "student (specializes in educational and academic queries), "
                "social_media (specializes in social media-related queries), "
                "calendar (specializes in scheduling and calendar management queries)."
            ),
            max_tokens=10
        )
        decision = response.choices[0].text.strip().lower()

        if decision == "medical":
            agent = MedicalAgent()
        elif decision == "student":
            agent = StudentAgent()
        elif decision == "social_media":
            agent = SocialMediaAgent()
        elif decision == "calendar":
            agent = CalendarAgent(Container.calendar_service())
        else:
            return "Agent not found."

        return await agent.handle_query(userChatQuery)
