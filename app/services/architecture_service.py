# app/services/architecture_service.py

"""
Architecture builders:
- Day-5: Single-file architecture (cleaned & optimized in Day-12)
- Day-10/11: Multi-file system architecture
"""

# ⬇️ NEW IMPORTS for Day-12 compression
from app.utils.compress_utils import (
    dedupe_nodes,
    dedupe_edges,
    minimize_node,
    minimize_edge
)

# ===================================================================
# ✅ DAY-12 — Optimized Single-File Architecture Builder
# ===================================================================
def build_architecture_map(parsed_data: dict):
    """
    Build optimized, compressed architecture graph from a single file.
    Used in Day-5 and for single-file analysis endpoint.
    """

    nodes = []
    edges = []

    # -----------------------------
    # Nodes
    # -----------------------------
    for cls in parsed_data.get("classes", []):
        nodes.append({"id": f"class:{cls}", "label": cls, "type": "class"})

    for func in parsed_data.get("functions", []):
        nodes.append({"id": f"func:{func}", "label": func, "type": "function"})

    for imp in parsed_data.get("imports", []):
        nodes.append({"id": f"import:{imp}", "label": imp, "type": "import"})

    # -----------------------------
    # Edges (simple relationships)
    # -----------------------------
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

    # -----------------------------
    # DAY-12 Optimization
    # -----------------------------
    nodes = dedupe_nodes(nodes)
    edges = dedupe_edges(edges)

    nodes = [minimize_node(n) for n in nodes]
    edges = [minimize_edge(e) for e in edges]

    return {
        "nodes": nodes,
        "edges": edges,
        "summary": f"{len(nodes)} nodes, {len(edges)} edges"
    }


# ===================================================================
# ✅ DAY-10/11 — Multi-File System Architecture Builder
# ===================================================================
def build_system_architecture(
    parsed_files: dict,
    cross_relations: list,
    subsystems: dict,
    layers: dict,
    service_calls: list
):
    """
    Project-wide architecture graph.
    Combines classes/functions/imports + relationships across all files.
    """

    nodes = []
    edges = []

    # ------------------------------------------------------------
    # 1. Create nodes for each file’s classes/functions/imports
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
    # 2. Cross-file relations (imports, references)
    # ------------------------------------------------------------
    for rel in cross_relations:
        edges.append({
            "from": rel["from"],
            "to": rel["to"],
            "relation": rel["relation"],
            "type": "cross-file"
        })

    # ------------------------------------------------------------
    # 3. Subsystem grouping
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
    # 4. Layer grouping
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
    # 5. Service-to-service call graph
    # ------------------------------------------------------------
    for svc in service_calls:
        edges.append({
            "from": svc["from"],
            "to": svc["to"],
            "relation": svc["relation"],
            "type": "service-call"
        })

    # ------------------------------------------------------------
    summary = f"{len(nodes)} nodes, {len(edges)} relationships"

    return {
        "nodes": nodes,
        "edges": edges,
        "summary": summary
    }
