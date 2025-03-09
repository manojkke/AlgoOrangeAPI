from app.domain.interfaces import Agent

class SocialMediaAgent(Agent):
    async def handle_query(self, query: str) -> str:
        # Social Media-specific processing here
        return "Social Media advice based on query"
