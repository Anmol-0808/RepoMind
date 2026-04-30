from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.agent import app as agent_app

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    last_repo_topic: str = ""
    messages: list = []


@app.post("/chat")
def chat(request: ChatRequest):

    state = {
        "messages": request.messages + [request.message],
        "response": "",
        "last_repo_topic": request.last_repo_topic
    }

    result = agent_app.invoke(state)

    return {
        "response": result["response"],
        "last_repo_topic": result.get("last_repo_topic", "")
    }