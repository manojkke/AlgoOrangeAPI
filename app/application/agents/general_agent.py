from dotenv import load_dotenv
from app.domain.interfaces import Agent
import groq
import os
# Load environment variables from .env file
load_dotenv()

class GeneralAgent(Agent):
    def __init__(self):
        self.client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

    async def handle_query(self, userChatQuery: str, chatHistory: str):
        # Combine the user query and chat history into a single message list
        messages = [
            {"role": "system", "content": "You are an AI assistant providing general advice."}
        ]
        
        # Add previous chat history
        if chatHistory:
            for history in chatHistory.split('\n'):
                messages.append({"role": "user", "content": history})
        
        # Add the current user query
        messages.append({"role": "user", "content": userChatQuery})

        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Use the best available Groq model
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
