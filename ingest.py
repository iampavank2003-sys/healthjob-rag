"""Step 1: load job postings and store them in a vector database (Chroma)."""
import json
import chromadb

client = chromadb.PersistentClient(path="chroma_db")
# Chroma's default embedding model (all-MiniLM-L6-v2) turns text into vectors
collection = client.get_or_create_collection("jobs", metadata={"hnsw:space": "cosine"})

jobs = json.load(open("data/jobs.json"))
collection.upsert(
    ids=[j["id"] for j in jobs],
    documents=[f'{j["title"]}. {j["description"]}' for j in jobs],
    metadatas=[{"title": j["title"], "city": j["city"], "category": j["category"]} for j in jobs],
)
print(f"Stored {collection.count()} job postings.")
