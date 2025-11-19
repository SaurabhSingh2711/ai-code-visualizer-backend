# app/services/subsystem_service.py

import re
from typing import Dict, List


def detect_subsystems(parsed_results: Dict[str, Dict]) -> Dict[str, List[str]]:
    """
    Very simple heuristic-based subsystem detection based on file name patterns.
    """

    subsystems = {
        "controller": [],
        "service": [],
        "data": [],
        "util": [],
        "unknown": [],
    }

    for fname, parsed in parsed_results.items():
        name = fname.lower()

        if "controller" in name:
            subsystems["controller"].append(fname)
        elif "service" in name:
            subsystems["service"].append(fname)
        elif "repo" in name or "db" in name:
            subsystems["data"].append(fname)
        elif "util" in name or "helper" in name or "helpers" in name:
            subsystems["util"].append(fname)
        else:
            subsystems["unknown"].append(fname)

    return subsystems


def detect_layers(parsed_results: Dict[str, Dict]) -> Dict[str, List[str]]:
    """
    Classify files into logical layers: App, Service, Data, Utility, Unknown.
    """

    layers = {
        "app_layer": [],
        "service_layer": [],
        "data_layer": [],
        "utility_layer": [],
        "unknown_layer": [],
    }

    for fname, parsed in parsed_results.items():
        name = fname.lower()

        if "app" in name or "controller" in name or "main" in name:
            layers["app_layer"].append(fname)
        elif "service" in name:
            layers["service_layer"].append(fname)
        elif "repo" in name or "db" in name:
            layers["data_layer"].append(fname)
        elif "util" in name or "helper" in name or "helpers" in name:
            layers["utility_layer"].append(fname)
        else:
            layers["unknown_layer"].append(fname)

    return layers


def detect_service_calls(parsed_results: Dict[str, Dict]) -> List[Dict]:
    """
    Detect calls to classes ending with 'Service' across files.

    Example:
    - from app.py → UserService
    """

    results = []

    for fname, parsed in parsed_results.items():
        raw = parsed.get("raw_text", "")

        # Find expressions like XService()
        service_calls = re.findall(r"([A-Za-z_]+Service)\s*\(", raw)

        for svc in service_calls:
            target_file = find_service_definition(parsed_results, svc)

            if target_file:
                results.append({
                    "from": fname,
                    "to": target_file,
                    "relation": f"calls-service:{svc}"
                })

    return results


def find_service_definition(parsed_results: Dict[str, Dict], class_name: str) -> str:
    """
    Find which file defines a service class.
    """
    for fname, parsed in parsed_results.items():
        if class_name in parsed.get("classes", []):
            return fname
    return None
