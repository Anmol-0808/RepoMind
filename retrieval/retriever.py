from typing import List, Dict
from retrieval.embeddings import get_embedding
import chromadb


def get_chroma_client(persist_dir: str = "chroma_db"):
    return chromadb.PersistentClient(path=persist_dir)


def get_collection(client, name: str = "repo_chunks"):
    return client.get_or_create_collection(name=name)


def query_vector_db(query: str, top_k: int = 5) -> List[Dict]:

    client = get_chroma_client()
    collection = get_collection(client)

    expanded_query = f"{query} authentication login user token session auth"
    query_embedding = get_embedding(expanded_query)

   
    results = collection.query(
    query_embeddings=[query_embedding],
    n_results=top_k,
    include=["documents", "metadatas", "distances", "embeddings"]
)

  
    retrieved_chunks = []

    for i in range(len(results["documents"][0])):
        retrieved_chunks.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "score": results["distances"][0][i],
                "embedding": results["embeddings"][0][i]
            })

    return retrieved_chunks