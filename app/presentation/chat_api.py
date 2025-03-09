from fastapi import FastAPI, APIRouter, Depends
from app.application.orchestrator.use_cases import Orchestrator
from app.core.di import Container

app = FastAPI()
chatRouter = APIRouter()


@chatRouter.post("/query")
async def query_handler(query: str):
    orchestrator = Orchestrator(query)
    response = await orchestrator.route_query(query)
    return {"response": response}


app.include_router(chatRouter)
