import ast
import re

def parse_code_from_text(code_text: str, language: str):
    """
    Main entry point for parsing Python or Java code text.
    Returns structured dictionary containing classes, functions, imports.
    """
    if not code_text.strip():
        return {"summary": "Empty source file", "classes": [], "functions": [], "imports": []}

    if language == "python":
        return parse_python_code(code_text)
    elif language == "java":
        return parse_java_code(code_text)
    else:
        raise ValueError("Unsupported language type")


# ========================
# PYTHON PARSER
# ========================
def parse_python_code(code_text: str):
    print("[DEBUG] Python parser started...")
    try:
        tree = ast.parse(code_text)
    except Exception as e:
        print(f"[ERROR] Python parse failed: {e}")
        return {"summary": f"Parse error: {e}", "classes": [], "functions": [], "imports": []}

    classes, functions, imports = [], [], []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    summary = f"{len(classes)} classes, {len(functions)} functions, {len(imports)} imports found."
    print(f"[DEBUG] Python parse summary: {summary}")

    return {
        "summary": summary,
        "classes": classes,
        "functions": functions,
        "imports": imports
    }


# ========================
# JAVA PARSER
# ========================
def parse_java_code(code_text: str):
    print("[DEBUG] Java parser started...")

    # Basic patterns for structure extraction
    class_pattern = re.compile(r"\bclass\s+(\w+)")
    interface_pattern = re.compile(r"\binterface\s+(\w+)")
    function_pattern = re.compile(r"(?:public|private|protected)?\s+\w+\s+(\w+)\s*\(")
    import_pattern = re.compile(r"import\s+([\w\.]+);")

    classes = class_pattern.findall(code_text)
    interfaces = interface_pattern.findall(code_text)
    functions = function_pattern.findall(code_text)
    imports = import_pattern.findall(code_text)

    summary = f"{len(classes)} classes, {len(functions)} functions, {len(imports)} imports, {len(interfaces)} interfaces found."
    print(f"[DEBUG] Java parse summary: {summary}")

    return {
        "summary": summary,
        "classes": classes,
        "functions": functions,
        "imports": imports,
        "interfaces": interfaces
    }
