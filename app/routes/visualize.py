# app/routes/visualize.py

from fastapi import APIRouter, HTTPException, Body
from app.services.visualizer_service import generate_visual_layout

router = APIRouter()

@router.post("/visualize/")
async def visualize(payload: dict = Body(...)):
    """
    Takes:
    {
      "architecture": {
         "nodes": [...],
         "edges": [...]
      }
    }
    Returns layout (x,y,color,size,zoom_level)
    """
    try:
        arch = payload.get("architecture")

        if arch is None:
            raise HTTPException(status_code=400, detail="Missing 'architecture' in request.")

        return {"layout": generate_visual_layout(arch)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
