from typing import List, Optional

from pydantic import BaseModel,Field


class ChatMessage(BaseModel):

    role: str
    content: str


class ChatRequest(BaseModel):

    question: str

    history: List[ChatMessage] = []

    document: Optional[str] = None