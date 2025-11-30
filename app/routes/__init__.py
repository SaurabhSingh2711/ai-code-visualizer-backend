from .health_routes import health_router
from .upload_routes import upload_router
from .analysis_routes import analysis_router

__all__ = [
    "health_router",
    "upload_router",
    "analysis_router",
]
