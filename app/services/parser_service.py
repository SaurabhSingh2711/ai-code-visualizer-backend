# app/services/parser_service.py
"""
Simple parser service for Day-2.
Supports basic extraction for Python (ast) and Java (javalang).
Returns structured JSON:
{
  "classes": [...],
  "functions": [...],
  "imports": [...],
  "summary": "..."
}
"""

import ast
import re

try:
    import javalang
    JAVALANG_AVAILABLE = True
except Exception:
    JAVALANG_AVAILABLE = False


def parse_code_from_text(code_text: str, language: str):
    language = language.lower()
    if language == "python":
        return _parse_python(code_text)
    elif language == "java":
        if not JAVALANG_AVAILABLE:
            return {"error": "javalang not installed on server"}
        return _parse_java(code_text)
    else:
        return {"error": "unsupported language"}


# ---------- Python parser ----------
def _parse_python(code_text: str):
    classes = []
    functions = []
    imports = []

    # parse AST
    try:
        tree = ast.parse(code_text)
    except SyntaxError as e:
        return {"error": "Python syntax error", "details": str(e)}

    for node in ast.walk(tree):
        # class definitions
        if isinstance(node, ast.ClassDef):
            classes.append(node.name)
            # optionally capture methods within class
            # methods are FunctionDef nodes inside ClassDef.body
            # (we don't expand here to keep Day-2 simple)
        # standalone functions
        elif isinstance(node, ast.FunctionDef):
            # top-level functions: ensure parent is Module
            # For simplicity, we include all functions (will filter later if needed)
            functions.append(node.name)
        # imports
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


# ---------- Java parser ----------
def _parse_java(code_text: str):
    if not JAVALANG_AVAILABLE:
        return {"error": "javalang not available"}
    classes = []
    functions = []
    imports = []

    try:
        tree = javalang.parse.parse(code_text)
    except Exception as e:
        # fallback: regex-based extraction if parse fails
        return _parse_java_with_regex(code_text)

    # imports
    for imp in getattr(tree, "imports", []):
        imports.append(imp.path)

    # types => class declarations (tree.types)
    for type_decl in getattr(tree, "types", []):
        try:
            name = getattr(type_decl, "name", None)
            if name:
                classes.append(name)
                # methods: type_decl.methods
                for method in getattr(type_decl, "methods", []):
                    functions.append(method.name)
        except Exception:
            pass

    return {
        "classes": classes,
        "functions": functions,
        "imports": imports,
        "summary": f"{len(classes)} classes, {len(functions)} methods, {len(imports)} imports found."
    }


def _parse_java_with_regex(code_text: str):
    # simple backup when javalang fails: use regex
    classes = re.findall(r'\bclass\s+([A-Za-z_][A-Za-z0-9_]*)', code_text)
    methods = re.findall(r'(?:public|private|protected)\s+[A-Za-z0-9_<>\[\]]+\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(', code_text)
    imports = re.findall(r'import\s+([\w\.]+);', code_text)
    return {
        "classes": classes,
        "functions": methods,
        "imports": imports,
        "summary": f"{len(classes)} classes, {len(methods)} methods, {len(imports)} imports found (regex fallback)."
    }
