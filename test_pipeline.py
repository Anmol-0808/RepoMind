from ingestion.repo_loader import clone_repo, load_repository_files
from ingestion.code_chunker import chunk_repository, create_repo_structure_chunk
from retrieval.embeddings import embed_chunks
from retrieval.vector_store import (
    add_chunks_to_vector_db,
    get_chroma_client,
    collection_exists
)
from retrieval.retriever import query_vector_db
from retrieval.reranker import rerank_chunks
from retrieval.rag_pipeline import ask_repo


repo_path = clone_repo("https://github.com/Anmol-0808/Mail-Mind")
repo_name = repo_path.split("\\")[-1]

files = load_repository_files(repo_path)
print("Loaded files:", len(files))

chunks = chunk_repository(files)

structure_chunk = create_repo_structure_chunk(files)
chunks.append(structure_chunk)

for chunk in chunks:
    chunk["repo_name"] = repo_name

print("Chunks created:", len(chunks))

embedded_chunks = embed_chunks(chunks)
print("Embeddings created:", len(embedded_chunks))

print("Sample keys:", embedded_chunks[0].keys())

client = get_chroma_client()

if not collection_exists(client, repo_name):
    print("\n📦 Storing embeddings for the first time...")
    add_chunks_to_vector_db(embedded_chunks)
else:
    print(f"\n⚠️ Collection for '{repo_name}' already exists, skipping storage.")

query = "authentication logic"

print("\n🔎 WITHOUT RERANKING:\n")
results = query_vector_db(query, repo_name, top_k=5)

for i, res in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print("Score:", res["score"])
    print("File:", res["metadata"]["file_name"])

print("\n🔥 WITH RERANKING:\n")

results = query_vector_db(query, repo_name, top_k=10)
reranked = rerank_chunks(query, results, top_k=5)

for i, res in enumerate(reranked):
    print(f"\n--- Result {i+1} ---")
    print("File:", res["metadata"]["file_name"])

answer = ask_repo("How authentication works?")

print("\n🧠 AI Answer:\n")
print(answer)

results = query_vector_db("authentication", repo_name, top_k=5)

print("\nDEBUG RESULTS:\n")
for r in results:
    print(r["metadata"]["file_name"])
    print(r["content"][:100])