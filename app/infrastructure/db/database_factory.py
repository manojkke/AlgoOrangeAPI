from app.core.config import Settings
from app.infrastructure.db.sqlite_db import SQLite
from app.infrastructure.db.mongo_db import MongoDB
from app.infrastructure.db.database_interface import DatabaseInterface

class DatabaseFactory:
    @staticmethod
    def get_database() -> DatabaseInterface:
        db_type = Settings().get_db_type()
        if db_type == "MongoDB":
            return MongoDB()
        elif db_type == "SQLite":
            return SQLite()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
