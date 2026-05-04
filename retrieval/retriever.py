from typing import List, Dict
from retrieval.embeddings import get_embedding
import chromadb


def get_chroma_client(persist_dir: str = "chroma_db"):
    return chromadb.PersistentClient(path=persist_dir)


def get_collection(client, repo_name: str):
    return client.get_or_create_collection(name=repo_name)


def query_vector_db(query: str, repo_name: str, top_k: int = 5) -> List[Dict]:

    client = get_chroma_client()
    collection = get_collection(client, repo_name)

    auth_keywords = [
    "auth", "authentication", "login",
    "signup", "token", "jwt", "user", "session"
]

    if any(word in query.lower() for word in auth_keywords):
        expanded_query = f"{query} authentication login user token session auth"
    else:
        expanded_query = query
    query_embedding = get_embedding(expanded_query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances", "embeddings"]
    )

    retrieved_chunks = []

    if not results["documents"] or not results["documents"][0]:
        return retrieved_chunks

    for i in range(len(results["documents"][0])):
        retrieved_chunks.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "score": results["distances"][0][i],
            "embedding": results["embeddings"][0][i]
        })

    return retrieved_chunks