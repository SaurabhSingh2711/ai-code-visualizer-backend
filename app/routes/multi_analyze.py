# app/routes/multi_analyze.py

from fastapi import APIRouter, UploadFile, File, HTTPException
import os

from app.utils.file_utils import extract_zip_to_temp, cleanup_temp_dir
from app.services.parser_service import parse_code_from_text
from app.services.system_insight_service import (
    merge_project_data,
    detect_cross_file_relations
)
from app.services.subsystem_service import (
    detect_subsystems,
    detect_layers,
    detect_service_calls
)
from app.services.architecture_service import build_system_architecture
from app.services.layout_service import generate_layout
from app.services.ai_service import generate_full_ai_insights  

router = APIRouter()


@router.post("/multi-analyze/")
async def analyze_project_zip(file: UploadFile = File(...), use_llm: bool = False):
    """
    Full multi-file project analysis (Day-13 Ready)
    """

    # Step 1: Validate input
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Please upload a .zip file")

    # Step 2: Extract ZIP
    extract_path = extract_zip_to_temp(file)
    parsed_results = {}

    # Step 3: Walk and parse source files (Python & Java)
    for root, dirs, files in os.walk(extract_path):
        for fname in files:
            if fname.endswith(".py") or fname.endswith(".java"):
                full_path = os.path.join(root, fname)
                with open(full_path, "r", errors="ignore") as f:
                    code_text = f.read()

                language = "python" if fname.endswith(".py") else "java"
                parsed = parse_code_from_text(code_text, language)
                parsed["raw_text"] = code_text

                parsed_results[fname] = parsed

    # Step 4: Merge project summary
    merged = merge_project_data(parsed_results)

    # Step 5: Cross-file relations
    cross_relations = detect_cross_file_relations(parsed_results)

    # Step 6: Subsystems (controller / service / util)
    subsystems = detect_subsystems(parsed_results)

    # Step 7: Layers (app / service / data / util)
    layers = detect_layers(parsed_results)

    # Step 8: Service call graph
    service_calls = detect_service_calls(parsed_results)

    # Step 9: Build unified architecture graph
    architecture = build_system_architecture(
        parsed_results,
        cross_relations,
        subsystems,
        layers,
        service_calls
    )

    # Step 10: Layout for frontend
    layout = generate_layout(architecture)

    # Step 11: AI Insights (Day-13)
    ai_insights = generate_full_ai_insights(
        parsed=merged["combined"],
        architecture=architecture,
        use_llm=use_llm
    )

    # Step 12: Clean up
    cleanup_temp_dir(extract_path)

    # Step 13: Return final response
    return {
        "parsed_files": parsed_results,
        "system_summary": merged,
        "cross_file_relations": cross_relations,
        "subsystems": subsystems,
        "layers": layers,
        "service_calls": service_calls,
        "architecture": architecture,
        "layout": layout,
        "ai_insights": ai_insights
    }
