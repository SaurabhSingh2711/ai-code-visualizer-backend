# app/utils/compress_utils.py

"""
Utility helpers for compressing and optimizing architecture graphs.
Day-12: Used by architecture_service.py
"""

# ---------------------------------------------------------
# Remove duplicate nodes (same id)
# ---------------------------------------------------------
def dedupe_nodes(nodes: list):
    seen = set()
    unique = []
    for n in nodes:
        if n["id"] not in seen:
            seen.add(n["id"])
            unique.append(n)
    return unique


# ---------------------------------------------------------
# Remove duplicate edges (same from → to → relation)
# ---------------------------------------------------------
def dedupe_edges(edges: list):
    seen = set()
    unique = []
    for e in edges:
        key = (e["from"], e["to"], e["relation"])
        if key not in seen:
            seen.add(key)
            unique.append(e)
    return unique


# ---------------------------------------------------------
# Minify a node for frontend transport
# (remove heavy or unnecessary fields)
# ---------------------------------------------------------
def minimize_node(node: dict):
    return {
        "id": node["id"],
        "l": node.get("label"),
        "t": node.get("type"),
        "f": node.get("file"),
    }


# ---------------------------------------------------------
# Minify an edge for frontend transport
# ---------------------------------------------------------
def minimize_edge(edge: dict):
    return {
        "f": edge["from"],
        "t": edge["to"],
        "r": edge["relation"],
        "k": edge.get("type"),
    }
