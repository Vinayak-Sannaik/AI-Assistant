# Module VIII Project — Enterprise RAG Assistant

## Goal

Build a production-style Retrieval-Augmented Generation (RAG) system that progressively introduces enterprise RAG concepts such as hybrid retrieval, re-ranking, memory, observability, hallucination reduction, and performance optimization.

---

# Tech Stack

| Layer | Technology |
|---------|------------|
| Workflow Orchestration | LangGraph |
| LLM | Gemini 2.x |
| Embeddings | BAAI/bge-small-en-v1.5 (Local) |
| Re-Ranker | BAAI/bge-reranker-base |
| Vector Database | ChromaDB |
| Keyword Search | BM25 |
| Monitoring & Tracing | LangSmith |
| Backend API | FastAPI |
| Memory Storage | SQLite / JSON |
| Document Loading | LangChain Document Loaders |

---

# Final Architecture

```text
                          User Query
                               │
                               ▼
                      Query Analyzer
                               │
                               ▼
                    Multi Query Expansion
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
          BM25 Retrieval               Chroma Retrieval
                │                             │
                └──────────────┬──────────────┘
                               ▼
                       Candidate Chunks
                               │
                               ▼
                     Cross Encoder Re-Ranker
                               │
                               ▼
                    Context Fusion & Compression
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
         Short-Term Memory          Persistent Memory
                │                             │
                └──────────────┬──────────────┘
                               ▼
                          Gemini LLM
                               │
                               ▼
                      Grounded Response
                               │
                               ▼
                          LangSmith
```

---

# Phase 1 — Basic RAG Foundation

## Objective

Build the simplest working RAG pipeline.

### Features

- Document ingestion
- Text chunking
- Local embedding generation
- Chroma vector storage
- Semantic retrieval
- Gemini answer generation

### Workflow

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Retriever
    ↓
Gemini
```

### Concepts Covered

- RAG fundamentals
- Embeddings
- Vector databases
- Semantic search
- Prompt grounding

### Deliverable

A chatbot that answers questions from uploaded documents.

---

# Phase 2 — Conversational Memory

## Objective

Enable the assistant to remember conversation context.

### Features

### Short-Term Memory

Store current conversation messages.

Example:

```json
{
  "messages": []
}
```

### Persistent Memory

Store user-specific information.

Example:

```json
{
  "preferences": [],
  "topics": []
}
```

### Workflow

```text
User Query
      ↓
Memory Retrieval
      ↓
Document Retrieval
      ↓
Gemini
```

### Concepts Covered

- Session memory
- Long-term memory
- Context injection

### Deliverable

Assistant remembers previous questions and user preferences.

---

# Phase 3 — Hybrid Search

## Objective

Improve retrieval quality.

### Features

### Semantic Search

```text
ChromaDB
```

### Lexical Search

```text
BM25
```

### Hybrid Retrieval

```text
Final Results =
Vector Results +
Keyword Results
```

### Workflow

```text
Query
   ↓
BM25 Search
   ↓
Chroma Search
   ↓
Merge Results
```

### Concepts Covered

- Hybrid retrieval
- Recall improvement
- Enterprise search patterns

### Deliverable

Better retrieval for exact keywords and semantic queries.

---

# Phase 4 — Multi-Query Retrieval

## Objective

Improve recall for ambiguous questions.

### Features

Generate multiple search queries.

Example:

```text
Original:
How does authentication work?

Generated:
- JWT authentication
- OAuth flow
- Session authentication
- API authentication
```

### Workflow

```text
Question
     ↓
Query Expansion
     ↓
Multiple Retrievals
     ↓
Merge Results
```

### Concepts Covered

- Query expansion
- Recall optimization

### Deliverable

Higher-quality retrieval coverage.

---

# Phase 5 — Re-Ranking

## Objective

Filter noisy retrieval results.

### Features

Use Cross Encoder Re-Ranker.

Model:

```text
BAAI/bge-reranker-base
```

### Workflow

```text
Top 20 Chunks
        ↓
Cross Encoder
        ↓
Top 5 Chunks
```

### Concepts Covered

- Precision optimization
- Cross encoders
- Ranking systems

### Deliverable

More relevant context passed to Gemini.

---

# Phase 6 — Context Fusion & Compression

## Objective

Reduce token usage while preserving information.

### Features

- Merge overlapping chunks
- Remove duplicate information
- Compress context before LLM call

### Workflow

```text
20 Chunks
     ↓
Fusion
     ↓
Compression
     ↓
Gemini
```

### Concepts Covered

- Context engineering
- Token optimization
- Cost reduction

### Deliverable

Smaller prompts with better quality.

---

# Phase 7 — Hallucination Reduction

## Objective

Increase answer reliability.

### Features

- Ground responses on retrieved context
- Source citations
- Confidence scoring
- Retrieval quality validation

### Rules

```text
If context unavailable:
Return "I don't know"
```

### Workflow

```text
Retrieved Context
       ↓
Validation
       ↓
Grounded Prompt
       ↓
Gemini
```

### Concepts Covered

- Grounding
- Trustworthiness
- AI safety basics

### Deliverable

Reduced hallucinated answers.

---

# Phase 8 — Query Planning & Multi-Hop Reasoning

## Objective

Handle complex questions.

### Example

```text
Who created LangGraph and
what products do they offer?
```

### Workflow

```text
Question
      ↓
Planner
      ↓
Sub Query 1
      ↓
Sub Query 2
      ↓
Combine Results
      ↓
Answer
```

### Concepts Covered

- Query decomposition
- Multi-hop retrieval
- Agentic reasoning

### Deliverable

Assistant answers multi-step questions.

---

# Phase 9 — Cost & Latency Optimization

## Objective

Make the system production-ready.

### Features

### Embedding Cache

```text
Avoid regenerating embeddings
```

### Retrieval Cache

```text
Reuse retrieval results
```

### Response Cache

```text
Reuse previous answers
```

### Dynamic Top-K

```text
Easy Query → Top 3

Hard Query → Top 10
```

### Concepts Covered

- Cost optimization
- Latency optimization
- Scalability

### Deliverable

Faster and cheaper RAG pipeline.

---

# Phase 10 — Monitoring & Evaluation

## Objective

Measure system quality.

### LangSmith Integration

Track:

- Traces
- Retrieval flow
- Prompt execution
- LLM latency
- Failures

### Metrics Dashboard

Monitor:

```text
Retrieval Precision

Average Similarity Score

Response Latency

Token Consumption

Cost Per Query

Cache Hit Rate

Hallucination Rate

User Feedback Score
```

### Concepts Covered

- Observability
- Production monitoring
- AI evaluation

### Deliverable

Enterprise-grade monitoring dashboard.

---