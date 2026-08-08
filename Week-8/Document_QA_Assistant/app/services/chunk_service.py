from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkService:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " ", ""],
        )

    def create_chunks(self, pages):
        chunks = []

        for page in pages:
            text = page["text"].strip()
            if not text:
                continue

            for chunk_index, text_chunk in enumerate(
                self.splitter.split_text(text)
            ):
                text_chunk = text_chunk.strip()
                if not text_chunk:
                    continue

                chunks.append(
                    {
                        "content": text_chunk,
                        "page": page["page"],
                        "document": page["document"],
                        "chunk_index": chunk_index,
                    }
                )

        return chunks
