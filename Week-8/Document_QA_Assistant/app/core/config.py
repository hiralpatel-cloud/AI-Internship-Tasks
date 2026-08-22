from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ==========================================================
    # APPLICATION
    # ==========================================================

    APP_NAME: str = "Intelligent Document Q&A Assistant"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    # ==========================================================
    # GOOGLE GEMINI
    # ==========================================================

    GOOGLE_API_KEY: str

    GEMINI_MODEL: str = "gemini-3.6-flash"

    # ==========================================================
    # CHROMADB
    # ==========================================================

    CHROMA_DB_PATH: str = "chroma_db"

    CHROMA_COLLECTION_NAME: str = "document_chunks"

    # ==========================================================
    # FILE UPLOAD
    # ==========================================================

    UPLOAD_FOLDER: str = "uploads"

    MAX_FILE_SIZE_MB: int = 25

    # ==========================================================
    # LOGGING
    # ==========================================================

    LOG_LEVEL: str = "INFO"

    # ==========================================================
    # PYDANTIC SETTINGS
    # ==========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()