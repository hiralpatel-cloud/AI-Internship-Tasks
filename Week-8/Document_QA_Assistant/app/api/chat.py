from fastapi import APIRouter, HTTPException

from Document_QA_Assistant.app.schemas.chat import ChatRequest
from Document_QA_Assistant.app.services.rag_service import RAGService


router = APIRouter(prefix="/chat", tags=["Chat"])
rag = RAGService()


@router.post("/")
def ask_question(request: ChatRequest):
    try:
        history = [message.model_dump() for message in request.history]
        return rag.ask(request.question, history=history)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"RAG request failed: {exc}") from exc
