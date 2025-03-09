from fastapi import FastAPI
from app.presentation.student_api import studentRouter
from app.presentation.chat_api import chatRouter

app = FastAPI()

app.include_router(studentRouter, prefix="/Students2", tags=["StudentsAPI"])
app.include_router(chatRouter, prefix="/chat", tags=["ChatAPI"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Student CRUD ddd API"}
