from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.utils.file_utils import save_upload_file_temp
from app.services.parser_service import parse_code_from_text
from app.services.architecture_service import build_architecture_map
from app.services.layout_service import generate_layout
from app.services.ai_service import generate_ai_insights


router = APIRouter()   # IMPORTANT


@router.post("/report/")
async def generate_full_report(
    file: UploadFile = File(...),
    use_llm: bool = Form(False)
):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    temp_path = await save_upload_file_temp(file)

    try:
        file_bytes = await file.read()
        code_text = file_bytes.decode("utf-8", errors="ignore")

        filename = file.filename.lower()

        # Detect language
        if filename.endswith(".py"):
            language = "python"
        elif filename.endswith(".java"):
            language = "java"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type (.py or .java only)")

        # Step 1 — Parse
        parsed = parse_code_from_text(code_text, language)

        # Step 2 — Architecture
        architecture = build_architecture_map(parsed)

        # Step 3 — Layout
        layout = generate_layout(architecture)

        # Step 4 — AI (optional)
        ai = generate_ai_insights(parsed, architecture, use_llm)

        return {
            "filename": file.filename,
            "language": language,
            "parsed": parsed,
            "architecture": architecture,
            "layout": layout,
            "ai": ai
        }

    finally:
        import os
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
