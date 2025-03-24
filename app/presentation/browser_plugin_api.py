from fastapi import FastAPI, APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from app.application.orchestrator.use_cases import Orchestrator

app = FastAPI()
browserPluginApiRouter = APIRouter()


# Define a Pydantic model for the request body
class BrowserRequest(BaseModel):
    action: str
    content: str
    userQuestion: Optional[str] = None


@browserPluginApiRouter.post("/v1/webHelper")
async def handle_browser_request(request: BrowserRequest):
    print(
        f"Request received: action={request.action}, content={request.content}, userQuestion={request.userQuestion}"
    )
    # # Process user query using Orchestrator if userQuestion is provided
    # if request.userQuestion:
    #     orchestrator = Orchestrator(userChatQuery=request.userQuestion)
    #     response = await orchestrator.route_query()
    # else:
    #     response = "No user question provided."

    return {"message": "Request processed successfully"}


app.include_router(browserPluginApiRouter, prefix="/browserPlugin")
