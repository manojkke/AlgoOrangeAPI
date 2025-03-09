from app.domain.interfaces import Agent

class MedicalAgent(Agent):
    async def handle_query(self, query: str) -> str:
        # Medical-specific processing here
        return "Medical advice based on query"
