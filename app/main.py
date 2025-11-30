from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings

# Import routers from routes package
from app.routes import health_router, upload_router, analysis_router

# Logger
from app.utilities.logger import logger


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        description="AI Code-to-Architecture Visualizer Backend (Minimal Mode)"
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # REGISTER ROUTERS
    app.include_router(health_router)
    app.include_router(upload_router)
    app.include_router(analysis_router)

    @app.on_event("startup")
    async def startup_event():
        logger.info("BACKEND STARTED ✔")
        logger.info(f"Environment: {settings.ENV}")

    return app


app = create_app()
