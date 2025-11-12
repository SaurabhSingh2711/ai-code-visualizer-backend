# app/routes/analyze.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser_service import parse_code_from_text
from app.utils.file_utils import save_upload_file_temp

router = APIRouter()

@router.post("/")
async def analyze_code(file: UploadFile = File(...)):
    """
    Accepts a single source file upload (.py or .java).
    Returns parsed JSON with classes, functions and imports.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Save file temporarily (useful if you want to handle zip extraction later)
    temp_path = await save_upload_file_temp(file)

    try:
        content = None
        # read in-memory content (safe for single files)
        file_content = await file.read()
        try:
            content = file_content.decode("utf-8")
        except Exception:
            # fallback in case of other encodings
            content = file_content.decode("latin-1")

        # detect language from filename
        filename = file.filename.lower()
        if filename.endswith(".py"):
            language = "python"
        elif filename.endswith(".java"):
            language = "java"
        else:
            language = "unknown"

        if language == "unknown":
            raise HTTPException(status_code=400, detail="Unsupported file type. Use .py or .java")

        result = parse_code_from_text(content, language)
        return {
            "filename": file.filename,
            "language": language,
            "analysis": result
        }
    finally:
        # optional: remove temp file if created
        try:
            import os
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass
