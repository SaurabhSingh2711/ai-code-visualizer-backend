# app/routes/analyze.py
"""
Day-2: Analyze Route (final version)
-----------------------------------
Accepts .py or .java source files, extracts class/function/import
details using parser_service.py, and returns clean JSON output.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser_service import parse_code_from_text
import os
import tempfile
import logging

router = APIRouter()

# basic logger setup (or integrate with app/core/logger.py)
logger = logging.getLogger(__name__)

@router.post("/")
async def analyze_code(file: UploadFile = File(...)):
    """
    Upload a single source code file (.py or .java).
    Returns JSON containing extracted architecture info.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    temp_path = None
    try:
        # Read the uploaded file into memory once
        file_content = await file.read()
        if not file_content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        # Decode content safely (UTF-8 preferred, fallback to Latin-1)
        try:
            content = file_content.decode("utf-8")
        except UnicodeDecodeError:
            content = file_content.decode("latin-1")

        # Optionally save a temporary file copy (useful for debugging or zip uploads later)
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            tmp.write(file_content)
            temp_path = tmp.name

        # Detect language automatically
        filename = file.filename.lower()
        if filename.endswith(".py"):
            language = "python"
        elif filename.endswith(".java"):
            language = "java"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use .py or .java")

        # Log for debugging
        logger.info(f"Analyzing file: {file.filename} (language={language}) size={len(content)} bytes")

        # Call your parsing service
        result = parse_code_from_text(content, language)

        # Handle parsing-level errors gracefully
        if "error" in result:
            raise HTTPException(status_code=500, detail=result.get("error", "Parsing failed"))

        # Return structured JSON
        return {
            "filename": file.filename,
            "language": language,
            "analysis": result
        }

    except HTTPException:
        raise  # rethrow cleanly for FastAPI to handle
    except Exception as e:
        logger.exception("Unexpected error during code analysis")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        # Cleanup any temporary file created
        try:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception as cleanup_err:
            logger.warning(f"Temp cleanup failed: {cleanup_err}")
