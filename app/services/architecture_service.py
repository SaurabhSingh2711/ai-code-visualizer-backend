def build_architecture_map(parsed):
    nodes = []
    edges = []

    # Add classes
    for cls in parsed.get("classes", []):
        nodes.append({
            "id": f"class:{cls}",
            "type": "class",
            "label": cls          # <-- ADDED
        })

    # Add functions
    for func in parsed.get("functions", []):
        nodes.append({
            "id": f"func:{func}",
            "type": "function",
            "label": func         # <-- ADDED
        })

    # Add imports
    for imp in parsed.get("imports", []):
        nodes.append({
            "id": f"import:{imp}",
            "type": "import",
            "label": imp          # <-- ADDED
        })

    # Edges (unchanged)
    for cls in parsed.get("classes", []):
        for func in parsed.get("functions", []):
            if func.lower().startswith(cls.lower()):
                edges.append({
                    "from": f"class:{cls}",
                    "to": f"func:{func}",
                    "relation": "contains"
                })

    for imp in parsed.get("imports", []):
        for cls in parsed.get("classes", []):
            edges.append({
                "from": f"import:{imp}",
                "to": f"class:{cls}",
                "relation": "uses"
            })

    return {
        "nodes": nodes,
        "edges": edges,
        "summary":
            f"{len(nodes)} nodes, {len(edges)} relationships "
            f"({len(parsed.get('classes', []))} classes, "
            f"{len(parsed.get('functions', []))} functions, "
            f"{len(parsed.get('imports', []))} imports)"
    }
