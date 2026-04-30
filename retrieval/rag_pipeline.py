from langchain_openai import ChatOpenAI
from retrieval.retriever import query_vector_db
from retrieval.reranker import rerank_chunks
from dotenv import load_dotenv
import os

load_dotenv()


def get_llm():
    return ChatOpenAI(
        model="gpt-5",
        temperature=0.1,
        api_key=os.getenv("OPENAI_API_KEY")
    )


def format_context(chunks):
    context = ""

    for i, chunk in enumerate(chunks):
        metadata = chunk.get("metadata", {})

        context += f"""
--- Chunk {i+1} ---
File: {metadata.get("file_name", "")}
Path: {metadata.get("file_path", "")}
Type: {metadata.get("type", "")}
Name: {metadata.get("name", "")}

Code:
{chunk.get("content", "")[:500]}
"""

    return context


def ask_repo(query: str, repo_name: str):

    retrieved_chunks = query_vector_db(
        query=query,
        repo_name=repo_name,
        top_k=25
    )

    retrieved_chunks = rerank_chunks(
        query,
        retrieved_chunks,
        top_k=10
    )

    context = format_context(retrieved_chunks)

    prompt = f"""
You are a senior software engineer analyzing a codebase.

Your job is to provide a clear, structured answer.

STRICT RULES:
- Use ONLY the provided context
- Do NOT hallucinate
- If information is missing, say: "I could not find this in the codebase."
- If the question is about the overall system, explain the flow across multiple components.

FORMAT YOUR ANSWER EXACTLY LIKE THIS:

📌 Summary:
(2-3 lines explaining the answer)

📂 Relevant Files:
(List important files and functions)

🧠 Explanation:
(Detailed explanation of how it works)

📎 Evidence:
(Reference code snippets or test files if available)

---

QUESTION:
{query}

---

CONTEXT:
{context}

---

ANSWER:
"""

    llm = get_llm()
    response = llm.invoke(prompt)

    return response.content