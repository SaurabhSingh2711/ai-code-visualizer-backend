# app/services/ai_service.py

import os
import json
from typing import Dict, Any
from openai import AzureOpenAI


# ---------------------------------------------------------
# Azure OpenAI Client Initialization
# ---------------------------------------------------------
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")


# ---------------------------------------------------------
# MAIN PUBLIC ENTRY FUNCTION
# ---------------------------------------------------------
def generate_full_ai_insights(
    parsed: Dict[str, Any],
    architecture: Dict[str, Any],
    use_llm: bool = False
) -> Dict[str, Any]:
    """
    Unified AI engine (Day-13):
    - Static analysis
    - Optional LLM summary using Azure OpenAI
    """

    static_section = _static_analysis(parsed, architecture)

    llm_section = None
    if use_llm:
        llm_section = _llm_insights(parsed, architecture)

    return {
        "static": static_section,
        "llm_summary": llm_section
    }


# ---------------------------------------------------------
# STATIC ANALYSIS SECTION
# ---------------------------------------------------------
def _static_analysis(parsed, architecture):
    """
    Lightweight, deterministic, fast analysis.
    """

    classes = parsed.get("classes", [])
    functions = parsed.get("functions", [])
    imports = parsed.get("imports", [])

    smells = []
    if not functions:
        smells.append("No functions found.")
    if not classes:
        smells.append("No classes found.")
    if not imports:
        smells.append("No imports detected.")

    complexity_score = len(classes) + len(functions)

    return {
        "class_count": len(classes),
        "function_count": len(functions),
        "import_count": len(imports),
        "complexity": _rate_complexity(complexity_score),
        "code_smells": smells,
        "architecture_node_count": len(architecture.get("nodes", [])),
        "architecture_edge_count": len(architecture.get("edges", [])),
    }


def _rate_complexity(score: int) -> str:
    if score < 5:
        return "Low"
    elif score < 15:
        return "Medium"
    else:
        return "High"


# ---------------------------------------------------------
# LLM SECTION — Azure GPT
# ---------------------------------------------------------
def _llm_insights(parsed, architecture):
    """
    Calls Azure OpenAI GPT model.
    """

    prompt = _build_prompt(parsed, architecture)

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are an expert software architect."},
                {"role": "user", "content": prompt}
            ]
        )

        # Azure SDK new format
        return response.choices[0].message.content

    except Exception as e:
        return f"[AZURE LLM ERROR] {str(e)}"


def _build_prompt(parsed, architecture):
    return f"""
Analyze the following parsed code and architecture:

PARSED:
{json.dumps(parsed, indent=2)}

ARCHITECTURE:
{json.dumps(architecture, indent=2)}

Provide:
1. High-level system summary
2. Architecture explanation
3. Code smells
4. Refactoring suggestions
5. Modularity improvements
"""


# ---------------------------------------------------------
# END OF FILE
# ---------------------------------------------------------
