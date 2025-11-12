from fastapi import FastAPI
#from app.routes.analyze import router as analyze_router

from app.routes import analyze, insight   #  import both routes

app = FastAPI(
    title="AI Code-to-Architecture Visualizer",
    version="1.0.0"
)

# ✅ Register both routers under /api prefix
app.include_router(analyze.router, prefix="/api")
app.include_router(insight.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "AI Code Visualizer backend is running"}



