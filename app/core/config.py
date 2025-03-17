class Settings:
    db_type: str = "MongoDB"  # MongoDB or SQLite
    calendar_service: str = "Google"  # Google or Microsoft

    def get_db_type(self):
        return self.db_type
