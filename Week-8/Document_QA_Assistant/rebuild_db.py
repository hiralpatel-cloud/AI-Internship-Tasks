from pathlib import Path

from app.core.config import settings
from app.services.chunk_service import ChunkService
from app.services.pdf_service import PDFService
from app.vectorstore.chroma_manager import ChromaManager


upload_dir = Path(settings.UPLOAD_FOLDER)
pdf_service = PDFService()
chunk_service = ChunkService()
chroma = ChromaManager()

print("Current directory:", Path.cwd())
print("Upload folder:", upload_dir)

pdf_files = sorted(upload_dir.glob("*.pdf"))

if not pdf_files:
    print("No PDF files found in uploads/.")
    raise SystemExit(0)

chroma.clear_all()

total_chunks = 0

for pdf_path in pdf_files:
    print(f"\nProcessing: {pdf_path.name}")
    pages = pdf_service.extract_text(str(pdf_path))
    chunks = chunk_service.create_chunks(pages)
    stored = chroma.add_chunks(chunks)
    total_chunks += stored
    print(f"Pages: {len(pages)} | Chunks: {stored}")

print(f"\nRebuild complete. PDFs: {len(pdf_files)} | Total chunks: {total_chunks}")
