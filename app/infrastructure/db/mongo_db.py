from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import Settings

class MongoDB:
    def __init__(self):
        self.client = AsyncIOMotorClient(Settings().db_type)
        self.db = self.client["chatbot_db"]

    async def get_data(self, collection_name: str):
        return await self.db[collection_name].find().to_list(length=100)
