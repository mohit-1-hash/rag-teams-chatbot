import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
def build_faiss_index(chunks,ids,rebuild=False):
    # build_faiss_index.py  
    # loading clean chunks from chunks_cleaned.json
    texts = [c["text"] for c in chunks]
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
    print(type(embeddings))
    # building faiss index
    dim = embeddings.shape[1]
    print(dim)
    if(rebuild==True or not os.path.exists("faiss.index")):
        base_index = faiss.IndexFlatIP(dim) # using cosine similarity
        index=faiss.IndexIDMap(base_index)
    else:
         index=faiss.read_index("faiss.index")
    id_np=np.array(ids).astype('int64')
    print(id_np.shape)
    index.add_with_ids(embeddings,id_np)

    print("FAISS index size:", index.ntotal)

    # saving index and metadata into faiss.index
    faiss.write_index(index, "faiss.index")

    return  
def embed_text(text: str):
    # Replace with real embedder
        embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        query_vec = embed_model.encode(
        [text],
        convert_to_numpy=True,
        normalize_embeddings=True
        )
        return query_vec    