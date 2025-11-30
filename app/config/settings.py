from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """
    Application settings (Azure OpenAI ONLY).
    Loaded automatically from .env file.
    """

    # App info
    APP_NAME: str = "AI Code-to-Architecture Visualizer"
    ENV: str = "development"

    # Upload directories
    UPLOAD_DIR_FILES: str = "uploaded_files"
    UPLOAD_DIR_ZIPS: str = "uploaded_zips"

    # Logs
    LOG_DIR: str = "logs"

    # ----------------------------------------------------------
    # Azure OpenAI ONLY
    # ----------------------------------------------------------
    AZURE_OPENAI_KEY: str | None = None
    AZURE_OPENAI_ENDPOINT: str | None = None  # e.g. https://my-resource.openai.azure.com/
    AZURE_OPENAI_DEPLOYMENT_NAME: str | None = None  # e.g. gpt-4o-mini

    model_config = ConfigDict(extra="ignore", env_file=".env")


def get_settings() -> Settings:
    """
    Returns settings instance.
    Automatically caches & reloads values from `.env`.
    """
    return Settings()
