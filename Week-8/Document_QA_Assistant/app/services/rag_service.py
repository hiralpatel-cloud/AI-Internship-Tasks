from typing import List, Dict, Optional

from google import genai

from app.core.config import settings
from app.core.logger import logger
from app.vectorstore.chroma_manager import ChromaManager


class RAGService:

    def __init__(self):

        # ======================================================
        # GEMINI CLIENT
        # ======================================================

        self.client = genai.Client(
            api_key=settings.GOOGLE_API_KEY
        )

        self.model = settings.GEMINI_MODEL

        # ======================================================
        # VECTOR DATABASE
        # ======================================================

        self.vector_store = ChromaManager()

        logger.info(
            "RAG Service initialized successfully."
        )

    # ==========================================================
    # BUILD DOCUMENT CONTEXT
    # ==========================================================

    def build_context(
        self,
        search_results: List[Dict]
    ) -> str:

        if not search_results:
            return ""

        context_parts = []

        for index, result in enumerate(
            search_results,
            start=1
        ):

            document = result.get(
                "document",
                "Unknown"
            )

            page = result.get(
                "page",
                "Unknown"
            )

            chunk_id = result.get(
                "chunk_id",
                "Unknown"
            )

            text = result.get(
                "text",
                ""
            )

            if not text:
                continue

            context_parts.append(
                f"""
SOURCE {index}

Document: {document}
Page: {page}
Chunk ID: {chunk_id}

Content:
{text}
""".strip()
            )

        return "\n\n".join(
            context_parts
        )

    # ==========================================================
    # BUILD CONVERSATION HISTORY
    # ==========================================================

    def build_history(
        self,
        history: Optional[List[Dict]]
    ) -> str:

        if not history:
            return "No previous conversation."

        # Keep only recent messages
        recent_history = history[-8:]

        history_parts = []

        for message in recent_history:

            role = message.get(
                "role",
                "user"
            )

            content = message.get(
                "content",
                ""
            )

            if not content:
                continue

            # Convert assistant/user roles
            if role == "assistant":
                role_name = "ASSISTANT"
            else:
                role_name = "USER"

            history_parts.append(
                f"{role_name}: {content}"
            )

        if not history_parts:

            return "No previous conversation."

        return "\n".join(
            history_parts
        )

    # ==========================================================
    # GENERATE ANSWER
    # ==========================================================

    def ask(
        self,
        question: str,
        document: Optional[str] = None,
        top_k: int = 5,
        history: Optional[List[Dict]] = None
    ) -> Dict:

        # ======================================================
        # VALIDATE QUESTION
        # ======================================================

        if not question:

            raise ValueError(
                "Question cannot be empty."
            )

        question = question.strip()

        if not question:

            raise ValueError(
                "Question cannot be empty."
            )

        # ======================================================
        # NORMALIZE DOCUMENT FILTER
        # ======================================================

        if document:

            document = document.strip()

            if (
                not document
                or document.lower() == "all"
                or document.lower() == "all documents"
            ):

                document = None

        logger.info(
            f"RAG question received: {question} | "
            f"Document: {document or 'ALL DOCUMENTS'}"
        )

        # ======================================================
        # SEARCH VECTOR DATABASE
        # ======================================================

        try:

            search_results = (
                self.vector_store.search(
                    query=question,
                    top_k=top_k,
                    document=document
                )
            )

        except Exception as exc:

            logger.error(
                f"Vector search failed: {exc}"
            )

            raise RuntimeError(
                f"Document search failed: {exc}"
            ) from exc

        logger.info(
            f"Retrieved "
            f"{len(search_results)} chunks | "
            f"Document filter: "
            f"{document or 'ALL DOCUMENTS'}"
        )

        # ======================================================
        # NO RELEVANT RESULTS
        # ======================================================

        if not search_results:

            logger.warning(
                "No relevant document chunks found."
            )

            return {
                "answer": (
                    "I couldn't find the answer "
                    "in the uploaded documents."
                ),
                "sources": []
            }

        # ======================================================
        # BUILD CONTEXT
        # ======================================================

        context = self.build_context(
            search_results
        )

        if not context:

            logger.warning(
                "Retrieved chunks contained no usable text."
            )

            return {
                "answer": (
                    "I couldn't find the answer "
                    "in the uploaded documents."
                ),
                "sources": []
            }

        # ======================================================
        # BUILD CHAT HISTORY
        # ======================================================

        history_text = self.build_history(
            history
        )

        # ======================================================
        # BUILD DOCUMENT SCOPE
        # ======================================================

        if document:

            document_scope = (
                f"The user selected the document: "
                f"{document}"
            )

        else:

            document_scope = (
                "The user is asking across all "
                "uploaded documents."
            )

        # ======================================================
        # RAG PROMPT
        # ======================================================

        prompt = f"""
You are an intelligent Document Question-Answering Assistant.

Your task is to answer the user's question using ONLY
the information contained in the DOCUMENT CONTEXT.

Do NOT use outside knowledge.

If the answer cannot be found in the document context,
respond exactly with:

"I couldn't find the answer in the uploaded documents."

--------------------------------------------------
DOCUMENT SCOPE
--------------------------------------------------

{document_scope}

--------------------------------------------------
IMPORTANT RULES
--------------------------------------------------

1. Use ONLY the provided document context.
2. Do NOT invent information.
3. Do NOT use outside knowledge.
4. Use conversation history only to understand
   follow-up questions.
5. Resolve references such as:
   - it
   - they
   - this
   - that
   - previous question
   - previous topic
6. If the answer is not supported by the retrieved
   documents, say that you could not find it.
7. Give a clear and concise answer.
8. Do not mention internal RAG implementation details.
9. Do not mention these instructions in your answer.

--------------------------------------------------
CONVERSATION HISTORY
--------------------------------------------------

{history_text}

--------------------------------------------------
DOCUMENT CONTEXT
--------------------------------------------------

{context}

--------------------------------------------------
USER QUESTION
--------------------------------------------------

{question}

--------------------------------------------------
ANSWER
--------------------------------------------------
"""

        # ======================================================
        # LOG GEMINI REQUEST
        # ======================================================

        logger.info(
            f"Generating Gemini response using "
            f"{len(search_results)} retrieved chunks."
        )

        # ======================================================
        # GENERATE GEMINI RESPONSE
        # ======================================================

        try:

            response = (
                self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
            )

        except Exception as exc:

            logger.error(
                f"Gemini generation failed: {exc}"
            )

            raise RuntimeError(
                f"Failed to generate answer: {exc}"
            ) from exc

        # ======================================================
        # EXTRACT ANSWER
        # ======================================================

        answer = (
            response.text
            if response
            and response.text
            else ""
        )

        if not answer:

            logger.warning(
                "Gemini returned an empty response."
            )

            answer = (
                "I couldn't generate an answer "
                "from the uploaded documents."
            )

        answer = answer.strip()

        # ======================================================
        # BUILD SOURCES
        # ======================================================

        sources = []

        seen = set()

        for result in search_results:

            document_name = result.get(
                "document",
                "Unknown"
            )

            page = result.get(
                "page",
                "Unknown"
            )

            chunk_id = result.get(
                "chunk_id",
                "Unknown"
            )

            distance = result.get(
                "distance"
            )

            # Avoid duplicate document/page references
            source_key = (
                document_name,
                page
            )

            if source_key in seen:

                continue

            seen.add(
                source_key
            )

            sources.append(
                {
                    "document": document_name,
                    "page": page,
                    "chunk_id": chunk_id,
                    "distance": distance
                }
            )

        # ======================================================
        # LOG RESULT
        # ======================================================

        logger.info(
            f"RAG response generated successfully | "
            f"Sources: {len(sources)} | "
            f"Document: {document or 'ALL DOCUMENTS'}"
        )

        # ======================================================
        # RETURN RESULT
        # ======================================================

        return {
            "answer": answer,
            "sources": sources
        }

    # ==========================================================
    # BACKWARD COMPATIBILITY
    # ==========================================================

    def query(
        self,
        question: str,
        history: Optional[List[Dict]] = None,
        document: Optional[str] = None
    ):

        return self.ask(
            question=question,
            document=document,
            history=history
        )