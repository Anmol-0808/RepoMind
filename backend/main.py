from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import time

from agents.tools import set_active_repo
from agents.agent import app as agent_app

from ingestion.repo_loader import clone_repo, load_repository_files
from ingestion.code_chunker import chunk_repository, create_repo_structure_chunk
from retrieval.embeddings import embed_chunks
from retrieval.vector_store import add_chunks_to_vector_db


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


class RepoRequest(BaseModel):
    repo_url: str


@app.post("/analyze-repo")
def analyze_repo(request: RepoRequest):
    try:
        repo_path = clone_repo(request.repo_url)

        repo_name = repo_path.split("\\")[-1]
        set_active_repo(repo_name)

        files = load_repository_files(repo_path)

        chunks = chunk_repository(files)

        structure_chunk = create_repo_structure_chunk(files)
        chunks.append(structure_chunk)

        embedded_chunks = embed_chunks(
            chunks,
            repo_name=repo_name
        )

        add_chunks_to_vector_db(embedded_chunks)

        return {
            "message": "Repository analyzed successfully ✅"
        }

    except Exception as e:
        return {
            "message": f"Failed to analyze repository: {str(e)}"
        }


def stream_response(text):
    for char in text:
        yield char
        time.sleep(0.01)


@app.post("/chat")
def chat(request: ChatRequest):
    state = {
        "messages": request.messages + [request.message],
        "response": "",
        "last_repo_topic": request.last_repo_topic
    }

    result = agent_app.invoke(state)

    full_response = result["response"]

    return StreamingResponse(
        stream_response(full_response),
        media_type="text/plain"
    )