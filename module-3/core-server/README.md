# RAG System (Retrieval Augmented Generation)

## Overview

This project implements a **domain-specific RAG (Retrieval Augmented Generation) system** using:

* NestJS (Backend API)
* FastAPI (Python AI service)
* PostgreSQL + pgvector (Vector database)
* Sentence Transformers (Local embeddings)

The system enables:

1. Storing documents
2. Chunking content
3. Generating embeddings
4. Performing semantic search
5. Retrieving relevant context

---

Start Project:
nest start --watch backend API.
uvicorn main:app --reload --port 8000 ai-service API.
npm run dev web

Migration Generate new file:
npm run typeorm -- migration:generate src/migrations/AddTsvColumn -d src/data-source.ts

RUN Migration:
npm run typeorm -- migration:run -d src/data-source.ts



## Architecture

```
User Request
   ↓
NestJS API
   ↓
Chunking Layer
   ↓
Python AI Service (Embeddings)
   ↓
PostgreSQL (pgvector)
   ↓
Similarity Search
```

---

## What We Built Step-by-Step

### 1. Document Ingestion

* Developed REST APIs to store documents
* Stored raw content in PostgreSQL

---

### 2. Chunking (Initial Mistake + Fix)

#### ❌ Initial Approach:

```ts
text.slice(start, end)
```

**Problems:**

* Broke sentences mid-way
* Produced meaningless chunks
* Resulted in poor embeddings → weak retrieval

#### ✅ Fix:

* Switched to **sentence-based chunking**
* Preserved semantic meaning

---

### 3. Embeddings

* Built a Python microservice using:

  * `sentence-transformers`
  * Model: `all-MiniLM-L6-v2`
* Generated embeddings locally (completely free)

---

### 4. Storing Embeddings

* Used `pgvector` in PostgreSQL
* Stored embeddings in a `vector` column

---

### 5. Similarity Search (Critical Learning)

#### ❌ Initial Approach (Incorrect):

```sql
embedding <-> query_embedding
```

This uses **Euclidean distance**

**Problems:**

* Poor semantic ranking
* High distance values (~1.0+)
* Weak similarity signals

---

#### ✅ Fixed Approach (Correct):

```sql
embedding <=> query_embedding
```

This uses **Cosine similarity**

---

## Why Cosine Similarity?

Embeddings represent **direction (semantic meaning)** rather than magnitude.

### Euclidean Distance:

* Measures raw distance
* Sensitive to vector scale
* Not suitable for semantic comparison

### Cosine Similarity:

* Measures angle between vectors
* Captures semantic similarity
* Standard approach in NLP systems

---

## Results Comparison

| Approach          | Distance Range | Quality |
| ----------------- | -------------- | ------- |
| Euclidean (`<->`) | ~1.0 – 1.3     | ❌ Poor  |
| Cosine (`<=>`)    | ~0.2 – 0.4     | ✅ Good  |

---

## 6. Chunk Size Optimization

#### ❌ Initial:

```
chunk size = 500
```

**Problems:**

* Too large
* Low precision
* Weak matching

#### ✅ Fix:

```
chunk size = 150
overlap = 30
```

**Result:**

* Improved semantic matching
* Better retrieval accuracy

---

## Final Retrieval Flow

```
User Query
   ↓
Convert to Embedding
   ↓
Cosine Similarity Search (pgvector)
   ↓
Top-K Relevant Chunks
```

---

## Example Query

```
"What is RAG?"
```

### Output:

```json
[
  {
    "content": "Retrieval Augmented Generation (RAG) is a method...",
    "distance": 0.32
  }
]
```

---

## Key Learnings

### 1. Retrieval > LLM

```
RAG = 80% Retrieval + 20% Generation
```

---

### 2. Chunking Quality is Critical

Bad chunking → bad embeddings → poor retrieval

---

### 3. Distance Metric Matters

Using the wrong metric leads to incorrect results

---

### 4. Data Quality > Model Choice

Better content → stronger embeddings → improved results

---

### 5. ORMs Don’t Handle Everything

* `pgvector` required manual handling
* Raw SQL queries were necessary

---

## Current Status

```
✔ Document ingestion
✔ Chunking (sentence-based)
✔ Embeddings (local)
✔ Vector storage (pgvector)
✔ Similarity search (cosine)
❌ Answer generation (next step)
```

---

## Next Steps

* Integrate an LLM for answer generation
* Improve prompt engineering
* Add filtering and ranking mechanisms
* Optimize using vector indexes (HNSW)

---

## Tech Stack

* NestJS (Fastify)
* TypeORM
* PostgreSQL (Supabase)
* pgvector
* FastAPI
* sentence-transformers

---

## Conclusion

This project demonstrates a **production-style RAG pipeline**, focusing on:

* Correct data flow
* Proper vector search implementation
* Strong understanding of retrieval mechanics

The goal is not just to make the system work, but to ensure it works **correctly and efficiently**.
