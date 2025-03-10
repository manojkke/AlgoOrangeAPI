from app.domain.interfaces import Agent
from app.infrastructure.services.student.student_service import create_student, get_student, update_student, delete_student
from app.schemas.student import StudentCreate, StudentUpdate

class StudentAgent(Agent):
    def __init__(self, student_service, student_data):
        self.student_data = student_data
        self.student_service = student_service

    async def handle_query(self, userChatQuery: str, chatHistory: str, db_session):
        if "create student" in userChatQuery:
            new_student = await create_student(db_session, StudentCreate(**self.student_data))
            return f"Created student: {new_student}"
        elif "get student" in userChatQuery:
            student_id = int(userChatQuery.split()[-1])
            student = get_student(db_session, student_id)
            return f"Student details: {student}"
        elif "update student" in userChatQuery:
            student_id = int(userChatQuery.split()[-1])
            updated_student = update_student(db_session, student_id, StudentUpdate(**self.student_data))
            return f"Updated student: {updated_student}"
        elif "delete student" in userChatQuery:
            student_id = int(userChatQuery.split()[-1])
            deleted_student = delete_student(db_session, student_id)
            return f"Deleted student: {deleted_student}"
        return "Invalid query"
