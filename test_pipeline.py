from ingestion.repo_loader import clone_repo, load_repository_files
from ingestion.code_chunker import chunk_repository
from retrieval.embeddings import embed_chunks

repo_path = clone_repo("https://github.com/psf/requests")

files = load_repository_files(repo_path)
print("Loaded files:", len(files))

chunks = chunk_repository(files)
print("Chunks created:", len(chunks))

embedded_chunks = embed_chunks(chunks)
print("Embeddings created:", len(embedded_chunks))

print("Sample keys:", embedded_chunks[0].keys())

from retrieval.vector_store import add_chunks_to_vector_db

from retrieval.vector_store import get_chroma_client, collection_exists

client = get_chroma_client()

if not collection_exists(client):
    print("Storing embeddings for the first time...")
    add_chunks_to_vector_db(embedded_chunks)
else:
    print("Collection already exists, skipping storage.")
from retrieval.retriever import query_vector_db

results = query_vector_db("authentication logic", top_k=5)

def collection_exists(client, name="repo_chunks"):
    try:
        client.get_collection(name)
        return True
    except:
        return False
    
for i, res in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print("Score:", res["score"])
    print("File:", res["metadata"]["file_name"])
    print("Content Preview:\n", res["content"][:300])

from retrieval.rag_pipeline import ask_repo

answer = ask_repo("How authentication works?")
print("\n🧠 AI Answer:\n")
print(answer)