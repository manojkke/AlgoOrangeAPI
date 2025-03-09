from abc import ABC, abstractmethod

class Agent(ABC):
    @abstractmethod
    async def handle_query(self, query: str) -> str:
        pass
