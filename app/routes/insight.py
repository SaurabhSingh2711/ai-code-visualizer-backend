# app/routes/insight.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_insights():
    return {"message": "Insight endpoint ready (Day-2 placeholder)"}
