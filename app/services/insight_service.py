"""
insight_service.py
------------------
Analyzes the parsed & architecture data to generate
AI-style insights, complexity hints, and summary text.
"""

from typing import Dict

def generate_insights(parsed_data: Dict, architecture_data: Dict) -> Dict:
    """
    Generates insights from parsed and architecture info.
    """
    num_classes = len(parsed_data.get("classes", []))
    num_funcs = len(parsed_data.get("functions", []))
    num_imports = len(parsed_data.get("imports", []))
    total_nodes = len(architecture_data.get("nodes", []))
    total_edges = len(architecture_data.get("edges", []))

    summary_lines = []
    summary_lines.append(f"The code defines {num_classes} classes, {num_funcs} functions, and {num_imports} imports.")
    if total_nodes:
        summary_lines.append(f"The architecture graph has {total_nodes} nodes and {total_edges} relationships.")

    # Simple rule-based hints (will later connect to LLM)
    hints = []
    if num_classes == 0 and num_funcs > 0:
        hints.append("No classes found — consider using classes to organize related functions.")
    if num_funcs > 15:
        hints.append("High number of functions — possible need for modularization.")
    if num_imports > 10:
        hints.append("Many imports — verify if all dependencies are required.")
    if total_edges == 0:
        hints.append("No interconnections detected; the system appears isolated.")

    if not hints:
        hints.append("Code structure looks balanced and clean.")

    return {
        "summary": " ".join(summary_lines),
        "hints": hints,
        "metrics": {
            "classes": num_classes,
            "functions": num_funcs,
            "imports": num_imports,
            "nodes": total_nodes,
            "edges": total_edges
        }
    }
