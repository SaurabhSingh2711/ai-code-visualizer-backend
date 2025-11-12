"""
insight.py
----------
Provides insights on previously parsed + mapped architecture data.
"""

from fastapi import APIRouter, HTTPException, Body
from app.services.insight_service import generate_insights

router = APIRouter()

@router.post("/insight/")
async def get_insights(payload: dict = Body(...)):
    """
    Expects:
    {
      "parsed_data": {...},
      "architecture_data": {...}
    }
    Returns AI-style insight summary and metrics.
    """
    try:
        parsed_data = payload.get("parsed_data", {})
        architecture_data = payload.get("architecture_data", {})
        if not parsed_data:
            raise HTTPException(status_code=400, detail="Missing parsed_data")

        insights = generate_insights(parsed_data, architecture_data)
        return {
            "insights": insights,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")
