# app/routes/multi_analyze.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_utils import extract_zip_to_temp, cleanup_temp_dir
from app.services.parser_service import parse_code_from_text
from app.services.architecture_service import build_architecture_map
from app.services.layout_service import generate_layout

from app.services.system_insight_service import (
    merge_project_data,
    detect_cross_file_relations,
)

from app.services.subsystem_service import (
    detect_subsystems,
    detect_layers,
    detect_service_calls,
)

import os

router = APIRouter()


@router.post("/multi-analyze/")
async def analyze_project_zip(file: UploadFile = File(...)):
    """
    Day-9: Full multi-file project analysis
    - Accepts .zip file
    - Extracts / temp folder
    - Parses all .py / .java files
    - Merges project-level insights
    - Detects cross-file relations
    - Detects subsystems, layers, service calls
    - Produces system-wide architecture + layout
    """

    # Step 1 — Validate zip file
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Please upload a .zip file")

    # Step 2 — Extract ZIP to temp dir
    extract_path = extract_zip_to_temp(file)

    parsed_results = {}

    # Step 3 — Walk extracted folder and parse all source files
    for root, dirs, files in os.walk(extract_path):
        for fname in files:
            if fname.endswith(".py") or fname.endswith(".java"):
                full_path = os.path.join(root, fname)

                with open(full_path, "r", errors="ignore") as f:
                    code_text = f.read()

                language = "python" if fname.endswith(".py") else "java"

                parsed_output = parse_code_from_text(code_text, language)

                # Required for class/function reference detection
                parsed_output["raw_text"] = code_text

                parsed_results[fname] = parsed_output

    # Step 4 — Merge full project summary (Day-9 core feature)
    merged = merge_project_data(parsed_results)

    # Step 5 — Cross-file relations (imports, class/function calls)
    relations = detect_cross_file_relations(parsed_results)

    # Step 6 — Subsystem detection
    subsystems = detect_subsystems(parsed_results)

    # Step 7 — Layered architecture detection
    layers = detect_layers(parsed_results)

    # Step 8 — Service-to-service call graph
    service_calls = detect_service_calls(parsed_results)

    # Step 9 — Build final architecture (Day-10 fix)
    # ----------------------------------------------
    # important: merged["combined"] contains classes/functions/imports
    architecture = build_architecture_map(merged.get("combined", {}))

    # Step 10 — Layout for UI visualization
    layout = generate_layout(architecture)

    # Step 11 — Cleanup temporary folder
    cleanup_temp_dir(extract_path)

    # Step 12 — Return final artifact
    return {
        "parsed_files": parsed_results,
        "system_summary": merged,
        "cross_file_relations": relations,
        "subsystems": subsystems,
        "layers": layers,
        "service_calls": service_calls,
        "architecture": architecture,
        "layout": layout,
    }
