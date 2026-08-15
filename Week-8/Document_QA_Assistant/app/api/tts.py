from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.services.tts_service import TTSService


router = APIRouter(
    prefix="/tts",
    tags=["Text-to-Speech"]
)


tts_service = TTSService()


class TTSRequest(BaseModel):
    text: str
    language: str = "en"


@router.post("/generate")
async def generate_audio(request: TTSRequest):

    try:

        result = tts_service.generate_audio(
            text=request.text,
            language=request.language,
            filename="tts_output"
        )

        return {
            "success": True,
            "message": "Audio generated successfully",
            "files": result["files"],
            "language": result["language"],
            "language_name": result["language_name"],
            "audio_urls": [
                f"/tts/audio/{filename}"
                for filename in result["files"]
            ]
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Audio generation failed: {str(e)}"
        )


@router.get("/audio/{filename}")
async def get_audio(filename: str):

    file_path = (
        tts_service.audio_folder / filename
    )

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Audio file not found."
        )

    return FileResponse(
        path=str(file_path),
        media_type="audio/mpeg",
        filename=filename
    )