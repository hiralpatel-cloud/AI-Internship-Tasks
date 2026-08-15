from pathlib import Path

import pymupdf

from app.core.logger import logger


class PDFService:

    def extract_text(self, pdf_path: str):
        pages = []

        path = Path(pdf_path)

        with pymupdf.open(path) as document:

            for page_number, page in enumerate(
                document,
                start=1
            ):

                text = page.get_text("text").strip()

                pages.append(
                    {
                        "page": page_number,
                        "text": text,
                        "document": path.name,
                    }
                )

        logger.info(
            "Extracted %s pages from %s",
            len(pages),
            path.name
        )

        return pages