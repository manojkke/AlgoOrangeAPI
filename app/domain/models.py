# Example model, can be expanded based on requirements
from pydantic import BaseModel

class UserQuery(BaseModel):
    query: str
    user_id: str
