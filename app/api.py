from fastapi import FastAPI
from pydantic import BaseModel

from app.graph import build_graph, chat

app = FastAPI(title="Task 1 – Tool Selection Agent")
graph = build_graph()


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest) -> ChatResponse:
    return ChatResponse(session_id=req.session_id, reply=chat(graph, req.session_id, req.message))


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}