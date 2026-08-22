from pathlib import Path

from app.core.config import settings
from app.services.pdf_service import PDFService
from app.vectorstore.chroma_manager import ChromaManager

upload_dir = Path(settings.UPLOAD_FOLDER)
pdf_service = PDFService()
chroma = ChromaManager()

print("Current directory:", Path.cwd())
print("Upload folder:", upload_dir)

pdf_files = sorted(upload_dir.glob("*.pdf"))
if not pdf_files:
    print("No PDF files found in uploads/.")
    raise SystemExit(0)

print(f"Found {len(pdf_files)} PDF file(s).")
print("Clearing existing ChromaDB data...")
chroma.clear_all()

total_chunks = 0
success = 0
failed = 0

for pdf_path in pdf_files:
    print("\n" + "=" * 60)
    print("Processing:", pdf_path.name)
    print("=" * 60)
    try:
        chunks = pdf_service.create_chunks(str(pdf_path))
        stored = chroma.add_chunks(chunks)
        pages = len({c["metadata"]["page"] for c in chunks})
        total_chunks += stored
        success += 1
        print(f"Pages: {pages}")
        print(f"Chunks: {stored}")
    except Exception as exc:
        failed += 1
        print(f"FAILED: {exc}")

print("\n" + "=" * 60)
print("REBUILD COMPLETE")
print("=" * 60)
print("PDFs found:", len(pdf_files))
print("Successfully processed:", success)
print("Failed:", failed)
print("Total chunks:", total_chunks)
