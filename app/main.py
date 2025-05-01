from fastapi import FastAPI
from app.presentation.chat_api import chatRouter

from app.presentation.browser_plugin_api import browserPluginApiRouter
from app.application.agents.calendar_agent import CalendarAgent
from app.infrastructure.services.calendar.google_calendar import GoogleCalendar
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.include_router(chatRouter, prefix="/chat", tags=["ChatAPI"])
app.include_router(
    browserPluginApiRouter, prefix="/browserPlugin", tags=["BrowserPluginAPI"]
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Student CRUD ddd API"}
