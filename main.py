from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import route modules
from app.routes import (
    analyze,
    multi_analyze,
    report,
    visualize,
    insight
)

app = FastAPI(
    title="AI Code-to-Architecture Visualizer",
    version="1.0.0"
)

# API versioning prefix
API_PREFIX = "/api/v1"

# CORS (not required but recommended)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # allow frontend to access backend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register backend route modules
app.include_router(analyze.router, prefix=API_PREFIX)
app.include_router(insight.router, prefix=API_PREFIX)
app.include_router(visualize.router, prefix=API_PREFIX)
app.include_router(report.router, prefix=API_PREFIX)
app.include_router(multi_analyze.router, prefix=API_PREFIX)

@app.get("/")
async def root():
    return {"message": "AI Code Visualizer backend is running"}
