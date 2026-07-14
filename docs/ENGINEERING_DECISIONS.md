# Engineering Decisions

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) based troubleshooting assistant for Microsoft Teams. Instead of relying solely on the language model's internal knowledge, the system retrieves relevant information from documentation using semantic search and uses the retrieved context to generate grounded responses.

The project was built to better understand the engineering aspects of modern LLM applications, including retrieval, vector search, prompt engineering, and system design.

---

# System Architecture

```
Documents (PDFs / URLs)
            │
            ▼
      Text Extraction
            │
            ▼
        Chunking
            │
            ▼
   Sentence Embeddings
            │
            ▼
      FAISS Vector Index
            │
            ▼
 Retrieve Top-K Chunks
            │
            ▼
 Prompt Construction
            │
            ▼
     Google Gemini
            │
            ▼
         Response
```

PostgreSQL is used to store document metadata, while FAISS is responsible for semantic retrieval.

---

# Major Engineering Decisions

## 1. Why Retrieval-Augmented Generation?

A standalone LLM can hallucinate or provide outdated information.

RAG grounds the model's responses using relevant documents retrieved at query time, improving factual accuracy and allowing the knowledge base to be updated without retraining the model.

---

## 2. Why Chunking?

Entire documents are too large to embed effectively and often exceed model context limits.

Splitting documents into meaningful chunks improves retrieval quality and allows only the most relevant information to be passed to the LLM.

---

## 3. Why Sentence Embeddings?

Semantic embeddings capture meaning rather than exact keyword matches.

This enables retrieval even when the user's query is phrased differently from the original documentation.

---

## 4. Why FAISS?

FAISS provides efficient similarity search over high-dimensional embedding vectors.

It is significantly faster than performing brute-force comparisons and is well suited for local semantic search.

---

## 5. Why PostgreSQL?

PostgreSQL is used to store structured metadata such as document information.

FAISS is optimized for vector similarity search, while PostgreSQL is optimized for structured storage and querying.

The two systems complement each other rather than replacing one another.

---

## 6. Prompt Engineering

The retrieved chunks are inserted into a structured prompt before being sent to Gemini.

The prompt instructs the model to answer using only the retrieved context and avoid fabricating unsupported information.

---

# Challenges Encountered

## API Authentication

Initially misunderstood the distinction between ChatGPT subscriptions and API billing.

Resolved by configuring Gemini API access correctly and using environment variables for API keys.

---

## Retrieval Quality

Observed that retrieving larger amounts of context did not necessarily improve answer quality.

Learned that retrieval relevance is more important than simply increasing the amount of context provided.

---

## Duplicate Chunks

Some duplicated document content resulted in repetitive retrieval results.

Resolved by deduplicating chunks before indexing.

---

## Context Size

Initially assumed that providing more context would improve responses.

Found that excessive context often reduced response quality due to irrelevant information.

Relevant context consistently produced better answers.

---

## Metadata Management

Separated semantic retrieval (FAISS) from structured metadata (PostgreSQL), resulting in a cleaner and more maintainable architecture.

---

# Lessons Learned

- More context does not necessarily produce better responses.
- Retrieval quality is more important than retrieval quantity.
- Effective chunking significantly impacts retrieval performance.
- Prompt design strongly influences answer quality.
- Separating vector search from structured storage simplifies system design.
- Modern LLM applications require engineering decisions beyond simply calling an API.

---

# Future Improvements

- Hybrid retrieval (semantic + keyword search)
- Better chunking strategies
- Retrieval reranking
- Conversation memory
- Multi-document reasoning
- Support for additional document formats
- Retrieval evaluation metrics

---

# Key Takeaways

This project provided practical experience with building an end-to-end Retrieval-Augmented Generation pipeline rather than simply interacting with an LLM API.

The primary learnings came from understanding retrieval quality, prompt engineering, semantic search, and the engineering trade-offs involved in designing reliable LLM-powered applications.