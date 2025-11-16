"""
Day-5 Layout Service
This adds X/Y coordinates, color, size for diagram nodes.
"""

def generate_layout(architecture):
    nodes = architecture.get("nodes", [])
    edges = architecture.get("edges", [])

    layout_nodes = []

    x = 100
    y_start = 100

    for idx, node in enumerate(nodes):
        layout_nodes.append({
            "id": node["id"],
            "label": node["label"],
            "type": node["type"],
            "x": x,
            "y": y_start + (idx * 80),
            "color": "#00E5FF",   # neon blue
            "size": 20
        })
        x += 120  # horizontal spacing

    return {
        "nodes": layout_nodes,
        "edges": edges
    }
