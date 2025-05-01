from dotenv import load_dotenv
from app.domain.interfaces import Agent
import groq
import os
# Load environment variables from .env file
load_dotenv()

class GeneralAgent(Agent):
    def __init__(self):
        self.client = groq.Client(api_key="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")

    async def handle_query(self, userChatQuery: str, chatHistory: str):
        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Use the best available Groq model
            messages=[
                {"role": "system", "content": "You are an AI assistant providing general advice."},
                {"role": "user", "content": userChatQuery},
                {"role": "user", "content": chatHistory}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content