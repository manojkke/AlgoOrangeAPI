from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import Settings

class MongoDB:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.client = AsyncIOMotorClient(Settings().db_type)
        self.db = self.client["chatbot_db"]

    @property
    def session(self):
        # Implement the session logic here
        return self._create_session()

    def _create_session(self):
        # Logic to create and return a session
        pass

    async def get_data(self, collection_name: str):
        return await self.db[collection_name].find().to_list(length=100)
