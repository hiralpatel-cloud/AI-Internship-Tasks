import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from Document_QA_Assistant.app.core.config import settings
from Document_QA_Assistant.app.core.logger import logger


class ChromaManager:
    COLLECTION_NAME = "documents"
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.embedding_function = SentenceTransformerEmbeddingFunction(
            model_name=self.EMBEDDING_MODEL
        )
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            embedding_function=self.embedding_function,
            metadata={"description": "PDF document chunks"},
        )
        logger.info("Connected to ChromaDB collection '%s'.", self.COLLECTION_NAME)

    def add_chunks(self, chunks):
        if not chunks:
            logger.warning("No chunks to store.")
            return 0

        documents = [chunk["content"] for chunk in chunks]
        metadatas = [
            {
                "page": int(chunk["page"]),
                "document": chunk["document"],
            }
            for chunk in chunks
        ]
        ids = [
            f'{chunk["document"]}__{chunk["page"]}__{chunk["chunk_index"]}'
            for chunk in chunks
        ]

        self.collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )
        logger.info("Stored/upserted %s chunks.", len(documents))
        return len(documents)

    def search(self, query: str, top_k: int = 10):
        if self.collection.count() == 0:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}

        top_k = min(top_k, self.collection.count())
        return self.collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

    def get_documents(self):
        results = self.collection.get(include=["metadatas"])
        documents = {
            metadata.get("document")
            for metadata in results.get("metadatas", [])
            if metadata and metadata.get("document")
        }
        return sorted(documents)

    def delete_document(self, filename: str):
        results = self.collection.get(where={"document": filename})
        ids = results.get("ids", [])

        if not ids:
            return False

        self.collection.delete(ids=ids)
        logger.info("Deleted %s chunks for %s.", len(ids), filename)
        return True

    def clear_all(self):
        if self.collection.count() > 0:
            self.collection.delete(where={})
        logger.info("Cleared all ChromaDB document chunks.")
