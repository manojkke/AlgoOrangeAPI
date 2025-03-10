from fastapi import FastAPI
from app.presentation.student_api import studentRouter
from app.presentation.chat_api import chatRouter
from app.application.agents.calendar_agent import CalendarAgent
from app.infrastructure.services.calendar.google_calendar import GoogleCalendar

app = FastAPI()

app.include_router(studentRouter, prefix="/Students2", tags=["StudentsAPI"])
app.include_router(chatRouter, prefix="/chat", tags=["ChatAPI"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Student CRUD ddd API"}

