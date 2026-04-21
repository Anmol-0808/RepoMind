from typing import List, Dict
from retrieval.embeddings import get_embedding
import numpy as np


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def rerank_chunks(query: str, chunks: List[Dict], top_k: int = 5) -> List[Dict]:
    """
    Re-rank retrieved chunks based on similarity with query
    """

    query_embedding = get_embedding(query)

    scored = []

    for chunk in chunks:
        chunk_embedding = chunk.get("embedding")

        
        if chunk_embedding is None:
            chunk_embedding = get_embedding(chunk["content"])

        score = cosine_similarity(query_embedding, chunk_embedding)


        file_name = chunk["metadata"].get("file_name", "").lower()
        if "test" not in file_name:
            score += 0.05

        scored.append((score, chunk))

    
    scored.sort(key=lambda x: x[0], reverse=True)

    return [chunk for score, chunk in scored[:top_k]]