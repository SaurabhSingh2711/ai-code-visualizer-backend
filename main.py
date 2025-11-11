from fastapi import FastAPI
from app.routes import analyze, insight

app = FastAPI(
    title="AI Code-to-Architecture Visualizer Backend",
    description="Backend API to parse source code and generate architecture diagrams",
    version="1.0.0"
)

app.include_router(analyze.router, prefix="/api/analyze", tags=["Analyze"])
app.include_router(insight.router, prefix="/api/insight", tags=["Insights"])

@app.get("/")
def root():
    return {"message": "AI Code-to-Architecture Visualizer Backend Running ✅"}
