# app/routes/multi_analyze.py

from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from app.utils.file_utils import extract_zip_to_temp, cleanup_temp_dir
from app.services.parser_service import parse_code_from_text
from app.services.architecture_service import build_system_architecture
from app.services.layout_service import generate_layout

from app.services.system_insight_service import (
    merge_project_data,
    detect_cross_file_relations,
    clean_parsed_output
)

from app.services.subsystem_service import (
    detect_subsystems,
    detect_layers,
    detect_service_calls
)

from app.services.cache_service import compute_hash, get_from_cache, store_in_cache

router = APIRouter()


@router.post("/multi-analyze/")
async def analyze_project_zip(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Please upload a .zip file")

    extract_path = extract_zip_to_temp(file)

    parsed_results = {}

    # walk files
    for root, dirs, files in os.walk(extract_path):
        for fname in files:
            if fname.endswith(".py") or fname.endswith(".java"):
                full = os.path.join(root, fname)
                text = open(full, "r", errors="ignore").read()
                language = "python" if fname.endswith(".py") else "java"

                parsed = parse_code_from_text(text, language)
                parsed["raw_text"] = text

                parsed_results[fname] = parsed

    # compute cache key
    key = compute_hash("".join([str(parsed_results)]))

    # search cache
    cached = get_from_cache(key)
    if cached:
        cleanup_temp_dir(extract_path)
        return cached

    # --- project insights ---
    merged = merge_project_data(parsed_results)
    relations = detect_cross_file_relations(parsed_results)
    subsystems = detect_subsystems(parsed_results)
    layers = detect_layers(parsed_results)
    service_calls = detect_service_calls(parsed_results)

    # --- architecture ---
    architecture = build_system_architecture(
        parsed_results,
        relations,
        subsystems,
        layers,
        service_calls
    )

    layout = generate_layout(architecture)

    # Create frontend-safe JSON
    response = {
        "parsed_files": clean_parsed_output(parsed_results),
        "system_summary": merged,
        "cross_file_relations": relations,
        "subsystems": subsystems,
        "layers": layers,
        "service_calls": service_calls,
        "architecture": architecture,
        "layout": layout,
    }

    # store in cache
    store_in_cache(key, response)

    # cleanup
    cleanup_temp_dir(extract_path)

    return response
