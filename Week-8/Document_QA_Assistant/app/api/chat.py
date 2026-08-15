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


# --------------------------------------------------
# Existing Chat / RAG endpoint
# --------------------------------------------------

@router.post("/")
def ask_question(request: ChatRequest):
    try:
        history = [
            message.model_dump()
            for message in request.history
        ]

        return rag.ask(
            request.question,
            history=history
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"RAG request failed: {exc}"
        ) from exc


# --------------------------------------------------
# Chat + Text-to-Speech endpoint
# --------------------------------------------------

@router.post("/with-audio")
def ask_question_with_audio(
    request: ChatRequest,
    language: str = "english"
):
    try:

        # 1. Get answer from RAG
        history = [
            message.model_dump()
            for message in request.history
        ]

        rag_result = rag.ask(
            request.question,
            history=history
        )

        # 2. Extract answer text
        if isinstance(rag_result, dict):

            answer = (
                rag_result.get("answer")
                or rag_result.get("response")
                or rag_result.get("result")
                or rag_result.get("message")
            )

        else:
            answer = str(rag_result)

        if not answer:
            raise ValueError(
                "RAG returned an empty answer."
            )

        # 3. Generate audio
        audio_result = tts_service.generate_audio(
            text=answer,
            language=language,
            filename="chat_answer"
        )

        # 4. Return answer + audio
        return {
            "success": True,
            "question": request.question,
            "answer": answer,
            "language": audio_result["language"],
            "language_name": audio_result["language_name"],
            "audio_files": audio_result["files"],
            "audio_urls": [
                f"/tts/audio/{filename}"
                for filename in audio_result["files"]
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