import groq  # Assuming you are using Groq's API
from app.application.agents.medical_agent import MedicalAgent
from app.application.agents.student_agent import StudentAgent
from app.application.agents.social_media_agent import SocialMediaAgent
from app.application.agents.calendar_agent import CalendarAgent
from app.core.di import Container
import os

class Orchestrator:
    def __init__(self, userChatQuery: str, chatHistory: str):
        self.userChatQuery = userChatQuery
        self.chatHistory = chatHistory
    

    async def route_query(self, userChatQuery: str, chatHistory: str):
        # Initialize Groq client
        client = groq.Client(api_key="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")   # Replace with your actual API key

        # Query Groq LLM to determine which agent to call
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Groq-supported model
            messages=[
                {"role": "system", "content": "You are an AI that routes queries to specialized agents."},
                {"role": "user", "content": f"Query: {userChatQuery}. Chat History: {chatHistory}. The options are: "
                                             "student (specializes in educational and academic queries), "
                                             "medical (specializes in health-related queries), "
                                             "social_media (specializes in social media management), "
                                             "calendar (specializes in scheduling and calendar management). "
                                             "Return only the agent name (e.g., 'student', 'medical')."}
            ],
            max_tokens=10
        )
        print(response)
        # Extract decision from response
        decision = response.choices[0].message.content.strip().lower()
        print(decision)

        # Map decision to the corresponding agent
        agent_mapping = {
            "medical": MedicalAgent,
            "student": lambda: StudentAgent(Container.student_service(), Container.db_session()),  # Added db_session
            "social_media": SocialMediaAgent,
            "calendar": lambda: CalendarAgent(Container.calendar_service()),
        }
        print(agent_mapping)

        agent_class = agent_mapping.get(decision)
        print(agent_class)

        if not agent_class:
            return "Agent not found."

        agent = agent_class()
         # Call handle_query with appropriate number of arguments
        if decision == "student":
            return await agent.handle_query(userChatQuery, chatHistory, Container.db_session())
        else:
            return await agent.handle_query(userChatQuery, chatHistory)