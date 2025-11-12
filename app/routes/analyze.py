from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser_service import parse_code_from_text
from app.services.architecture_service import build_architecture_map
import chardet
import os

router = APIRouter()

@router.post("/analyze/")
async def analyze_code(file: UploadFile = File(...)):
    """
    Accepts a single source file (.py or .java),
    parses its structure and builds an architecture map.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    print(f"[DEBUG] Uploaded filename: {file.filename}")

    #  Read file content
    file_bytes = await file.read()
    print(f"[DEBUG] File size: {len(file_bytes)} bytes")

    if not file_bytes:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

    #  Decode safely with fallback
    try:
        content = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        detected = chardet.detect(file_bytes)
        encoding = detected.get("encoding", "utf-8")
        print(f"[DEBUG] Detected encoding: {encoding}")
        content = file_bytes.decode(encoding, errors="ignore")

    print(f"[DEBUG] First 200 chars of uploaded code:\n{content[:200]}")

    #  Detect language
    filename = file.filename.lower()
    if filename.endswith(".py"):
        language = "python"
    elif filename.endswith(".java"):
        language = "java"
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    #  Parse structure
    parsed_output = parse_code_from_text(content, language)

    #  Build architecture map
    architecture = build_architecture_map(parsed_output)

    #  Respond
    return {
        "filename": file.filename,
        "language": language,
        "parsed_summary": parsed_output.get("summary"),
        "architecture": architecture
    }
