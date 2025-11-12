"""
Parser Service — Day 2 Version
--------------------------------
Parses uploaded code files (Python / Java) and extracts:
- Classes
- Functions / Methods
- Imports

Returns structured JSON like:
{
  "classes": [...],
  "functions": [...],
  "imports": [...],
  "summary": "1 class, 2 functions, 3 imports found."
}
"""

import ast
import re


def parse_code_from_text(code_text: str, language: str):
    """
    Entry point for parser service.
    Supports 'python' and 'java' languages.
    """
    language = language.lower()

    if language == "python":
        return _parse_python(code_text)
    elif language == "java":
        return _parse_java(code_text)
    else:
        return {"error": f"Unsupported language: {language}"}


# ---------- PYTHON PARSER ----------
def _parse_python(code_text: str):
    classes = []
    functions = []
    imports = []

    try:
        tree = ast.parse(code_text)
    except SyntaxError as e:
        return {"error": "Python syntax error", "details": str(e)}
    
    print("first Code received:", code_text[:200])

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
            print("second Code received:", code_text[:200])
        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)
            print("third Code received:", code_text[:200])
        elif isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return {
        "classes": classes,
        "functions": functions,
        "imports": imports,
        "summary": f"{len(classes)} classes, {len(functions)} functions, {len(imports)} imports found."
    }


# ---------- JAVA PARSER ----------
def _parse_java(code_text: str):
    """
    Attempts to parse Java code using 'javalang' if available,
    otherwise falls back to regex-based parsing.
    """
    try:
        import javalang
    except ImportError:
        return _parse_java_with_regex(code_text)

    classes = []
    functions = []
    imports = []

    try:
        tree = javalang.parse.parse(code_text)
    except Exception:
        # fallback to regex parsing on any error
        return _parse_java_with_regex(code_text)

    # imports
    for imp in getattr(tree, "imports", []):
        imports.append(imp.path)

    # class/type declarations
    for type_decl in getattr(tree, "types", []):
        try:
            if getattr(type_decl, "name", None):
                classes.append(type_decl.name)
                # extract method names
                for method in getattr(type_decl, "methods", []):
                    functions.append(method.name)
        except Exception:
            pass

    return {
        "classes": classes,
        "functions": functions,
        "imports": imports,
        "summary": f"{len(classes)} classes, {len(functions)} functions, {len(imports)} imports found."
    }


# ---------- JAVA REGEX FALLBACK ----------
def _parse_java_with_regex(code_text: str):
    """
    Basic regex fallback parser for Java files when javalang is missing or fails.
    """
    class_pattern = r'\bclass\s+([A-Za-z_][A-Za-z0-9_]*)'
    method_pattern = r'(?:public|private|protected)?\s*(?:static\s+)?[A-Za-z0-9_<>\[\]]+\s+([A-Za-z_][A-Za-z0-9_]*)\s*\('
    import_pattern = r'import\s+([\w\.]+);'

    classes = re.findall(class_pattern, code_text)
    functions = re.findall(method_pattern, code_text)
    imports = re.findall(import_pattern, code_text)

    return {
        "classes": classes,
        "functions": functions,
        "imports": imports,
        "summary": f"{len(classes)} classes, {len(functions)} functions, {len(imports)} imports found (regex fallback)."
    }
