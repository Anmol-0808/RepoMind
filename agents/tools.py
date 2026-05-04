from langchain.tools import tool
from retrieval.rag_pipeline import ask_repo


ACTIVE_REPO = ""


def set_active_repo(repo_name: str):
    global ACTIVE_REPO
    ACTIVE_REPO = repo_name


def get_active_repo():
    return ACTIVE_REPO


@tool
def repo_qa_tool(query: str) -> str:
    """
    Answer questions about the repository
    """
    if not ACTIVE_REPO:
        return "No repository has been analyzed yet. Please analyze a repository first."

    return ask_repo(query, ACTIVE_REPO)


@tool
def repo_improvement_tool(query: str) -> str:
    """
    Analyze repository and suggest improvements
    """
    if not ACTIVE_REPO:
        return "No repository has been analyzed yet. Please analyze a repository first."

    prompt = f"""
You are a senior software engineer reviewing a codebase.

Your job:
- Identify issues
- Suggest improvements
- Mention scalability, structure, best practices

Question:
{query}

Use the repository knowledge to answer.
"""

    return ask_repo(prompt, ACTIVE_REPO)


@tool
def repo_code_fix_tool(query: str) -> str:
    """
    Suggest code improvements without directly modifying code
    """
    if not ACTIVE_REPO:
        return "No repository has been analyzed yet. Please analyze a repository first."

    prompt = f"""
You are a senior software engineer.

Your task:
- Review the existing codebase
- Suggest better code practices
- Recommend improvements
- Do NOT directly write production code
- Explain what should be changed and why

Question:
{query}
"""

    return ask_repo(prompt, ACTIVE_REPO)