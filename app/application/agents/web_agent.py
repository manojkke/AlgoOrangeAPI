import json
import os
import re
from bs4 import BeautifulSoup  # For web scraping general URLs
import groq
import requests
from app.domain.interfaces import Agent

class WebAgent(Agent):
    def __init__(self):
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    async def handle_query(self, userChatQuery: str, userChatHistory: str) -> str:
        client = groq.Client(api_key=self.GROQ_API_KEY)  # Replace with your actual API key

        # Query Groq LLM to determine which action to perform
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are an AI assistant that performs web scraping actions."},
                {"role": "user", "content": f"Query: {userChatQuery}. Identify if the query is related to one of the following actions:"
                                            "summarize → If the query is about summarizing the content of a webpage,"
                                            "points → If the query asks to provide key points from the content,"
                                            "highlight → If the query involves highlighting specific information from the content."
                                            "Respond with only one word from the list: summarize, points, highlight. Do not provide explanations."}
            ],
            max_tokens=10
        )

        query_lower = response.choices[0].message.content.strip().lower()

        # Determine the type of query (summarize, points, highlight)
        if query_lower == "summarize":
            return await self.summarize_content(userChatQuery)
        elif query_lower == "points":
            return await self.provide_key_points(userChatQuery)
        elif query_lower == "highlight":
            return await self.highlight_information(userChatQuery)
        else:
            return "Unknown query type."

    async def summarize_content(self, userChatQuery: str) -> str:
        url = self.extract_url_from_query(userChatQuery)
        if not url:
            return "Could not extract URL from the query."
        
        content = self.fetch_webpage_content(url)
        return content

    async def provide_key_points(self, userChatQuery: str) -> str:
        url = self.extract_url_from_query(userChatQuery)
        if not url:
            return "Could not extract URL from the query."
        
        content = self.fetch_webpage_content(url)
        key_points = self.extract_key_points(content, num_points=10)  # Provide 10 key points
        return "\n".join(key_points)

    async def highlight_information(self, userChatQuery: str) -> str:
        url = self.extract_url_from_query(userChatQuery)
        if not url:
            return "Could not extract URL from the query."
        
        keyword = self.extract_keyword_from_query(userChatQuery)
        if not keyword:
            return "Could not extract keyword from the query."
        
        content = self.fetch_webpage_content(url)
        highlighted_content = self.highlight(content, keyword)
        return highlighted_content

    def extract_url_from_query(self, query: str) -> str:
        url_pattern = re.search(r"https?://[^\s]+", query)
        return url_pattern.group().rstrip(".,!?") if url_pattern else None

    def extract_keyword_from_query(self, query: str) -> str:
        keyword_pattern = re.search(r'highlight\s+(.+)', query)
        return keyword_pattern.group(1).strip() if keyword_pattern else None

    def fetch_webpage_content(self, url: str) -> str:
        """Fetches the main content of a webpage and returns clean text."""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                return f"Error fetching webpage: {response.status_code}"

            soup = BeautifulSoup(response.text, "html.parser")
            paragraphs = soup.find_all("p")  # Extract paragraphs
            text_content = "\n".join([p.get_text() for p in paragraphs])

            return text_content[:2000]  # Limit characters for efficiency
        except Exception as e:
            return f"Error fetching webpage content: {str(e)}"

    def extract_key_points(self, content: str, num_points: int) -> list:
        """Extract key points from the content."""
        sentences = content.split('.')
        key_points = []

        for sentence in sentences:
            if len(key_points) >= num_points:
                break
            if len(sentence.split()) > 5:  # Consider sentences with more than 5 words as key points
                key_points.append(sentence.strip())

        return key_points

    def highlight(self, content: str, keyword: str) -> str:
        # Implement highlighting logic here
        return content.replace(keyword, f"**{keyword}**")

