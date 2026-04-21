import ast
from typing import List, Dict
def extract_python_chunks(file_content: str) -> List[Dict]:

    chunks = []
    lines = file_content.split("\n")

    try:
        tree = ast.parse(file_content)
    except Exception:
        return chunks 

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):

            start = node.lineno - 1
            end = getattr(node, "end_lineno", None)

            if end is None:
                continue

            chunk_code = "\n".join(lines[start:end])

            chunks.append({
                "type": type(node).__name__,  
                "name": node.name,
                "start_line": start + 1,
                "end_line": end,
                "content": chunk_code
            })

    return chunks

def simple_chunk(file_content: str, chunk_size: int = 100) -> List[Dict]:
    """
    Split file into fixed-size chunks (fallback for non-python files)
    """

    lines = file_content.split("\n")
    chunks = []

    for i in range(0, len(lines), chunk_size):

        chunk = "\n".join(lines[i:i + chunk_size])

        chunks.append({
            "type": "text",
            "start_line": i + 1,
            "end_line": i + chunk_size,
            "content": chunk
        })

    return chunks

def chunk_file(file: Dict) -> List[Dict]:
    file_path = file.get("path", "")
    content = file.get("content", "")

    if not content.strip():
        return []

    if file_path.endswith(".py"):
        ast_chunks = extract_python_chunks(content)

        if ast_chunks:
            return ast_chunks

    return simple_chunk(content)

def chunk_repository(files: List[Dict]) -> List[Dict]:
 

    all_chunks = []

    for file in files:

        file_chunks = chunk_file(file)

        for chunk in file_chunks:
            chunk["file_path"] = file.get("path")
            chunk["file_name"] = file.get("file_name")

        all_chunks.extend(file_chunks)

    return all_chunks

def create_repo_structure_chunk(files):
    structure = "Project Structure:\n"

    for file in files:
        structure += f"{file['relative_path']}\n"

    return {
        "type": "structure",
        "name": "repo_structure",
        "file_name": "REPO_OVERVIEW",
        "file_path": "root",
        "content": structure
    }