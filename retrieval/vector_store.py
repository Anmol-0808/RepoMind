import chromadb
from typing import List, Dict
import uuid


def get_chroma_client(persist_dir: str = "chroma_db"):
    return chromadb.PersistentClient(path=persist_dir)


def get_or_create_collection(client, repo_name: str):
    return client.get_or_create_collection(name=repo_name)


def collection_exists(client, repo_name: str):
    try:
        client.get_collection(repo_name)
        return True
    except:
        return False


def add_chunks_to_vector_db(chunks: List[Dict]):

    if not chunks:
        return

    client = get_chroma_client()

    repo_name = chunks[0].get("repo_name", "default_repo")
    collection = get_or_create_collection(client, repo_name)

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:
        ids.append(str(uuid.uuid4()))

        documents.append(
            f"""
File: {chunk.get('file_name')}
Path: {chunk.get('file_path')}
Type: {chunk.get('type')}
Name: {chunk.get('name', '')}

Code:
{chunk.get('content')}
"""
        )

        embeddings.append(chunk["embedding"])

        metadatas.append({
            "file_path": chunk.get("file_path"),
            "file_name": chunk.get("file_name"),
            "type": chunk.get("type"),
            "name": chunk.get("name", ""),
            "repo_name": chunk.get("repo_name", "default_repo")
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    