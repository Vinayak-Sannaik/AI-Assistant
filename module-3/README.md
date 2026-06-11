# RAG Question Answering System

## Overview

This project implements a **Retrieval Augmented Generation (RAG)** system from scratch using a modern backend stack.

It allows users to:

* Store documents
* Convert them into embeddings
* Perform semantic search
* Generate grounded answers using an LLM

The system is designed to **reduce hallucinations** by forcing the model to answer using retrieved context.
<img width="1726" height="1042" alt="image" src="https://github.com/user-attachments/assets/96187f44-7aa3-4a91-bb40-bc178bac0016" />
<img width="1385" height="677" alt="image" src="https://github.com/user-attachments/assets/270d518b-e48e-4967-9f0b-a0ae7a20d8b7" />
---

## Architecture

```txt
User Query
   ↓
NestJS API (Fastify)
   ↓
Embedding Service (Python - FastAPI)
   ↓
PostgreSQL + pgvector
   ↓
Similarity Search (Cosine)
   ↓
Top-K Relevant Chunks
   ↓
Prompt Construction
   ↓
Gemini LLM
   ↓
Final Answer
```

---

## Tech Stack

### Backend

* NestJS (Fastify)
* TypeORM
* PostgreSQL (Supabase)

### AI / ML

* sentence-transformers (`all-MiniLM-L6-v2`)
* FastAPI (Python microservice for embeddings)
* Gemini API (LLM)

### Database

* pgvector (vector similarity search)

---

## Core Features

### 1. Document Ingestion

* REST API to store documents
* Automatically splits content into chunks

---

### 2. Chunking Strategy

#### Initial Problem

* Used naive slicing (`text.slice`)
* Broke sentences mid-way
* Resulted in poor embeddings

#### Final Approach

* Sentence-based chunking
* Chunk size ~150 chars
* Preserves semantic meaning

---

### 3. Embeddings

* Generated using local model:

  * `all-MiniLM-L6-v2`
* Runs via Python FastAPI service
* Fully free (no API cost)

---

### 4. Vector Storage

* Stored in PostgreSQL using `pgvector`
* Each chunk has:

  * content
  * embedding vector

---

### 5. Similarity Search (Critical Fix)

#### Initial Mistake

```sql
embedding <-> query_embedding
```

* Uses Euclidean distance
* Produced poor ranking (~1.0+ distances)

---

#### Final Solution

```sql
embedding <=> query_embedding
```

* Uses Cosine similarity
* Correct semantic comparison

---

## Results Comparison

| Method    | Distance Range | Quality |
| --------- | -------------- | ------- |
| Euclidean | ~1.0 – 1.3     | ❌ Poor  |
| Cosine    | ~0.2 – 0.5     | ✅ Good  |

---

### 6. Retrieval Pipeline

```txt
Query → Embedding → Cosine Search → Top 3 Chunks
```

Enhancements:

* Limit results to top 3
* Filter weak matches (distance > 0.7)
* Clean chunk content

---

### 7. LLM Integration (Gemini)

* Uses Gemini API for answer generation
* Strict prompt to prevent hallucination

---

## Prompt Strategy

```txt
You are a strict AI assistant.

Answer ONLY using the context below.
Do NOT add external knowledge.
If the answer is not present, say "I don't know".

Context:
{retrieved_chunks}

Question:
{user_query}

Answer:
```

---

## Example

### Query

```json
{ "query": "What is RAG?" }
```

---

### Retrieved Chunks

```json
[
  {
    "content": "Retrieval Augmented Generation (RAG) is a method...",
    "distance": 0.55
  },
  {
    "content": "RAG helps reduce hallucinations...",
    "distance": 0.42
  }
]
```

---

### Final Answer

```json
{
  "answer": "Retrieval Augmented Generation (RAG) is a method used in artificial intelligence to improve the accuracy of language models. It helps reduce hallucinations by relying on real data instead of only the model’s internal knowledge."
}
```

---

## Key Learnings

### 1. Retrieval is the Core

```txt
RAG = 80% Retrieval + 20% Generation
```

---

### 2. Chunking Matters More Than You Think

Bad chunking → bad embeddings → bad results

---

### 3. Distance Metric is Critical

* Euclidean distance is incorrect for embeddings
* Cosine similarity is required

---

### 4. Data Quality > Model Choice

Better content → better retrieval → better answers

---

### 5. Ranking is Imperfect

Vector similarity:

* Finds relevant chunks ✔
* Does NOT fully understand intent ❌

Fixes:

* Better chunk design
* Light re-ranking

---

### 6. Prompt Controls Hallucination

Weak prompt → LLM ignores context
Strict prompt → grounded answers

---

## Current Status

```txt
✔ Document ingestion
✔ Chunking (sentence-based)
✔ Embeddings (local, free)
✔ Vector DB (pgvector)
✔ Similarity search (cosine)
✔ LLM integration (Gemini)
✔ Grounded answers
```

---

## Limitations

* Small dataset → limited retrieval quality
* No advanced re-ranking
* No hybrid search (keyword + vector)
* No frontend UI yet

---

## Future Improvements

* Add React UI (chat interface)
* Add citations (which chunk was used)
* Implement hybrid search (BM25 + vector)
* Add re-ranking model (cross-encoder)
* Add caching layer (Redis)

---

## Conclusion

This project demonstrates a **production-style RAG pipeline**, focusing on:

* Correct architecture
* Proper vector search
* Grounded LLM responses

Not just making it work — but making it **correct and explainable**.

---

## Author Notes

This system was built iteratively by:

* identifying incorrect assumptions
* debugging real-world issues
* improving retrieval quality step by step

It reflects how real RAG systems are developed in practice.
