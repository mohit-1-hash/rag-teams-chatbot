import faiss
import numpy as np
from psycopg2.extras import RealDictCursor
from db.db import get_connection
from sentence_transformers import SentenceTransformer
# ---- CONFIG ----
FAISS_PATH = "faiss.index"
TOP_K = 5

# ---- LOAD INDEX ----
index = faiss.read_index(FAISS_PATH)

# ---- EMBEDDING FUNCTION ----
def embed(text: str) -> np.ndarray:
    # Replace with real embedder
        embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        query_vec = embed_model.encode(
        [text],
        convert_to_numpy=True,
        normalize_embeddings=True
        )
        return query_vec    

# ---- DB CONNECTION ----
conn = get_connection()
cur = conn.cursor(cursor_factory=RealDictCursor)

# ---- QUERY ----
query = "Teams audio not working"
query_vec = embed(query).astype("float32")

# ---- FAISS SEARCH ----
distances, faiss_ids = index.search(query_vec, TOP_K)
faiss_ids = list(map(int, faiss_ids[0]))

print("FAISS IDs:", faiss_ids)

# ---- DB FETCH ----
cur.execute(
    """
    SELECT c.text, d.title, d.document_url
    FROM chunks c
    JOIN documents d ON c.document_id = d.document_id
    WHERE c.faiss_id = ANY(%s)
    """,
    (faiss_ids,)
)

rows = cur.fetchall()

# ---- DISPLAY ----
for r in rows:
    print("\n---")
    print(r["text"][:300])
    print("SOURCE:", r["title"])
    print("URL:", r["document_url"])

cur.close()
conn.close()
