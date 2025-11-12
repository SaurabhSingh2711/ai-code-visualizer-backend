from fastapi import FastAPI
from app.routes.analyze import router as analyze_router

app = FastAPI(
    title="AI Code-to-Architecture Visualizer",
    version="1.0.0"
)

# This line registers your analyzer API
app.include_router(analyze_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI Code Visualizer Backend is running"}

