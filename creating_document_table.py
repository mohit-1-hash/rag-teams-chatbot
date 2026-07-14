from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)
curr=conn.cursor()
curr.execute("DROP TABLE IF EXISTS documents") #restarting the serial numbers
def add_entry(curr,conn,service,title,source_type,source_path,document_url):
    curr.execute("""INSERT INTO documents(service,title,source_type,source_path,document_url)
                 VALUES(%s,%s,%s,%s,%s) RETURNING document_id""",(service,title,source_type,source_path,document_url))
    conn.commit()
curr.execute("""CREATE TABLE IF NOT EXISTS  documents (
    document_id SERIAL PRIMARY KEY,
    service TEXT NOT NULL,              -- Teams, Outlook, etc.
    title TEXT NOT NULL,                -- Display name for admin
    source_type TEXT NOT NULL,          -- pdf / url / docx
    source_path TEXT NOT NULL,          -- file path or URL
    document_url TEXT  ,         -- original url from web
    status TEXT DEFAULT 'active',       -- active / inactive
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""")
conn.commit()

'''service="Teams"
title="Teams_troubleshooting"
source_type="url"
#source_path="C:\\Users\\tavit\\Mohit\\Mohit\\All_language_codes\\pythoncodes\\complete_chatbot\\phase_2_completed\\troubleshoot-microsoftteams.pdf"
document_url="https://learn.microsoft.com/en-us/troubleshoot/microsoftteams/teams-welcome"
source_path=document_url
add_entry(curr,conn,service,title,source_type,source_path,document_url)
'''
conn.commit()