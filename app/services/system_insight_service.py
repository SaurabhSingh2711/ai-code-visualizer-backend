# app/services/system_insight_service.py

import os
from typing import Dict, Any, List


# ----------------------------------------------------------
# MAIN ENTRY: Build system-level insights for ZIP project
# ----------------------------------------------------------
def build_system_insights(parsed_results: Dict[str, Any]) -> Dict[str, Any]:
    files = list(parsed_results.keys())

    # Extract combined metrics
    combined = {
        "classes": [],
        "functions": [],
        "imports": []
    }

    for fname, data in parsed_results.items():
        combined["classes"].extend(data.get("classes", []))
        combined["functions"].extend(data.get("functions", []))
        combined["imports"].extend(data.get("imports", []))

    # Detect cross-file relationships
    cross_file_relations = detect_cross_file_relations(parsed_results)

    return {
        "summary": f"Parsed project → {len(combined['classes'])} classes, "
                   f"{len(combined['functions'])} functions, "
                   f"{len(combined['imports'])} imports",

        "combined": combined,

        "cross_file_relations": cross_file_relations
    }


# ----------------------------------------------------------
# CROSS-FILE SCAN
# ----------------------------------------------------------
def detect_cross_file_relations(parsed_results: Dict[str, Any]) -> List[Dict[str, str]]:
    relations = []

    files = list(parsed_results.keys())

    for fname in files:
        current = parsed_results[fname]
        current_imports = current.get("imports", [])
        current_text = current.get("raw_text", "") or ""

        # Normalize
        current_imports = [i.strip() for i in current_imports]

        for other_file in files:
            if other_file == fname:
                continue

            other = parsed_results[other_file]

            other_classes = other.get("classes", [])
            other_functions = other.get("functions", [])
            other_imports = other.get("imports", [])

            other_text = other.get("raw_text", "") or ""

            # -----------------------------------------------------
            # 1. IMPORT-BASED RELATION (improved handling)
            # -----------------------------------------------------
            for imp in current_imports:
                imp_parts = imp.split(".")      # utils.helpers → ["utils", "helpers"]

                # Match against real filename without extension
                target_base = os.path.splitext(other_file)[0].lower()

                for part in imp_parts:
                    if part.lower() == target_base:
                        relations.append({
                            "from": fname,
                            "to": other_file,
                            "relation": f"imports-module:{imp}"
                        })

            # -----------------------------------------------------
            # 2. CROSS-FILE CLASS REFERENCE (text-based matching)
            # -----------------------------------------------------
            for cls in other_classes:
                if cls in current_text:
                    relations.append({
                        "from": fname,
                        "to": other_file,
                        "relation": f"references-class:{cls}"
                    })

            # -----------------------------------------------------
            # 3. CROSS-FILE FUNCTION REFERENCE
            # -----------------------------------------------------
            for fn in other_functions:
                if fn in current_text:
                    relations.append({
                        "from": fname,
                        "to": other_file,
                        "relation": f"references-function:{fn}"
                    })

    # Deduplicate relations
    unique = []
    seen = set()

    for r in relations:
        key = f"{r['from']}->{r['to']}:{r['relation']}"
        if key not in seen:
            seen.add(key)
            unique.append(r)

    return unique
