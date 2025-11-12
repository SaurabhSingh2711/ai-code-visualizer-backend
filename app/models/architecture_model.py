# app/models/architecture_model.py
from pydantic import BaseModel
from typing import List, Dict, Any

class ModuleAnalysis(BaseModel):
    classes: List[str]
    functions: List[str]
    imports: List[str]
    summary: str

class AnalysisResponse(BaseModel):
    filename: str
    language: str
    analysis: ModuleAnalysis
