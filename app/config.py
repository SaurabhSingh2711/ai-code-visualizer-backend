from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AI Code-to-Architecture Visualizer"
    ENV: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
