# app/routes/report.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ai_service import generate_full_ai_insights
from app.services.parser_service import parse_code_from_text
from app.services.architecture_service import build_architecture_map

router = APIRouter()


@router.post("/report/")
async def generate_report(file: UploadFile = File(...), use_llm: bool = False):
    """
    Generates a full AI-powered report from a single file:
    - Parsing
    - Architecture extraction
    - AI static insights
    - OPTIONAL: LLM architectural reasoning
    """

    if not (file.filename.endswith(".py") or file.filename.endswith(".java")):
        raise HTTPException(
            status_code=400, detail="Only .py and .java files are supported."
        )

    code = (await file.read()).decode("utf-8", errors="ignore")
    language = "python" if file.filename.endswith(".py") else "java"

    parsed = parse_code_from_text(code, language)
    arch = build_architecture_map(parsed)

    # Call unified AI engine
    ai_output = generate_full_ai_insights(parsed, arch, use_llm=use_llm)

    return {
        "filename": file.filename,
        "language": language,
        "parsed": parsed,
        "architecture": arch,
        "ai_report": ai_output
    }
