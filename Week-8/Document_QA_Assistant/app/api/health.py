from fastapi import APIRouter

from app.core.config import settings
from app.vectorstore.chroma_manager import ChromaManager


router = APIRouter(tags=["Health"])
chroma = ChromaManager()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.APP_ENV,
        "documents": len(chroma.get_documents()),
        "chunks": chroma.collection.count(),
    }
