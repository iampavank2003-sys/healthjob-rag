"""Step 2: retrieve the jobs most similar to a candidate profile."""
import sys
import chromadb

collection = chromadb.PersistentClient(path="chroma_db").get_collection("jobs")

def retrieve(profile: str, k: int = 3):
    res = collection.query(query_texts=[profile], n_results=k)
    return [
        {"title": m["title"], "city": m["city"], "text": d, "distance": dist}
        for m, d, dist in zip(res["metadatas"][0], res["documents"][0], res["distances"][0])
    ]

if __name__ == "__main__":
    profile = " ".join(sys.argv[1:]) or "nurse with 3 years ICU experience"
    for r in retrieve(profile):
        print(f'{r["title"]} ({r["city"]})  distance={r["distance"]:.3f}')
