from typing import List, Dict, Optional

import chromadb

from app.core.config import settings
from app.core.logger import logger
from app.services.embedding_service import EmbeddingService


class ChromaManager:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="document_chunks"
            )
        )

        logger.info(
            "ChromaDB collection initialized."
        )

    # ==========================================================
    # ADD CHUNKS
    # ==========================================================

    def add_chunks(
        self,
        chunks: List[Dict]
    ) -> int:

        if not chunks:
            raise ValueError(
                "No chunks provided."
            )

        documents = []
        metadatas = []
        ids = []

        for chunk in chunks:

            text = chunk.get(
                "text",
                ""
            ).strip()

            if not text:
                continue

            metadata = chunk.get(
                "metadata",
                {}
            )

            document_name = metadata.get(
                "document",
                "unknown"
            )

            page = metadata.get(
                "page",
                0
            )

            chunk_id = metadata.get(
                "chunk_id"
            )

            if not chunk_id:

                chunk_id = (
                    f"{document_name}"
                    f"_page_{page}"
                    f"_chunk_{len(ids) + 1}"
                )

            documents.append(text)

            metadatas.append(
                {
                    "document": str(
                        document_name
                    ),

                    "source": str(
                        metadata.get(
                            "source",
                            document_name
                        )
                    ),

                    "page": int(page),

                    "chunk_id": str(
                        chunk_id
                    ),

                    "chunk_index": int(
                        metadata.get(
                            "chunk_index",
                            len(ids) + 1
                        )
                    ),

                    "page_chunk_index": int(
                        metadata.get(
                            "page_chunk_index",
                            1
                        )
                    )
                }
            )

            ids.append(
                str(chunk_id)
            )

        if not documents:
            raise ValueError(
                "No valid chunks to store."
            )

        embeddings = (
            self.embedding_service
            .generate_embeddings(
                documents
            )
        )

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        logger.info(
            f"Stored {len(documents)} chunks "
            f"in ChromaDB."
        )

        return len(documents)

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search(
        self,
        query: str,
        top_k: int = 5,
        document: Optional[str] = None
    ) -> List[Dict]:

        if not query or not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        query_embedding = (
            self.embedding_service
            .generate_embeddings(
                [query.strip()]
            )[0]
        )

        where = None

        if document and document.lower() != "all":

            where = {
                "document": document
            }

        try:

            results = self.collection.query(
                query_embeddings=[
                    query_embedding
                ],

                n_results=top_k,

                where=where,

                include=[
                    "documents",
                    "metadatas",
                    "distances"
                ]
            )

        except Exception as exc:

            logger.error(
                f"ChromaDB search failed: {exc}"
            )

            raise

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        search_results = []

        for index, text in enumerate(
            documents
        ):

            metadata = (
                metadatas[index]
                if index < len(metadatas)
                else {}
            )

            distance = (
                distances[index]
                if index < len(distances)
                else None
            )

            search_results.append(
                {
                    "text": text,

                    "document": metadata.get(
                        "document",
                        "Unknown"
                    ),

                    "page": metadata.get(
                        "page",
                        "Unknown"
                    ),

                    "chunk_id": metadata.get(
                        "chunk_id",
                        "Unknown"
                    ),

                    "chunk_index": metadata.get(
                        "chunk_index",
                        0
                    ),

                    "distance": distance,

                    "metadata": metadata
                }
            )

        logger.info(
            f"Retrieved {len(search_results)} "
            f"chunks for query."
        )

        return search_results

    # ==========================================================
    # GET DOCUMENTS
    # ==========================================================

    def get_documents(self) -> List[str]:

        try:

            result = self.collection.get(
                include=["metadatas"]
            )

            metadatas = result.get(
                "metadatas",
                []
            )

            documents = sorted(
                {
                    metadata.get("document")

                    for metadata in metadatas

                    if metadata
                    and metadata.get("document")
                }
            )

            return documents

        except Exception as exc:

            logger.error(
                f"Failed to get documents: {exc}"
            )

            return []

    # ==========================================================
    # DELETE DOCUMENT
    # ==========================================================

    def delete_document(
        self,
        document_name: str
    ):

        if not document_name:
            raise ValueError(
                "Document name is required."
            )

        self.collection.delete(
            where={
                "document": document_name
            }
        )

        logger.info(
            f"Deleted document: {document_name}"
        )

    # ==========================================================
    # CLEAR DATABASE
    # ==========================================================

    def clear_all(self):

        try:

            self.client.delete_collection(
                name="document_chunks"
            )

        except Exception:
            pass

        self.collection = (
            self.client.get_or_create_collection(
                name="document_chunks"
            )
        )

        logger.info(
            "ChromaDB collection cleared."
        )

    # ==========================================================
    # COUNT
    # ==========================================================

    def count(self):

        return self.collection.count()