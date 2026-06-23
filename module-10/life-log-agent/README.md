# Life Log Agent

AI agent built with Python that demonstrates different memory architectures used in modern LLM applications.

Instead of being a stateless chatbot, the agent can:

* Remember previous conversations (Episodic Memory)
* Store long-term user facts (Semantic Memory)
* Retrieve relevant facts using vector similarity search
* Generate high-level reflections from conversations

---

# Features

## 1. Episodic Memory

Stores every conversation in SQLite.

Example:

```
User: My name is Vinayak.
Assistant: Nice to meet you.

User: I work as a backend developer.
Assistant: That's great.
```

These conversations are persisted and can be reused as context in future interactions.

---

## 2. Semantic Memory

Instead of storing entire conversations, the agent extracts permanent facts.

Example:

Conversation:

```
User: My favorite language is Python.
```

Stored fact:

```
User likes Python.
```

Facts are stored separately from conversations.

---

## 3. Vector Search

Semantic facts are converted into embeddings using SentenceTransformers and indexed with FAISS.

When the user asks a question, the agent:

```
Question
    ↓
Embedding
    ↓
FAISS Similarity Search
    ↓
Relevant Facts
    ↓
LLM Prompt
```

This allows retrieval of long-term information without sending every stored fact to the model.

---

## 4. Reflection Memory

Every few conversations, the agent generates a high-level summary of the user's interests and goals.

Example:

```
User is preparing for backend interviews.

Interested in AI Agents and RAG systems.

Works primarily with Python and FastAPI.
```

These summaries are injected into future prompts as long-term memory.

---

# Project Structure

```
life-log-agent/

├── memory/
│   ├── episodic.py
│   ├── semantic.py
│   ├── reflection.py
│   ├── vector_store.py
│   ├── database.db
│   └── faiss.index
│
├── agent.py
├── app.py
├── config.py
├── .env
├── requirements.txt
└── README.md
```

---

# Architecture

```
                    User
                      │
                      ▼
                +-------------+
                |   app.py    |
                +-------------+
                      │
                      ▼
                +-------------+
                |  agent.py   |
                +-------------+
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
 Episodic        Semantic        Reflection
  Memory          Memory           Memory
(SQLite)      (Facts + FAISS)    (Summaries)
      │               │                │
      └───────────────┼────────────────┘
                      ▼
               Prompt Construction
                      │
                      ▼
                  Groq LLM
                      │
                      ▼
                  AI Response
```

---

# Tech Stack

* Python 3.12
* Groq API
* SQLite
* SentenceTransformers
* FAISS
* python-dotenv
* OpenAI Python SDK (used with Groq OpenAI-compatible API)

---

# Installation

Clone the repository:

```
git clone <repository-url>

cd life-log-agent
```

Create a virtual environment:

```
python3 -m venv .venv
```

Activate it:

macOS/Linux

```
source .venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```
GROQ_API_KEY=your_api_key
GROQ_BASE_URL=https://api.groq.com/openai/v1
MODEL_NAME=llama-3.3-70b-versatile
```

---

# Run

```
python app.py
```

Example:

```
==================================

Life Log Agent

==================================

You: My name is Vinayak

Assistant: Nice to meet you.

You: I like Python.

Assistant: Python is a great language.

You: What do you know about me?

Assistant:
- Your name is Vinayak.
- You like Python.
```

---

# Memory Layers

## Working Memory

Current prompt and active conversation.

---

## Episodic Memory

Stores complete conversation history.

Example:

```
User: I am learning Redis.
Assistant: Great choice.
```

---

## Semantic Memory

Stores extracted long-term facts.

Example:

```
User likes Python.
User works as a backend developer.
User is learning FastAPI.
```

---

## Reflection Memory

Stores high-level summaries generated from multiple conversations.

Example:

```
Preparing for backend interviews.

Interested in AI systems and RAG.

Focuses on backend development.
```

---

# Learning Objectives

This project demonstrates:

* LLM Integration
* Prompt Engineering
* Episodic Memory
* Semantic Memory
* Reflection Memory
* Vector Embeddings
* Similarity Search
* Retrieval-Augmented Generation (RAG)
* SQLite Persistence
* Basic AI Agent Architecture

---

# Future Improvements

* Memory Manager abstraction
* Background memory updates
* Tool calling support
* Memory importance scoring
* Memory conflict resolution
* ChromaDB or pgvector integration
* Streaming responses
* Web search tool integration

---

# License

This project is intended for learning and educational purposes.
