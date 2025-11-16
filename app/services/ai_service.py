import os
from typing import Dict, Any
from openai import AzureOpenAI

# Initialize Azure client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")


def generate_ai_insights(parsed: Dict[str, Any], arch: Dict[str, Any], use_llm: bool):
    """
    Day-6: Generate STATIC + OPTIONAL LLM-based analysis.
    """

    classes = parsed.get("classes", [])
    functions = parsed.get("functions", [])
    imports = parsed.get("imports", [])

    # Static analysis
    static = {
        "class_count": len(classes),
        "function_count": len(functions),
        "import_count": len(imports),
        "complexity": _rate_complexity(classes, functions),
        "code_smells": _detect_smells(parsed),
    }

    llm_summary = None

    if use_llm:
        prompt = _build_prompt(parsed, arch)

        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are an expert software architect."},
                {"role": "user", "content": prompt}
            ]
        )

        # FIXED for new OpenAI SDK
        llm_summary = response.choices[0].message.content

    return {
        "static": static,
        "llm_summary": llm_summary
    }


# Helper functions
def _rate_complexity(classes, functions):
    total = len(classes) + len(functions)
    if total < 5:
        return "Low"
    elif total < 15:
        return "Medium"
    else:
        return "High"


def _detect_smells(parsed):
    smells = []
    if len(parsed.get("functions", [])) == 0:
        smells.append("No functions found.")
    if len(parsed.get("classes", [])) == 0:
        smells.append("No classes found.")
    if len(parsed.get("imports", [])) == 0:
        smells.append("No imports detected.")
    return smells


def _build_prompt(parsed, arch):
    return f"""
Provide an expert-level architectural analysis.

CLASSES: {parsed.get("classes")}
FUNCTIONS: {parsed.get("functions")}
IMPORTS: {parsed.get("imports")}

ARCHITECTURE NODES: {arch.get("nodes")}
ARCHITECTURE EDGES: {arch.get("edges")}

Return:
1. A clear high-level system summary
2. Architecture structure explanation
3. Possible code smells
4. Suggestions for refactoring
5. Modularization improvements
"""
