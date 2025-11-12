def build_architecture_map(parsed_data: dict):
    """
    Builds a lightweight architecture graph from parsed data.
    (Dummy but structured enough for frontend visualization.)
    """
    nodes, edges = [], []

    # Add class nodes
    for cls in parsed_data.get("classes", []):
        nodes.append({"id": cls, "type": "class"})

    # Add function nodes
    for fn in parsed_data.get("functions", []):
        nodes.append({"id": fn, "type": "function"})

    # Add import nodes
    for imp in parsed_data.get("imports", []):
        nodes.append({"id": imp, "type": "import"})

    # Create simple edges (class -> function)
    for cls in parsed_data.get("classes", []):
        for fn in parsed_data.get("functions", []):
            edges.append({"from": cls, "to": fn, "type": "contains"})

    summary = f"{len(nodes)} nodes, {len(edges)} relationships ({len(parsed_data.get('classes', []))} classes, {len(parsed_data.get('functions', []))} functions, {len(parsed_data.get('imports', []))} imports)"

    return {"nodes": nodes, "edges": edges, "summary": summary}
