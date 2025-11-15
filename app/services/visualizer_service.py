# app/services/visualizer_service.py

"""
Day-5 Visualization Service
Generates UI-ready coordinates, colors, sizes, and zoom-levels
for architecture nodes.
"""

import math
from typing import Dict, Any

def generate_visual_layout(architecture: Dict[str, Any]) -> Dict[str, Any]:
    nodes = architecture.get("nodes", [])
    edges = architecture.get("edges", [])

    layout_nodes = []

    center_x, center_y = 600, 350
    total = max(len(nodes), 1)
    radius = 260 if total <= 8 else 380
    angle_step = (2 * math.pi) / total

    for i, node in enumerate(nodes):
        angle = i * angle_step
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

        ntype = node.get("type", "unknown").lower()

        layout_nodes.append({
            "id": node["id"],
            "label": node["label"],
            "type": ntype,
            "x": round(x, 2),
            "y": round(y, 2),
            "color": _node_color(ntype),
            "size": _node_size(ntype),
            "zoom_level": _zoom(ntype)
        })

    return {
        "nodes": layout_nodes,
        "edges": edges,
        "summary": f"Layout generated for {len(nodes)} nodes and {len(edges)} edges."
    }


def _node_color(t):
    return {
        "class": "#3299FF",
        "function": "#55DD33",
        "import": "#AA44DD"
    }.get(t, "#999999")


def _node_size(t):
    return {
        "class": 70,
        "function": 45,
        "import": 35
    }.get(t, 30)


def _zoom(t):
    if t == "class":
        return "high"
    if t == "function":
        return "medium"
    return "low"
