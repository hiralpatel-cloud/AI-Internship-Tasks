from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    APP_NAME: str = "Intelligent Document Q&A Assistant"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    GOOGLE_API_KEY: str
    GEMINI_MODEL: str = "gemini-3.6-flash"

    UPLOAD_FOLDER: str = str(BASE_DIR / "uploads")
    CHROMA_DB_PATH: str = str(BASE_DIR / "chroma_db")
    LOG_FOLDER: str = str(BASE_DIR / "logs")

    MAX_FILE_SIZE_MB: int = 25

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

Path(settings.UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
Path(settings.CHROMA_DB_PATH).mkdir(parents=True, exist_ok=True)
Path(settings.LOG_FOLDER).mkdir(parents=True, exist_ok=True)
