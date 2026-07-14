from db.db import get_active_documents
from ingestion.extract_text import extract_text
from ingestion.issues import extract_issues
from ingestion.chunk import chunk_issues
from ingestion.embed import build_faiss_index,embed_text
from db.db import insert_chunk,clear_chunks,get_next_faiss_id_from_db
import faiss
from psycopg2.extras import RealDictCursor
from db.db import get_connection
from ingestion.title import derive_title
from creating_document_table import add_entry

def rebuild_index():
    documents = get_active_documents()
    print(documents)
    all_chunks = []
    for doc in documents:
        pages = extract_text(doc)
        issues = extract_issues(pages,doc["document_id"])
        chunks = chunk_issues(issues)
        all_chunks.extend(chunks)
    print(len(all_chunks))
    clear_chunks()
    ids=[]
    for faiss_id, chunk in enumerate(all_chunks):
        ids.append(faiss_id)
        insert_chunk(faiss_id=faiss_id,chunk=chunk)
    build_faiss_index(all_chunks,ids,rebuild=True)

def run_pipeline(source_value,source_path,service):
    chunks=[]
    doc=dict()
    conn=get_connection()
    curr=conn.cursor()
    print("REACHED HERE")
    if(source_value=='url'):
        doc["document_url"]=source_path
    else:
        doc["document_url"]=None
    doc["source_type"]=source_value
    doc["source_path"]=source_path
    print("REACHED TEXT EXTRACTION")
    pages=extract_text(doc)
    #print(pages)
    title=derive_title(source_type=source_value,source_path=source_path)
    print("DERIVED TITLE")
    doc["title"]=title
    add_entry(curr,conn,service,title,source_value,source_path,doc["document_url"])
    print("ADDED ENTRY")
    document_id=curr.fetchone()[0]
    doc["document_id"]=document_id
    issues=extract_issues(pages,doc["document_id"])
    print("EXTRACTED ISSUES")
    chunks=chunk_issues(issues)
    print("CHUNKED ISSUES")
    ids=[]
    next_id=get_next_faiss_id_from_db()
    for chunk in chunks:
        ids.append(next_id)
        insert_chunk(faiss_id=next_id,chunk=chunk)
        next_id+=1
    print(chunks[0])
    print("INSERTED CHUNKS")
    if(ids[0]==0):
        build_faiss_index(chunks,ids,rebuild=True)
    else:
        build_faiss_index(chunks,ids,rebuild=False)
    print("BUILT INDEX")
    return

FAISS_INDEX_PATH = "faiss.index"
TOP_K = 5

# load once

def search(query: str):
    # embed query
    index = faiss.read_index(FAISS_INDEX_PATH)

    qvec = embed_text(query).astype("float32")

    # faiss search
    distances, ids = index.search(qvec, TOP_K)
    faiss_ids = [int(i) for i in ids[0] if i != -1]

    if not faiss_ids:
        return []

    # fetch chunks + metadata
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute(
        """
        SELECT 
            c.text,
            c.issue_title,
            d.title AS document_title,
            d.document_url
        FROM chunks c
        JOIN documents d ON c.document_id = d.document_id
        WHERE c.faiss_id = ANY(%s)
        """,
        (faiss_ids,)
    )

    results = cur.fetchall()
    cur.close()
    conn.close()
    print(results)
    return results
print(get_active_documents())
#clear_chunks()
print(get_active_documents())