import sqlite3
from app.core.config import Settings

class SQLite:
    def __init__(self):
        self.connection = sqlite3.connect('chatbot.db')
        self.cursor = self.connection.cursor()

    def get_data(self, table_name: str):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()
