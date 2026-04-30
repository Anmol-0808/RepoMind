from langchain.tools import tool
from retrieval.rag_pipeline import ask_repo


CURRENT_REPO = "Mail-Mind"


@tool
def repo_qa_tool(query: str) -> str:
    """
    Answer questions about the repository
    """
    return ask_repo(query, CURRENT_REPO)


@tool
def repo_improvement_tool(query: str) -> str:
    """
    Analyze repository and suggest improvements
    """
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

    return ask_repo(prompt, CURRENT_REPO)


@tool
def repo_code_fix_tool(query: str) -> str:
    """
    Suggest code improvements without directly modifying code
    """
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

    return ask_repo(prompt, CURRENT_REPO)