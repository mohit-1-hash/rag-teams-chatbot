import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

def get_connection():
    load_dotenv()

    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),)
    return conn


def get_active_documents(status="active"):
    conn=get_connection()
    curr=conn.cursor(cursor_factory=RealDictCursor)
    curr.execute(f"""SELECT * FROM DOCUMENTS WHERE status=%s;""",(status,))
    active_docs=curr.fetchall()
    curr.close()
    conn.close()
    return active_docs

def insert_chunk(faiss_id,chunk):
    conn=get_connection()
    curr=conn.cursor()
    #print("i")
    curr.execute(
        """
        INSERT INTO chunks(
            faiss_id,text,issue_title,document_id
        )
        VALUES (%s, %s, %s, %s)
        """,
        (
            faiss_id,chunk["text"],chunk["issue_title"],chunk["document_id"]
        )
    )
    conn.commit()
    curr.close()
    conn.close()
def clear_chunks():
    conn = get_connection()
    curr = conn.cursor()
    curr.execute("DROP TABLE IF EXISTS CHUNKS;")
    conn.commit()
    curr.execute("""CREATE TABLE CHUNKS( 
                 chunk_id SERIAL , --serial numbers
                 faiss_id  BIGINT PRIMARY KEY , --indices primary
                 text text NOT NULL ,-- actual chunk info
                 issue_title text NOT NULL, -- issue title 
                 document_id BIGINT NOT NULL, -- id of document from which it is extracted
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- time of creation
                 );""")
    conn.commit()
    curr.close()
    conn.close()

def get_next_faiss_id_from_db():
    conn=get_connection()
    print("getting faiss id")
    curr=conn.cursor()
    curr.execute("""CREATE TABLE IF NOT EXISTS chunks( 
                 chunk_id SERIAL , --serial numbers
                 faiss_id  BIGINT PRIMARY KEY , --indices primary
                 text text NOT NULL ,-- actual chunk info
                 issue_title text NOT NULL, -- issue title 
                 document_id BIGINT NOT NULL, -- id of document from which it is extracted
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- time of creation
                 );""")
    #print("h")
    curr.execute("SELECT COALESCE(MAX(faiss_id),-1) FROM chunks;")
    #print("J")
    next_id=curr.fetchone()[0]+1
    conn.commit()
    conn.close()
    curr.close()
    return next_id
