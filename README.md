# Microsoft Teams Troubleshooting Assistant (RAG)

## Overview

This project implements a Retrieval-Augmented Generation (RAG) based troubleshooting assistant for Microsoft Teams. It retrieves relevant information from documentation using semantic search and generates context-aware responses using Google's Gemini model.

## Features

- PDF and URL document ingestion
- Automatic text extraction
- Text chunking
- Embedding generation
- FAISS vector search
- PostgreSQL metadata storage
- Prompt engineering
- Gemini-powered answer generation
- Streamlit web interface

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- FAISS
- PostgreSQL
- LangChain
- Sentence Transformers

## Project Structure

```
app.py
db/
ingestion/
llm/
pages/
pipeline.py
```

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file with

```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
GEMINI_API_KEY=
```

Run

```bash
streamlit run app.py
```

## Future Improvements

- Hybrid retrieval
- Better reranking
- Improved chunking strategy
- Conversation memory
