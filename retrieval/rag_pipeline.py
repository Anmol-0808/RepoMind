from langchain_openai import ChatOpenAI
from retrieval.retriever import query_vector_db
import os
from dotenv import load_dotenv
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
        metadata = chunk["metadata"]

        context += f"""
--- Chunk {i+1} ---
File: {metadata.get("file_name")}
Path: {metadata.get("file_path")}
Type: {metadata.get("type")}
Name: {metadata.get("name")}

Code:
{chunk["content"]}
"""

    return context


def ask_repo(query: str):

   
    retrieved_chunks = query_vector_db(query, top_k=5)

    
    context = format_context(retrieved_chunks)

   
    prompt = f"""
You are a senior software engineer analyzing a codebase.

Your job is to:
- Explain clearly
- Reference functions/files when possible
- Be concise but informative

STRICT RULES:
- Use ONLY the provided context
- Do NOT hallucinate
- If unsure, say: "I could not find this in the codebase."

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