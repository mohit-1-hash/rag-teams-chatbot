# Microsoft Teams Troubleshooting Assistant

## Overview

A Retrieval-Augmented Generation (RAG) based troubleshooting assistant for Microsoft Teams. The application retrieves relevant information from documents using semantic search and generates context-aware responses using Google's Gemini model.

The project supports document ingestion, embedding generation, vector search, and an interactive Streamlit interface for answering troubleshooting queries.

---

## Features

- PDF document ingestion
- URL content ingestion
- Automatic text extraction
- Text chunking
- Embedding generation using Sentence Transformers
- Semantic search using FAISS
- PostgreSQL metadata storage
- Google Gemini integration for answer generation
- Streamlit-based user interface

---

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- FAISS
- Sentence Transformers
- PostgreSQL
- BeautifulSoup
- PDFPlumber
- Requests
- NumPy

---

## Project Structure

```
.
├── app.py
├── pipeline.py
├── db/
├── ingestion/
├── llm/
├── pages/
└── ...
```

---

## Installation

Clone the repository

```bash
git clone <repo-url>
cd <repo-name>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```text
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
GEMINI_API_KEY=
```

Run the application

```bash
streamlit run app.py
```

---

## Future Improvements

- Hybrid retrieval
- Better chunking strategies
- Reranking retrieved documents
- Conversation memory
- Support for additional document formats

## Additional Documentation

Further implementation notes and engineering decisions are available in `doc\ENGINEERING_DECISIONS.md`.