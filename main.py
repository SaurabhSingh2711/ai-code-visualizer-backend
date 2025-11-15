from fastapi import FastAPI
from app.routes import analyze, insight, visualize   # ONLY Day 1–5 routes

app = FastAPI(
    title="AI Code-to-Architecture Visualizer",
    version="1.0.0"
)

API_PREFIX = "/api/v1"

# Register available routers (Day 1–5 ONLY)
app.include_router(analyze.router, prefix=API_PREFIX)
app.include_router(insight.router, prefix=API_PREFIX)
app.include_router(visualize.router, prefix=API_PREFIX)

@app.get("/")
async def root():
    return {"message": "AI Code Visualizer backend is running"}
