from google import genai

from app.core.config import settings
from app.core.logger import logger
from app.prompts.prompt import RAG_PROMPT
from app.vectorstore.chroma_manager import ChromaManager


class RAGService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.vector_db = ChromaManager()
        logger.info("RAG Service initialized with model %s.", settings.GEMINI_MODEL)

    @staticmethod
    def _build_history(history):
        lines = []
        for message in history[-10:]:
            role = message.get("role", "").capitalize()
            content = message.get("content", "").strip()
            if role in {"User", "Assistant"} and content:
                lines.append(f"{role}: {content}")
        return "\n".join(lines) if lines else "No previous conversation."

    @staticmethod
    def _select_results(results):
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        candidates = []
        for document, metadata, distance in zip(documents, metadatas, distances):
            if not document or not metadata:
                continue
            candidates.append(
                {
                    "content": document,
                    "metadata": metadata,
                    "distance": float(distance),
                }
            )

        candidates.sort(key=lambda item: item["distance"])

        # Chroma's L2 distance is lower for better matches.
        # Always keep the best match; keep additional matches only
        # when they are reasonably close to the best distance.
        if not candidates:
            return []

        best_distance = candidates[0]["distance"]
        threshold = max(0.75, best_distance + 0.35)

        selected = []
        page_counts = {}

        for item in candidates:
            if item["distance"] > threshold:
                continue

            metadata = item["metadata"]
            key = (metadata.get("document"), metadata.get("page"))
            page_counts[key] = page_counts.get(key, 0) + 1

            # At most two chunks from the same page.
            if page_counts[key] > 2:
                continue

            selected.append(item)
            if len(selected) >= 6:
                break

        return selected

    def ask(self, question: str, history=None):
        question = question.strip()
        history = history or []

        if not question:
            return {"answer": "Please enter a question.", "sources": []}

        results = self.vector_db.search(question, top_k=10)
        relevant = self._select_results(results)

        if not relevant:
            return {
                "answer": "I couldn't find the answer in the uploaded documents.",
                "sources": [],
            }

        context_parts = []
        sources = []

        for index, item in enumerate(relevant, start=1):
            metadata = item["metadata"]
            document = metadata.get("document", "Unknown document")
            page = metadata.get("page", "Unknown")

            context_parts.append(
                f"SOURCE {index}\n"
                f"Document: {document}\n"
                f"Page: {page}\n\n"
                f"{item['content']}"
            )

            source = {"document": document, "page": page}
            if source not in sources:
                sources.append(source)

        prompt = RAG_PROMPT.format(
            context="\n\n".join(context_parts),
            history=self._build_history(history),
            question=question,
        )

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )

        answer = (response.text or "").strip()
        if not answer:
            answer = "I couldn't generate an answer from the uploaded documents."

        logger.info("Answered question using %s retrieved chunks.", len(relevant))

        return {"answer": answer, "sources": sources}
