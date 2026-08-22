from fastapi import APIRouter, HTTPException

from app.core.logger import logger
from app.vectorstore.chroma_manager import ChromaManager


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

chroma = ChromaManager()


@router.get("/")
def get_documents():

    try:

        documents = chroma.get_documents()

        return {
            "documents": documents
        }

    except Exception as exc:

        logger.exception(
            "Failed to retrieve documents."
        )

        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve documents: {exc}"
        )


@router.delete("/{filename}")
def delete_document(filename: str):

    try:

        filename = filename.strip()

        if not filename:

            raise HTTPException(
                status_code=400,
                detail="Filename cannot be empty."
            )

        deleted_chunks = chroma.delete_document(
            filename
        )

        return {
            "success": True,
            "message": "Document deleted successfully.",
            "filename": filename,
            "deleted_chunks": deleted_chunks
        }

    except HTTPException:
        raise

    except Exception as exc:

        logger.exception(
            "Failed to delete document."
        )

        raise HTTPException(
            status_code=500,
            detail=f"Document deletion failed: {exc}"
        )