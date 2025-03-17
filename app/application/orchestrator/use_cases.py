import groq  # Assuming you are using Groq's API
from app.application.agents.medical_agent import MedicalAgent
from app.application.agents.project_agent import ProjectAgent
from app.application.agents.social_media_agent import SocialMediaAgent
from app.application.agents.calendar_agent import CalendarAgent
from app.application.agents.general_agent import GeneralAgent
from app.core.di import Container
import json

class Orchestrator:
    def __init__(self, userChatQuery: str, chatHistory: str):
        self.userChatQuery = userChatQuery
        self.chatHistory = chatHistory

    async def route_query(self, userChatQuery: str, chatHistory: str):
        # Initialize Groq client
        client = groq.Client(api_key="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")  # Replace with your actual API key

        # Query Groq LLM to determine which agent to call
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Groq-supported model
            messages=[
                {"role": "system", "content": "You are an AI that routes queries to specialized agents."},
                {"role": "user", "content": f"Query: {userChatQuery}. Chat History: {chatHistory}. The options are: "
                                             "project (specializes in projects and bussiness), "
                                             "medical (specializes in health-related queries), "
                                             "social_media (specializes in social media management), "
                                             "calendar (specializes in scheduling and calendar management). "
                                             "general (general advice)."
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
            "project": ProjectAgent,
            "social_media": SocialMediaAgent,
            "calendar": lambda: CalendarAgent(Container.calendar_service()),
            "general": GeneralAgent
        }
        print(agent_mapping)

        agent_class = agent_mapping.get(decision)
        print(agent_class)

        if not agent_class:
            return "Agent not found."

        agent = agent_class()
         # Call handle_query with appropriate number of arguments
        return await agent.handle_query(userChatQuery, chatHistory)