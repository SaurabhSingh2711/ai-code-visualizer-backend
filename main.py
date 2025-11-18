from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.routes import (
    analyze,
    insight,
    visualize,
    ai_analyze,
    report,
    multi_analyze
)

app = FastAPI(
    title="AI Code-to-Architecture Visualizer",
    version="1.0.0"
)

API_PREFIX = "/api/v1"

app.include_router(analyze.router, prefix=API_PREFIX)
app.include_router(insight.router, prefix=API_PREFIX)
app.include_router(visualize.router, prefix=API_PREFIX)
app.include_router(ai_analyze.router, prefix=API_PREFIX)
app.include_router(report.router, prefix=API_PREFIX)
app.include_router(multi_analyze.router, prefix=API_PREFIX)

@app.get("/")
async def root():
    return {"message": "AI Code Visualizer backend is running"}
