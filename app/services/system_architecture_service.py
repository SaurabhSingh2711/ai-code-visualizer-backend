# app/services/system_architecture_service.py

def build_system_architecture(parsed_files, cross_file_relations, subsystems, layers, service_calls):
    """
    Build a unified system-wide architecture graph.
    This merges:
    - Parsed classes/functions/imports from each file
    - Cross-file dependencies
    - Service calls
    - Subsystem grouping
    - Layer grouping
    """

    nodes = []
    edges = []

    # -------------------------
    # 1. BUILD ALL NODES
    # -------------------------
    for filename, data in parsed_files.items():
        # Classes
        for cls in data.get("classes", []):
            nodes.append({
                "id": f"class:{cls}",
                "label": cls,
                "type": "class",
                "file": filename
            })

        # Functions
        for fn in data.get("functions", []):
            nodes.append({
                "id": f"func:{fn}",
                "label": fn,
                "type": "function",
                "file": filename
            })

        # Imports
        for imp in data.get("imports", []):
            nodes.append({
                "id": f"import:{imp}",
                "label": imp,
                "type": "import",
                "file": filename
            })

    # -------------------------
    # 2. CROSS-FILE RELATIONS
    # -------------------------
    for rel in cross_file_relations:
        edges.append({
            "from": rel["from"],
            "to": rel["to"],
            "relation": rel["relation"]
        })

    # -------------------------
    # 3. SERVICE CALLS
    # -------------------------
    for sc in service_calls:
        edges.append({
            "from": sc["from"],
            "to": sc["to"],
            "relation": sc["relation"]
        })

    # -------------------------
    # 4. SUBSYSTEM → GROUPING (META)
    # -------------------------
    subsystem_meta = []
    for group, files in subsystems.items():
        for f in files:
            subsystem_meta.append({
                "file": f,
                "subsystem": group
            })

    # -------------------------
    # 5. LAYER TAGGING (META)
    # -------------------------
    layer_meta = []
    for layer, files in layers.items():
        for f in files:
            layer_meta.append({
                "file": f,
                "layer": layer
            })

    return {
        "nodes": nodes,
        "edges": edges,
        "subsystems": subsystem_meta,
        "layers": layer_meta,
        "summary": f"{len(nodes)} nodes, {len(edges)} edges"
    }
