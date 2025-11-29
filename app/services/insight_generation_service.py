# app/services/insight_generation_service.py

import json
from app.services.llm_service import LLMService

llm = LLMService()


def generate_ai_insights(parsed_files, cross_relations, subsystems, layers, service_calls):
    """
    Day-13:
    Generate AI-enhanced architecture analysis using LLM.
    """

    prompt = f"""
You are a senior enterprise architect.

Analyze the following software project metadata and produce:

1. High-level architecture summary (8–10 lines)
2. Explanation of detected subsystems
3. Explanation of layered architecture mapping
4. Dependency insights across modules
5. Service-to-service call flow explanation
6. Risks & bottlenecks
7. Recommended improvements & modernization suggestions
8. 10-line system documentation summary

=== PROJECT DATA START ===

Parsed Files:
{json.dumps(parsed_files, indent=2)}

Cross File Relations:
{json.dumps(cross_relations, indent=2)}

Subsystems:
{json.dumps(subsystems, indent=2)}

Layers:
{json.dumps(layers, indent=2)}

Service Calls:
{json.dumps(service_calls, indent=2)}

=== PROJECT DATA END ===
"""

    try:
        result = llm.ask(prompt)
    except Exception as e:
        return {"ai_insights": f"LLM Error: {str(e)}"}

    return {"ai_insights": result}
