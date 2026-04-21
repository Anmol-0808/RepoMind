from langchain.tools import tool
from retrieval.rag_pipeline import ask_repo


@tool
def repo_qa_tool(query: str) -> str:
    """Answer questions about the repository"""
    return ask_repo(query)


@tool
def repo_improvement_tool(query: str) -> str:
    """Analyze repository and suggest improvements"""
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
    return ask_repo(prompt)


@tool
def repo_code_fix_tool(query: str) -> str:
    """Suggest code improvements without modifying files"""

    prompt = f"""
You are a senior software engineer reviewing a codebase.

Your job:
- Suggest improvements to existing code
- Provide better versions of functions if needed
- Explain WHY the change is better

IMPORTANT:
- DO NOT assume code is missing unless necessary
- DO NOT say you are modifying files
- ONLY suggest changes for the developer to apply manually

FORMAT:

📌 Issue:
(what is wrong)

💡 Suggestion:
(what to improve)

💻 Suggested Code:
(optional improved snippet)

🧠 Reason:
(why this is better)

---

Question:
{query}
"""

    return ask_repo(prompt)