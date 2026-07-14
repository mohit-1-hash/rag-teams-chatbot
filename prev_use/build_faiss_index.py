# build_faiss_index.py

import json
import faiss
from sentence_transformers import SentenceTransformer

# loading clean chunks from chunks_cleaned.json
with open("chunks_cleaned_with_doc.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

texts = [c["text"] for c in chunks]
metadata = [
    {
        "issue_title": c["issue_title"],
        "issue_id": c["issue_id"],
        "chunk_id": c["chunk_id"],
        "document_title":c["document_title"],
        "document_url":c["document_url"],
    }
    for c in chunks
]

print("Chunks loaded:", len(texts))

# creating embeddings using sentence transformer
model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

print("Embedding shape:", embeddings.shape)

# building faiss index
dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim) # using cosine similarity
index.add(embeddings)

print("FAISS index size:", index.ntotal)

# saving index and metadata into faiss.index
faiss.write_index(index, "faiss.index")

with open("faiss_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("FAISS index and metadata saved")