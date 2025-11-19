# app/services/architecture_service.py

"""
Architecture building services for:
- Single-file analysis (Day 5)
- Multi-file system architecture (Day 10+)
"""

def build_architecture_map(parsed_data: dict):
    """
    Day-5:
    Build architecture graph from a single parsed file.
    parsed_data should contain:
    - classes
    - functions
    - imports
    """

    nodes = []
    edges = []

    # Classes
    for cls in parsed_data.get("classes", []):
        nodes.append({
            "id": f"class:{cls}",
            "label": cls,
            "type": "class"
        })

    # Functions
    for func in parsed_data.get("functions", []):
        nodes.append({
            "id": f"func:{func}",
            "label": func,
            "type": "function"
        })

    # Imports
    for imp in parsed_data.get("imports", []):
        nodes.append({
            "id": f"import:{imp}",
            "label": imp,
            "type": "import"
        })

    # Simple edges: import → class/function usage (base version)
    for imp in parsed_data.get("imports", []):
        for cls in parsed_data.get("classes", []):
            edges.append({
                "from": f"import:{imp}",
                "to": f"class:{cls}",
                "relation": "uses"
            })
        for func in parsed_data.get("functions", []):
            edges.append({
                "from": f"import:{imp}",
                "to": f"func:{func}",
                "relation": "uses"
            })

    summary = (
        f"{len(nodes)} nodes, {len(edges)} relationships "
        f"({len(parsed_data.get('classes', []))} classes, "
        f"{len(parsed_data.get('functions', []))} functions, "
        f"{len(parsed_data.get('imports', []))} imports)"
    )

    return {
        "nodes": nodes,
        "edges": edges,
        "summary": summary
    }


# ---------------------------------------------------------------------
# ❇️ DAY-10 / DAY-11: Complete multi-file system architecture builder
# ---------------------------------------------------------------------

def build_system_architecture(
    parsed_files: dict,
    cross_relations: list,
    subsystems: dict,
    layers: dict,
    service_calls: list
):
    """
    Build a project-wide full architecture graph.

    Combines:
    ✔ classes/functions/imports from all files
    ✔ cross-file relations (imports, references)
    ✔ subsystem grouping
    ✔ layered architecture detection
    ✔ service-to-service calls
    """

    nodes = []
    edges = []

    # ------------------------------------------------------------
    # 1. Create nodes for each file's classes/functions/imports
    # ------------------------------------------------------------
    for fname, pdata in parsed_files.items():

        for cls in pdata.get("classes", []):
            nodes.append({
                "id": f"class:{cls}:{fname}",
                "label": cls,
                "type": "class",
                "file": fname
            })

        for func in pdata.get("functions", []):
            nodes.append({
                "id": f"func:{func}:{fname}",
                "label": func,
                "type": "function",
                "file": fname
            })

        for imp in pdata.get("imports", []):
            nodes.append({
                "id": f"import:{imp}:{fname}",
                "label": imp,
                "type": "import",
                "file": fname
            })

    # ------------------------------------------------------------
    # 2. Add edges for cross-file relations
    # ------------------------------------------------------------
    for rel in cross_relations:
        edges.append({
            "from": rel["from"],
            "to": rel["to"],
            "relation": rel["relation"],
            "type": "cross-file"
        })

    # ------------------------------------------------------------
    # 3. Subsystem grouping: file → subsystem
    # ------------------------------------------------------------
    for subsystem_name, file_list in subsystems.items():
        for f in file_list:
            edges.append({
                "from": f,
                "to": subsystem_name,
                "relation": "belongs-to-subsystem",
                "type": "subsystem"
            })

    # ------------------------------------------------------------
    # 4. Layered architecture grouping
    # ------------------------------------------------------------
    for layer_name, file_list in layers.items():
        for f in file_list:
            edges.append({
                "from": f,
                "to": layer_name,
                "relation": "belongs-to-layer",
                "type": "layer"
            })

    # ------------------------------------------------------------
    # 5. Service-to-service communication edges
    # ------------------------------------------------------------
    for svc in service_calls:
        edges.append({
            "from": svc["from"],
            "to": svc["to"],
            "relation": svc["relation"],
            "type": "service-call"
        })

    # ------------------------------------------------------------
    # Final system architecture graph
    # ------------------------------------------------------------
    summary = f"{len(nodes)} nodes, {len(edges)} relationships"

    return {
        "nodes": nodes,
        "edges": edges,
        "summary": summary
    }
