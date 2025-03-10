from app.domain.interfaces import Agent

class MedicalAgent(Agent):
    async def handle_query(self, userChatQuery: str, chatHistory: str):
        # Implementation for handling medical queries
        # Medical-specific processing here
        return "Medical advice based on query"
