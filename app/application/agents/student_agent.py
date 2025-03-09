from app.domain.interfaces import Agent

class StudentAgent(Agent):
    async def handle_query(self, query: str) -> str:
        # Student-specific processing here
        return "Student-related response"
