from fastapi import APIRouter, HTTPException, Body
from app.services.ai_service import generate_ai_insights

router = APIRouter()

@router.post("/ai-analyze/")
async def ai_analyze(payload: dict = Body(...)):
    parsed = payload.get("parsed_data")
    arch = payload.get("architecture_data")
    use_llm = payload.get("use_llm", False)

    if parsed is None or arch is None:
        raise HTTPException(status_code=400, detail="parsed_data and architecture_data required")

    return {
        "ai_output": generate_ai_insights(parsed, arch, use_llm)
    }
