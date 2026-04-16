import chromadb
from typing import List, Dict
import uuid


def get_chroma_client(persist_dir: str = "chroma_db"):
    return chromadb.Client(
        chromadb.config.Settings(
            persist_directory=persist_dir
        )
    )


def get_or_create_collection(client, name: str = "repo_chunks"):
    return client.get_or_create_collection(name=name)



def collection_exists(client, name="repo_chunks"):
    try:
        client.get_collection(name)
        return True
    except:
        return False


def add_chunks_to_vector_db(chunks: List[Dict]):

    client = get_chroma_client()
    collection = get_or_create_collection(client)

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:
        ids.append(str(uuid.uuid4()))

        documents.append(chunk["content"])

        embeddings.append(chunk["embedding"])

        metadatas.append({
            "file_path": chunk.get("file_path"),
            "file_name": chunk.get("file_name"),
            "type": chunk.get("type"),
            "name": chunk.get("name", "")
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Stored {len(ids)} chunks in Chroma DB")