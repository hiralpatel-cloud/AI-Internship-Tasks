from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest
from app.services.rag_service import RAGService
from app.services.tts_service import TTSService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


rag = RAGService()
tts_service = TTSService()


# ==================================================
# NORMAL CHAT
# ==================================================

@router.post("/")
def ask_question(request: ChatRequest):

    try:

        question = request.question.strip()

        if not question:

            raise ValueError(
                "Question cannot be empty."
            )

        history = [
            message.model_dump()
            for message in request.history
        ]

        result = rag.ask(
            question=question,
            history=history,
            document=request.document
        )

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"RAG request failed: {exc}"
        ) from exc


# ==================================================
# CHAT + VOICE
# ==================================================

@router.post("/with-audio")
def ask_question_with_audio(
    request: ChatRequest,
    language: str = "english"
):

    try:

        question = request.question.strip()

        if not question:

            raise ValueError(
                "Question cannot be empty."
            )

        history = [
            message.model_dump()
            for message in request.history
        ]

        # -----------------------------
        # RAG
        # -----------------------------

        rag_result = rag.ask(
            question=question,
            history=history,
            document=request.document
        )

        answer = rag_result.get(
            "answer",
            ""
        )

        if not answer:

            raise ValueError(
                "RAG returned an empty answer."
            )

        # -----------------------------
        # TTS
        # -----------------------------

        audio_result = (
            tts_service.generate_audio(
                text=answer,
                language=language,
                filename="chat_answer"
            )
        )

        # -----------------------------
        # RESPONSE
        # -----------------------------

        return {

            "success": True,

            "question": question,

            "document": request.document or "ALL",

            "answer": answer,

            "sources": rag_result.get(
                "sources",
                []
            ),

            "language": (
                audio_result["language"]
            ),

            "language_name": (
                audio_result["language_name"]
            ),

            "audio_files": (
                audio_result["files"]
            ),

            "audio_urls": [
                f"/tts/audio/{filename}"
                for filename
                in audio_result["files"]
            ]
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Chat with audio failed: {exc}"
        ) from exc