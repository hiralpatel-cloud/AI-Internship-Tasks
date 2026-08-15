from sentence_transformers import SentenceTransformer

from app.core.logger import logger


class EmbeddingService:
    def __init__(self):
        logger.info("Loading embedding model...")
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        logger.info("Embedding model loaded successfully.")

    def embed_text(self, text: str):
        return self.model.encode(text).tolist()

    def embed_texts(self, texts: list[str]):
        return self.model.encode(texts).tolist()
