from typing import List, Dict
import os

USE_OPENAI = False  


from sentence_transformers import SentenceTransformer
_local_model = None


def get_local_model():
    global _local_model
    if _local_model is None:
        _local_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _local_model


def get_openai_client():
    from openai import OpenAI
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def format_chunk_text(chunk: Dict) -> str:
    return f"""
File: {chunk.get("file_name", "")}
Path: {chunk.get("file_path", "")}
Type: {chunk.get("type", "")}
Name: {chunk.get("name", "")}

Code:
{chunk.get("content", "")}
"""


def get_embedding(text: str) -> List[float]:

    if USE_OPENAI:
        client = get_openai_client()
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding

    else:
        model = get_local_model()
        return model.encode(text).tolist()


def embed_chunks(chunks: List[Dict]) -> List[Dict]:

    texts = [format_chunk_text(chunk) for chunk in chunks]

    if USE_OPENAI:
        client = get_openai_client()
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        embeddings = [item.embedding for item in response.data]

    else:
        model = get_local_model()
        embeddings = model.encode(texts)

    enriched_chunks = []

    for chunk, emb in zip(chunks, embeddings):
        new_chunk = chunk.copy()
        new_chunk["embedding"] = [float(x) for x in emb]
        enriched_chunks.append(new_chunk)

    return enriched_chunks