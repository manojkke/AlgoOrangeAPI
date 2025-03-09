from fastapi import FastAPI, APIRouter, Depends
from app.application.orchestrator.use_cases import Orchestrator
from app.core.di import Container
import random

app = FastAPI()
chatRouter = APIRouter()


@chatRouter.get("/query")
async def query_handler(userChatQuery: str, chatHistory: str, currentUser: str):
    orchestrator = Orchestrator(userChatQuery, chatHistory)
    response = await orchestrator.route_query(userChatQuery, chatHistory)
    test = "All Good Algo ORange AI " + userChatQuery
    return {"response": test}


app.include_router(chatRouter)
