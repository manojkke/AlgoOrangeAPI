from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.student_api import studentRouter
from app.presentation.chat_api import chatRouter

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.include_router(studentRouter, prefix="/Students2", tags=["StudentsAPI"])
app.include_router(chatRouter, prefix="/chat", tags=["ChatAPI"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Student CRUD ddd API"}
