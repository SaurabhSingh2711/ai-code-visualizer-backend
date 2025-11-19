# app/routes/multi_analyze.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.file_utils import extract_zip_to_temp, cleanup_temp_dir
from app.services.parser_service import parse_code_from_text
from app.services.architecture_service import (
    build_architecture_map,
    build_system_architecture,
)
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
    Day-9 & Day-10: Full multi-file project analysis
    """

    # Step 1 — Validate zip
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Please upload a .zip file")

    # Step 2 — Extract
    extract_path = extract_zip_to_temp(file)

    parsed_results = {}

    # Step 3 — Parse all files
    for root, dirs, files in os.walk(extract_path):
        for fname in files:
            if fname.endswith(".py") or fname.endswith(".java"):
                full_path = os.path.join(root, fname)

                with open(full_path, "r", errors="ignore") as f:
                    code_text = f.read()

                language = "python" if fname.endswith(".py") else "java"

                parsed_output = parse_code_from_text(code_text, language)
                parsed_output["raw_text"] = code_text  # Required for detection

                parsed_results[fname] = parsed_output

    # Step 4 — Merge project summary
    merged = merge_project_data(parsed_results)

    # Step 5 — Cross-file relations
    relations = detect_cross_file_relations(parsed_results)

    # Step 6 — Subsystems
    subsystems = detect_subsystems(parsed_results)

    # Step 7 — Layers
    layers = detect_layers(parsed_results)

    # Step 8 — Service calls (service → service)
    service_calls = detect_service_calls(parsed_results)

    # Step 9 — Build final system architecture graph
    system_architecture = build_system_architecture(
        parsed_results,
        relations,
        subsystems,
        layers,
        service_calls
    )

    # Step 10 — Layout for UI graph display
    layout = generate_layout(system_architecture)

    # Step 11 — Cleanup temporary workspace
    cleanup_temp_dir(extract_path)

    # Step 12 — Final return
    return {
        "parsed_files": parsed_results,
        "system_summary": merged,
        "cross_file_relations": relations,
        "subsystems": subsystems,
        "layers": layers,
        "service_calls": service_calls,
        "architecture": system_architecture,
        "layout": layout,
    }
