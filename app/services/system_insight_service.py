# app/services/system_insight_service.py

import re

############################################################
# DAY-9 — MERGING SYSTEM DATA
############################################################

def merge_project_data(parsed_files: dict):
    """
    Combine classes, functions, and imports across all files.
    """
    all_classes = []
    all_functions = []
    all_imports = []

    for fname, data in parsed_files.items():
        all_classes.extend(data.get("classes", []))
        all_functions.extend(data.get("functions", []))
        all_imports.extend(data.get("imports", []))

    summary = {
        "summary": f"Parsed project → {len(all_classes)} classes, {len(all_functions)} functions, {len(all_imports)} imports",
        "combined": {
            "classes": all_classes,
            "functions": all_functions,
            "imports": all_imports
        }
    }

    return summary


############################################################
# DAY-9 — CROSS-FILE DEPENDENCY DETECTION
############################################################

def detect_cross_file_relations(parsed_files: dict):
    """
    Detect inter-file relationships such as:
    - imports-module
    - references-class
    - references-function
    """
    relations = []

    for file_a, data_a in parsed_files.items():
        raw = data_a.get("raw_text", "")

        for file_b, data_b in parsed_files.items():
            if file_a == file_b:
                continue

            # Module-based linking
            for imp in data_a.get("imports", []):
                module_name = imp.split(".")[-1] + ".py"
                if module_name == file_b:
                    relations.append({
                        "from": file_a,
                        "to": file_b,
                        "relation": f"imports-module:{imp}"
                    })

            # Class references
            for cls in data_b.get("classes", []):
                regex = rf"\b{cls}\b"
                if re.search(regex, raw):
                    relations.append({
                        "from": file_a,
                        "to": file_b,
                        "relation": f"references-class:{cls}"
                    })

            # Function references
            for func in data_b.get("functions", []):
                regex = rf"\b{func}\b"
                if re.search(regex, raw):
                    relations.append({
                        "from": file_a,
                        "to": file_b,
                        "relation": f"references-function:{func}"
                    })

    return relations


############################################################
# DAY-10 — SUBSYSTEM DETECTION
############################################################

SUBSYSTEM_KEYWORDS = {
    "controller": ["controller", "api", "router", "endpoint"],
    "service": ["service", "manager"],
    "data": ["db", "database", "repo", "dao"],
    "util": ["util", "helper", "common"]
}

def detect_subsystems(parsed_files: dict):
    groups = {
        "controller": [],
        "service": [],
        "data": [],
        "util": [],
        "unknown": []
    }

    for fname, data in parsed_files.items():
        lowered = fname.lower()

        matched = False
        for group, keywords in SUBSYSTEM_KEYWORDS.items():
            if any(k in lowered for k in keywords):
                groups[group].append(fname)
                matched = True
                break

        if not matched:
            groups["unknown"].append(fname)

    return groups


############################################################
# DAY-10 — ARCHITECTURE LAYER DETECTION
############################################################

LAYER_RULES = {
    "app_layer": ["controller", "api"],
    "service_layer": ["service"],
    "data_layer": ["db", "repo", "dao"],
    "utility_layer": ["util", "helper"]
}

def detect_layers(parsed_files: dict):
    layers = {
        "app_layer": [],
        "service_layer": [],
        "data_layer": [],
        "utility_layer": [],
        "unknown_layer": []
    }

    for fname in parsed_files.keys():
        lowered = fname.lower()

        placed = False
        for layer, keys in LAYER_RULES.items():
            if any(k in lowered for k in keys):
                layers[layer].append(fname)
                placed = True
                break

        if not placed:
            layers["unknown_layer"].append(fname)

    return layers


############################################################
# DAY-10 — SERVICE CALL GRAPH
############################################################

def detect_service_calls(parsed_files: dict):
    call_graph = []

    for file_a, data_a in parsed_files.items():
        raw = data_a.get("raw_text", "")

        for file_b, data_b in parsed_files.items():
            if file_a == file_b:
                continue

            service_name = None
            for cls in data_b.get("classes", []):
                # Example: UserService, PaymentManager
                if "service" in cls.lower() or "manager" in cls.lower():
                    service_name = cls

            if service_name and re.search(rf"\b{service_name}\b", raw):
                call_graph.append({
                    "from": file_a,
                    "to": file_b,
                    "relation": f"calls-service:{service_name}"
                })

    return call_graph

############################################################
# DAY-12 — ONLY RETURN NECESSARY SUMMARY
############################################################

# ---------------------------------------------------------
# DAY-12 — Clean parsed output before building architecture
# ---------------------------------------------------------

def clean_parsed_output(parsed_files: dict) -> dict:
    """
    Cleans the raw parsed output:
    - Removes empty lists (empty classes, functions, imports)
    - Ensures raw_text exists
    - Normalizes structures for safety
    """

    cleaned = {}

    for fname, pdata in parsed_files.items():

        cleaned[fname] = {
            "classes": pdata.get("classes", []) or [],
            "functions": pdata.get("functions", []) or [],
            "imports": pdata.get("imports", []) or [],
            "raw_text": pdata.get("raw_text", ""),
        }

    return cleaned


