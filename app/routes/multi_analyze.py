from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_utils import extract_zip_to_temp, cleanup_temp_dir
from app.services.parser_service import parse_code_from_text
from app.services.architecture_service import build_architecture_map
from app.services.layout_service import generate_layout
from app.services.system_insight_service import (
    build_system_insights,
    detect_cross_file_relations
)
import os

router = APIRouter()

@router.post("/multi-analyze/")
async def analyze_project_zip(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Please upload a .zip file")

    # Extract uploaded ZIP
    extract_path = extract_zip_to_temp(file)
    parsed_results = {}

    # Parse each file in the project
    for root, dirs, files in os.walk(extract_path):
        for fname in files:
            if fname.endswith(".py") or fname.endswith(".java"):
                full_path = os.path.join(root, fname)
                code_text = open(full_path, "r", errors="ignore").read()

                language = "python" if fname.endswith(".py") else "java"
                parsed_output = parse_code_from_text(code_text, language)

                # Required for cross-file class/function scanning
                parsed_output["raw_text"] = code_text

                parsed_results[fname] = parsed_output

    # STEP 1 — SYSTEM LEVEL ANALYSIS (Day-9)
    system_summary = build_system_insights(parsed_results)

    # STEP 2 — CROSS FILE RELATIONS (Day-9)
    cross_relations = detect_cross_file_relations(parsed_results)

    # STEP 3 — build architecture + layout (Day 5–7)
    architecture = build_architecture_map(system_summary["combined"])
    layout = generate_layout(architecture)

    cleanup_temp_dir(extract_path)

    return {
        "parsed_files": parsed_results,
        "system_summary": system_summary,
        "cross_file_relations": cross_relations,
        "architecture": architecture,
        "layout": layout
    }
