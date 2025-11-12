from pydantic import BaseModel
from typing import List, Dict, Optional

class InsightResult(BaseModel):
    summary: str
    hints: List[str]
    metrics: Dict[str, int]
