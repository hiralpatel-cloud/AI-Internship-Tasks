from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import pymupdf

from app.services.tts_service import TTSService


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/voice",
    tags=["Voice / Text-to-Speech"]
)


# ============================================================
# SERVICES AND DIRECTORIES
# ============================================================

tts_service = TTSService()

UPLOAD_DIR = Path("uploads")
AUDIO_DIR = Path("audio")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

AUDIO_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# REQUEST MODEL
# ============================================================

class VoiceRequest(BaseModel):

    text: str
    language: str = "english"


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_path: Path):

    document = pymupdf.open(
        pdf_path
    )

    text_parts = []

    try:

        for page in document:

            text = page.get_text()

            if text:

                text_parts.append(
                    text
                )

    finally:

        document.close()

    return "\n".join(
        text_parts
    )


# ============================================================
# TEXT → SPEECH
# ============================================================

@router.post("/speak")
async def speak_text(
    request: VoiceRequest
):

    try:

        # ----------------------------------------------------
        # Validate text
        # ----------------------------------------------------

        if not request.text.strip():

            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty."
            )

        # ----------------------------------------------------
        # Generate translated audio
        # ----------------------------------------------------

        result = tts_service.generate_audio(
            text=request.text,
            language=request.language,
            filename="text"
        )

        files = result["files"]

        # ----------------------------------------------------
        # Return response
        # ----------------------------------------------------

        return {
            "message": "Audio generated successfully.",

            "language": result["language"],

            "language_name": result["language_name"],

            "translated_text": result.get(
                "translated_text",
                request.text
            ),

            "total_audio_parts": len(files),

            "audio_files": [
                f"/voice/audio/{file}"
                for file in files
            ]
        }

    except HTTPException:
        raise

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Voice generation failed: {str(e)}"
        )


# ============================================================
# PDF → SPEECH
# ============================================================

@router.post("/pdf/{filename}")
async def pdf_to_speech(
    filename: str,
    language: str = "english"
):

    try:

        # ----------------------------------------------------
        # Prevent unsafe paths
        # ----------------------------------------------------

        safe_filename = Path(
            filename
        ).name

        pdf_path = (
            UPLOAD_DIR / safe_filename
        )

        # ----------------------------------------------------
        # Check PDF
        # ----------------------------------------------------

        if not pdf_path.exists():

            raise HTTPException(
                status_code=404,
                detail=(
                    f"PDF '{safe_filename}' "
                    "not found."
                )
            )

        # ----------------------------------------------------
        # Extract PDF text
        # ----------------------------------------------------

        text = extract_pdf_text(
            pdf_path
        )

        if not text.strip():

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text "
                    "found in PDF."
                )
            )

        # ----------------------------------------------------
        # Generate translated audio
        # ----------------------------------------------------

        result = tts_service.generate_audio(
            text=text,
            language=language,
            filename=safe_filename
        )

        files = result["files"]

        # ----------------------------------------------------
        # Return response
        # ----------------------------------------------------

        return {
            "message": (
                "PDF converted to speech "
                "successfully."
            ),

            "document": safe_filename,

            "language": result["language"],

            "language_name": result["language_name"],

            "translated_text": result.get(
                "translated_text",
                text
            ),

            "total_audio_parts": len(files),

            "audio_files": [
                f"/voice/audio/{file}"
                for file in files
            ]
        }

    except HTTPException:
        raise

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except RuntimeError as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                f"PDF voice generation failed: "
                f"{str(e)}"
            )
        )


# ============================================================
# GET AUDIO FILE
# ============================================================

@router.get("/audio/{filename}")
async def get_audio(
    filename: str
):

    # --------------------------------------------------------
    # Prevent directory traversal
    # --------------------------------------------------------

    safe_filename = Path(
        filename
    ).name

    audio_path = (
        AUDIO_DIR / safe_filename
    )

    # --------------------------------------------------------
    # Check audio file
    # --------------------------------------------------------

    if not audio_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Audio file not found."
        )

    # --------------------------------------------------------
    # Return MP3
    # --------------------------------------------------------

    return FileResponse(
        path=str(audio_path),
        media_type="audio/mpeg",
        filename=safe_filename
    )