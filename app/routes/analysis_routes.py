from fastapi import APIRouter

analysis_router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

@analysis_router.get("/test")
async def test_analysis():
    return {
        "status": "analysis route working",
        "message": "LLM services not yet enabled — backend is running in minimal mode"
    }
