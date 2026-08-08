from fastapi import FastAPI

from Document_QA_Assistant.app.api.chat import router as chat_router
from Document_QA_Assistant.app.api.document import router as document_router
from Document_QA_Assistant.app.api.health import router as health_router
from Document_QA_Assistant.app.api.upload import router as upload_router
from Document_QA_Assistant.app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="RAG-based PDF Question & Answer Assistant.",
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(document_router)


@app.get("/")
def home():
    return {
        "message": "Document Q&A Assistant API Running",
        "docs": "/docs",
        "health": "/health",
    }
