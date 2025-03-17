import json
from app.domain.interfaces import Agent
from app.infrastructure.services.vector.vector_store import retrieve_relevant_text
import groq
import ast

class ProjectAgent(Agent):
    async def handle_query(self, userChatQuery, chatHistory):
        retrieved_data = retrieve_relevant_text(userChatQuery)
        
        try:
            data_list = ast.literal_eval(retrieved_data)  # Safely convert to a list
    
    # Convert list of dictionaries to JSON format for further processing
            json_data = json.dumps(data_list, indent=4)
            print(f"✅ JSON Output:\n{json_data}")

        except (SyntaxError, ValueError) as e:
            print(f"❌ Error converting data: {e}")

        # If retrieved_data is not a list, make it one
        if not isinstance(retrieved_data, list):
            retrieved_data = [retrieved_data]  # Wrap it in a list if it's a dict

        # Extract relevant details from each document
        # Ensure extracted data is a dictionary before accessing .get()
        formatted_context = "\n".join(
            f"- {item.get('collection_name', 'Unknown')}: {item.get('description', item.get('risk_description', item.get('name', 'No description available')))}"
            if isinstance(item, dict) else f"- {item}"  # If item is a string, include it as-is
            for item in retrieved_data
        )

        # Construct the prompt
        prompt = (
            f"Question: {userChatQuery}\n"
            f"Chat History: {chatHistory}\n"
            f"Context:\n{formatted_context}\n"
            f"Answer:"
        )

        # Use Groq's client
        client = groq.Client(api_key="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")  
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are an AI assistant for project management."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
