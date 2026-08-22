from pathlib import Path
from typing import List, Dict

import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.logger import logger


class PDFService:

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 120
    ):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                "; ",
                ", ",
                " ",
                ""
            ]
        )

    # ==========================================================
    # EXTRACT PAGE-WISE TEXT
    # ==========================================================

    def extract_pages(
        self,
        pdf_path: str
    ) -> List[Dict]:

        path = Path(pdf_path)

        if not path.exists():
            raise FileNotFoundError(
                f"PDF not found: {path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                "Only PDF files are supported."
            )

        logger.info(
            f"Extracting PDF: {path.name}"
        )

        pages = []

        document = pymupdf.open(str(path))

        try:

            for page_number, page in enumerate(
                document,
                start=1
            ):

                text = page.get_text("text")

                text = self.clean_text(text)

                if not text:
                    continue

                pages.append(
                    {
                        "document": path.name,
                        "page": page_number,
                        "text": text
                    }
                )

        finally:

            document.close()

        if not pages:
            raise ValueError(
                "No readable text found in PDF."
            )

        logger.info(
            f"Extracted {len(pages)} readable pages "
            f"from {path.name}"
        )

        return pages

    # ==========================================================
    # BACKWARD COMPATIBILITY
    # ==========================================================

    def extract_text(
        self,
        pdf_path: str
    ) -> List[Dict]:

        return self.extract_pages(pdf_path)

    # ==========================================================
    # CLEAN TEXT
    # ==========================================================

    def clean_text(
        self,
        text: str
    ) -> str:

        if not text:
            return ""

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if line:
                lines.append(line)

        return "\n".join(lines)

    # ==========================================================
    # CREATE CHUNKS
    # ==========================================================

    def create_chunks(
        self,
        pdf_path: str
    ) -> List[Dict]:

        path = Path(pdf_path)

        document_name = path.name

        pages = self.extract_pages(
            str(path)
        )

        chunks = []

        global_chunk_index = 0

        for page_data in pages:

            page_number = page_data["page"]

            page_text = page_data["text"]

            page_chunks = self.text_splitter.split_text(
                page_text
            )

            for page_chunk_index, chunk in enumerate(
                page_chunks,
                start=1
            ):

                chunk = chunk.strip()

                if not chunk:
                    continue

                global_chunk_index += 1

                chunk_id = (
                    f"{document_name}"
                    f"_page_{page_number}"
                    f"_chunk_{page_chunk_index}"
                )

                chunks.append(
                    {
                        "text": chunk,

                        "metadata": {
                            "document": document_name,
                            "source": document_name,
                            "page": page_number,
                            "chunk_id": chunk_id,
                            "chunk_index": global_chunk_index,
                            "page_chunk_index": page_chunk_index
                        }
                    }
                )

        if not chunks:
            raise ValueError(
                "No chunks could be created from PDF."
            )

        logger.info(
            f"Created {len(chunks)} chunks "
            f"from {document_name}"
        )

        return chunks

    # ==========================================================
    # PROCESS PDF
    # ==========================================================

    def process_pdf(
        self,
        pdf_path: str
    ):

        return self.create_chunks(pdf_path)