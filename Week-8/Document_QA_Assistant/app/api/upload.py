from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.core.logger import logger
from app.services.chunk_service import ChunkService
from app.services.pdf_service import PDFService
from app.vectorstore.chroma_manager import ChromaManager

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = Path(settings.UPLOAD_FOLDER)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

pdf_service = PDFService()
chunk_service = ChunkService()
chroma = ChromaManager()


@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    safe_name = Path(file.filename).name
    if not safe_name.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    destination = UPLOAD_DIR / safe_name
    if destination.exists():
        raise HTTPException(status_code=409, detail=f"{safe_name} already exists.")

    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        max_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024
        if destination.stat().st_size > max_bytes:
            destination.unlink(missing_ok=True)
            raise HTTPException(
                status_code=413,
                detail=f"PDF exceeds the {settings.MAX_FILE_SIZE_MB} MB limit.",
            )

        pages = pdf_service.extract_text(str(destination))
        if not any(page["text"].strip() for page in pages):
            destination.unlink(missing_ok=True)
            raise HTTPException(
                status_code=400,
                detail="No extractable text was found in the PDF. Scanned PDFs need OCR support.",
            )

        chunks = chunk_service.create_chunks(pages)
        stored = chroma.add_chunks(chunks)

        logger.info("Indexed %s: %s pages, %s chunks.", safe_name, len(pages), stored)

        return {
            "message": "PDF uploaded and indexed successfully.",
            "filename": safe_name,
            "pages": len(pages),
            "chunks": stored,
        }

    except HTTPException:
        raise
    except Exception as exc:
        destination.unlink(missing_ok=True)
        logger.exception("PDF upload failed: %s", safe_name)
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {exc}") from exc
