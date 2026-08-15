from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.core.logger import logger
from app.vectorstore.chroma_manager import ChromaManager


router = APIRouter(prefix="/documents", tags=["Documents"])
UPLOAD_DIR = Path(settings.UPLOAD_FOLDER)
chroma = ChromaManager()


@router.get("/")
def get_documents():
    documents = chroma.get_documents()
    return {"count": len(documents), "documents": documents}


@router.delete("/{filename}")
def delete_document(filename: str):
    safe_name = Path(filename).name
    pdf_path = UPLOAD_DIR / safe_name

    db_deleted = chroma.delete_document(safe_name)
    file_deleted = pdf_path.exists()

    if file_deleted:
        pdf_path.unlink()
        logger.info("Deleted file: %s", safe_name)

    if db_deleted or file_deleted:
        return {"message": f"{safe_name} deleted successfully."}

    raise HTTPException(status_code=404, detail="Document not found.")
