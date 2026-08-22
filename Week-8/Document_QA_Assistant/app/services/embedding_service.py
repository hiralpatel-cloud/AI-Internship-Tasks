from sentence_transformers import SentenceTransformer

from app.core.logger import logger


class EmbeddingService:

    def __init__(self):
        logger.info("Loading embedding model...")

        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        logger.info("Embedding model loaded successfully.")

    def embed_text(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        return self.model.encode(
            text,
            normalize_embeddings=True
        ).tolist()

    def embed_texts(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        if not texts:
            raise ValueError("Texts cannot be empty.")

        return self.model.encode(
            texts,
            normalize_embeddings=True
        ).tolist()

    # Compatibility method
    def generate_embeddings(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        return self.embed_texts(texts)