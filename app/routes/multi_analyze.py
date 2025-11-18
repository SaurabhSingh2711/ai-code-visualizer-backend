from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_utils import extract_zip_to_temp, cleanup_temp_dir
from app.services.parser_service import parse_code_from_text
from app.services.architecture_service import build_architecture_map
from app.services.layout_service import generate_layout

import os

router = APIRouter()

@router.post("/multi-analyze/")
async def analyze_zip(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # MUST be a ZIP file
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip allowed")

    # Extract temp folder
    temp_dir = extract_zip_to_temp(file)

    combined = {
        "classes": [],
        "functions": [],
        "imports": []
    }

    # Walk through all files
    for root, _, files in os.walk(temp_dir):
        for fname in files:
            path = os.path.join(root, fname)

            # Detect language
            if fname.endswith(".py"):
                lang = "python"
            elif fname.endswith(".java"):
                lang = "java"
            else:
                continue

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()

            parsed = parse_code_from_text(code, lang)

            combined["classes"].extend(parsed.get("classes", []))
            combined["functions"].extend(parsed.get("functions", []))
            combined["imports"].extend(parsed.get("imports", []))

    # Now build architecture + layout
    architecture = build_architecture_map(combined)
    layout = generate_layout(architecture)

    # Cleanup
    cleanup_temp_dir(temp_dir)

    return {
        "summary": (
            f"Parsed project → "
            f"{len(combined['classes'])} classes, "
            f"{len(combined['functions'])} functions, "
            f"{len(combined['imports'])} imports"
        ),
        "combined": combined,
        "architecture": architecture,
        "layout": layout
    }
