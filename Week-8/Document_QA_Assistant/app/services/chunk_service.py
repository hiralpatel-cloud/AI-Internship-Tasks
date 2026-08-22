from typing import List, Dict

from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkService:

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 120
    ):

        self.splitter = RecursiveCharacterTextSplitter(
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

    def create_chunks(
        self,
        pages: List[Dict]
    ) -> List[Dict]:

        chunks = []

        global_chunk_id = 0

        for page_data in pages:

            text = page_data.get(
                "text",
                ""
            ).strip()

            if not text:
                continue

            document = page_data.get(
                "document",
                "Unknown"
            )

            page = page_data.get(
                "page",
                0
            )

            page_chunks = self.splitter.split_text(
                text
            )

            for page_chunk_index, chunk_text in enumerate(
                page_chunks,
                start=1
            ):

                chunk_text = chunk_text.strip()

                if not chunk_text:
                    continue

                global_chunk_id += 1

                chunk_id = (
                    f"{document}"
                    f"_page_{page}"
                    f"_chunk_{page_chunk_index}"
                )

                chunks.append(
                    {
                        "text": chunk_text,

                        "metadata": {
                            "document": str(document),
                            "source": str(document),
                            "page": int(page),
                            "chunk_id": chunk_id,
                            "chunk_index": global_chunk_id,
                            "page_chunk_index": page_chunk_index
                        }
                    }
                )

        return chunks