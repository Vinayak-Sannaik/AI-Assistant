# AI Software Engineering Assistant

## Overview

AI Software Engineering Assistant is a distributed multi-agent AI platform designed to help developers automate software engineering workflows.

The project focuses on:
- LangChain
- LangGraph
- multi-agent orchestration
- structured tool calling
- MCP integrations
- workflow systems
- distributed AI architecture

The system intentionally uses a hybrid architecture:
- NestJS as the primary backend platform,
- Python as the AI orchestration service.

This mirrors real-world AI system architecture where:
- Node.js/Java/Go services manage platform/backend concerns,
- Python services handle AI/ML orchestration.

---

# Goals

The project is designed to teach:
- LangChain abstractions,
- LangGraph workflows,
- agent orchestration,
- distributed AI systems,
- structured tool calling,
- MCP integrations,
- AI workflow engineering,
- service-to-service communication.

---

# Primary Use Cases

# 1. Architecture Assistant

### Example

User asks:
```txt
Design migration strategy from monolith to microservices
```

System:
- creates execution plan,
- retrieves architecture patterns,
- identifies bottlenecks,
- generates phased migration strategy.

---

# 2. Repository Analysis

### Example

User asks:
```txt
Analyze scalability issues in this repository
```

System:
- scans repository,
- analyzes architecture,
- identifies anti-patterns,
- generates engineering report.

---

# 3. Engineering Documentation

### Example

User asks:
```txt
Generate API documentation for this module
```

System:
- reads repository files,
- extracts API information,
- generates markdown documentation.

---

# 4. Workflow Planning

### Example

User asks:
```txt
Create deployment strategy for this application
```

System:
- decomposes tasks,
- creates workflow plan,
- identifies risks,
- generates implementation roadmap.

---

# System Architecture

```txt
React Frontend
      ↓
NestJS Backend Gateway
      ↓
+--------------------------------+
| Core Platform APIs             |
+--------------------------------+
      ↓
Python AI Service
(LangChain + LangGraph)
      ↓
+-------------+-------------+
| Tools       | Memory      |
+-------------+-------------+
      ↓
+---------------------------+
| PostgreSQL + PGVector     |
+---------------------------+
      ↓
+---------------------------+
| MCP Servers               |
+---------------------------+
```

---

# Architecture Philosophy

# Why Hybrid Architecture?

The project intentionally separates:
- platform/backend concerns,
- AI orchestration concerns.

---

# NestJS Responsibilities

NestJS handles:
- APIs,
- workflow management,
- persistence,
- websocket streaming,
- orchestration requests,
- backend architecture.

Python handles:
- LangGraph workflows,
- agents,
- AI orchestration,
- retrieval,
- tool execution.

---

# Why This Architecture Matters

This teaches:
- distributed systems,
- service communication,
- AI microservices,
- orchestration boundaries,
- scalable architecture.

This is significantly more valuable than building a single Python monolith.

---

# Frontend Stack

# Framework
- ReactJS
- TypeScript
- Vite

---

# UI
- TailwindCSS
- shadcn/ui

---

# State Management
- Zustand

---

# Networking
- Axios
- SSE/WebSockets

---

# Visualization
- React Flow
- Recharts

---

# Backend Stack

# Main Backend

## Framework
- NestJS

## Responsibilities
- API gateway,
- persistence,
- workflow state management,
- streaming,
- request orchestration.

---

# AI Service

## Framework
- FastAPI

## Responsibilities
- LangChain,
- LangGraph,
- agents,
- workflows,
- tool calling,
- MCP integration.

---

# Infrastructure

# Database
- PostgreSQL

---

# Vector Store
- PGVector

---

# Queue System
- Redis

---

# AI Models

## Cloud Models
- OpenAI GPT models

---

## Local Models
- Ollama
- Llama models

---

## Embeddings
- OpenAI embeddings
- BGE embeddings

---

# Multi-Agent Architecture

# Agents

## Planner Agent
Responsible for:
- task decomposition,
- execution planning,
- workflow creation.

---

## Research Agent
Responsible for:
- retrieval,
- architecture lookup,
- technical research.

---

## Critic Agent
Responsible for:
- hallucination detection,
- architectural validation,
- risk identification.

---

## Code Agent
Responsible for:
- repository analysis,
- code inspection,
- implementation guidance.

---

## Writer Agent
Responsible for:
- formatting final output,
- generating markdown reports,
- summarization.

---

# LangGraph Workflow Engine

The project uses LangGraph for orchestration.

## Features
- graph-based workflows,
- branching,
- retries,
- checkpoints,
- interrupts,
- persistent state.

---

# Example Workflow

```txt
START
  ↓
Receive User Request
  ↓
Planner Agent
  ↓
Need Retrieval?
 ├── YES → Research Agent
 └── NO
  ↓
Need Tool Execution?
 ├── YES → Tool Agent
 └── NO
  ↓
Critic Agent
  ↓
Writer Agent
  ↓
Final Response
  ↓
END
```
```
Frontend
   ↓
NestJS
   ↓
FastAPI Route
   ↓
Service
   ↓
LangChain Chain
   ↓
Prompt
   ↓
LLM
   ↓
Parser
   ↓
Structured Response
```
---

# Structured Tool Calling

Agents can invoke tools safely using structured schemas.

# Tool Categories

## Filesystem Tools
- read files,
- scan repositories,
- inspect folders.

---

## Database Tools
- query PostgreSQL,
- inspect schemas,
- analyze migrations.

---

## Utility Tools
- markdown generation,
- JSON formatting,
- architecture summarization.

---

## API Tools
- GitHub APIs,
- Jira APIs,
- Notion APIs.

---

# MCP Integration

Supports:
- filesystem MCP,
- SQLite MCP,
- Git MCP,
- custom engineering MCP tools.

---

# MCP Use Cases

## Repository Analysis
Agents inspect repositories through MCP filesystem server.

---

## Database Inspection
Agents analyze schemas through MCP database tools.

---

## Git Operations
Agents inspect commits and PRs through MCP Git server.

---

# Lightweight Engineering RAG

RAG exists only to support engineering workflows.

# Knowledge Sources
- architecture documents,
- API specifications,
- engineering standards,
- migration notes,
- system design references.

---

# Retrieval Features
- semantic retrieval,
- hybrid retrieval,
- reranking,
- metadata filtering.

---

# Memory System

# Memory Types

## Conversation Memory
Stores active workflow context.

---

## Episodic Memory
Stores important engineering interactions.

---

## Semantic Memory
Stores persistent embeddings.

---

# Frontend Features

# 1. Chat Workspace

## Features
- streaming AI responses,
- markdown rendering,
- syntax highlighting,
- conversation history.

---

# 2. Workflow Visualization

## Features
- graph visualization,
- workflow execution tracking,
- agent state visualization.

Use:
- React Flow.

---

# 3. Tool Execution Panel

## Features
- inspect executed tools,
- tool inputs/outputs,
- execution logs.

---

# 4. Memory Viewer

## Features
- inspect stored memories,
- memory categories,
- vector retrieval results.

---

# NestJS Backend Responsibilities

# 1. API Gateway

## Responsibilities
- frontend communication,
- routing requests,
- orchestrating AI service calls.

---

# 2. Conversation Management

## Responsibilities
- message persistence,
- workflow history,
- session tracking.

---

# 3. Workflow State Management

## Responsibilities
- workflow metadata,
- execution status,
- retries,
- state persistence.

---

# 4. Streaming Layer

## Responsibilities
- SSE/WebSockets,
- real-time updates,
- workflow progress events.

---

# Python AI Service Responsibilities

# 1. LangGraph Workflows

## Responsibilities
- graph execution,
- agent orchestration,
- branching logic.

---

# 2. LangChain Pipelines

## Responsibilities
- prompts,
- parsers,
- retrievers,
- structured outputs.

---

# 3. Agent Coordination

## Responsibilities
- planner execution,
- critic validation,
- tool invocation.

---

# 4. MCP Tool Execution

## Responsibilities
- filesystem MCP,
- Git MCP,
- DB MCP,
- secure tool orchestration.

---

# Service Communication

Initial communication uses HTTP APIs.

---

# Example Request

## NestJS → Python

```http
POST /ai/execute-workflow
```

---

# Example Payload

```json
{
  "workflowType": "architecture_review",
  "query": "Analyze migration from monolith to microservices",
  "conversationId": "123"
}
```

---

# Example Response

```json
{
  "status": "completed",
  "result": "...",
  "steps": [],
  "toolsUsed": []
}
```

---

# Future Communication Improvements

Future upgrades may include:
- Redis queues,
- RabbitMQ,
- Kafka-based orchestration.

---

# Database Design

# Tables

## conversations

```sql
id
title
created_at
```

---

## messages

```sql
id
conversation_id
role
content
metadata
created_at
```

---

## memories

```sql
id
memory_type
content
embedding
created_at
```

---

## workflow_runs

```sql
id
workflow_name
status
state
created_at
```

---

## tool_executions

```sql
id
tool_name
input
output
status
created_at
```

---

# Recommended Folder Structure

# Frontend

```txt
frontend/
 ├── src/
 │
 ├── components/
 │    ├── chat/
 │    ├── workflow/
 │    ├── tools/
 │    └── memory/
 │
 ├── pages/
 │
 ├── hooks/
 │
 ├── store/
 │
 ├── services/
 │
 └── types/
```

---

# NestJS Backend

```txt
backend/
 ├── src/
 │
 ├── modules/
 │    ├── chat/
 │    ├── workflows/
 │    ├── memory/
 │    ├── tools/
 │    └── ai/
 │
 ├── common/
 │
 ├── database/
 │
 ├── infrastructure/
 │
 └── config/
```

---

# Python AI Service

```txt
ai-service/
 ├── app/
 │
 ├── agents/
 │
 ├── workflows/
 │
 ├── tools/
 │
 ├── memory/
 │
 ├── retrieval/
 │
 ├── mcp/
 │
 ├── services/
 │
 └── core/
```

---

# Development Phases

# Phase 1 — Core Chat System

## Goals
- React chat UI,
- NestJS backend,
- FastAPI AI service,
- streaming responses.

---

# Phase 1 Implementation

This repository now includes the first runnable slice of the hybrid system:

- `frontend/` — React + TypeScript + Vite chat workspace.
- `backend/` — NestJS API gateway with in-memory conversation management.
- `ai-service/` — FastAPI service with streaming workflow endpoints.

## Streaming Flow

```txt
React EventSource
      ↓
NestJS /chat/conversations/:id/stream
      ↓
FastAPI /ai/execute-workflow/stream
      ↓
token events streamed back to the UI
```

## Local Setup

Install Node dependencies:

```bash
npm install
```

Install Python dependencies into the local service dependency folder:

```bash
python3.13 -m pip install --target ai-service/.deps -r ai-service/requirements.txt
```

Run all three services:

```bash
npm run dev
```

Service URLs:

- Frontend: `http://localhost:5173`
- NestJS backend: `http://localhost:3000`
- FastAPI AI service: `http://localhost:8000`

Useful verification commands:

```bash
npm run typecheck
npm run build
npm run lint
PYTHONPATH=ai-service python3.13 -m py_compile ai-service/app/main.py ai-service/app/api/workflow.py ai-service/app/services/core_chat.py
```

The Phase 1 AI service returns a deterministic streamed response. This preserves the frontend/backend streaming contract while leaving the implementation ready for LangChain and LangGraph integration in later phases.

---

# Phase 2 — LangChain Integration

## Goals
- prompts,
- LCEL,
- structured outputs,
- parsers.

---

# Phase 2 Implementation

The AI service now routes core chat requests through LangChain primitives while keeping the Phase 1 streaming contract intact.

- Prompt template: `ai-service/app/prompts/core_chat.py`
- LCEL chain: `ai-service/app/chains/core_chat.py`
- Structured schema: `ai-service/app/schemas/engineering_response.py`
- JSON parser: `ai-service/app/parsers/engineering_response.py`

The current chain uses Gemini when `GEMINI_API_KEY` is set. When the key is blank, it falls back to a deterministic local model simulator. This makes the app runnable without API keys, while still exercising the same LangChain contracts that Gemini uses:

```txt
ChatPromptTemplate
      ↓
Gemini model or local RunnableLambda adapter
      ↓
JsonOutputParser(Pydantic schema)
      ↓
Markdown response formatter
      ↓
SSE token stream
```

`POST /ai/execute-workflow` now returns both `result` markdown and `structuredOutput` JSON. `POST /ai/execute-workflow/stream` continues to stream markdown tokens through NestJS to the React UI.

---

# Phase 3 — LangGraph Workflows

## Goals
- graph execution,
- planner agent,
- writer agent,
- workflow state management.

---

# Phase 3 Implementation

The AI service now wraps the Phase 2 LCEL chain in a minimal LangGraph workflow:

```txt
START
  ↓
planner
  ↓
writer
  ↓
END
```

- Graph implementation: `ai-service/app/workflows/core_chat.py`
- `planner` invokes the existing LangChain/LCEL chain and captures provider/configuration errors.
- `writer` formats the structured response into markdown for the existing SSE chat stream.
- `POST /ai/execute-workflow` includes `structuredOutput.workflowRun` with graph name, status, node events, and error type when applicable.

Success criteria for Phase 3:

- The workflow runs through LangGraph, not a direct chain call.
- `structuredOutput.workflowRun.events` shows `start`, `planner`, and `writer` state transitions.
- The existing React → NestJS → FastAPI SSE stream still emits markdown and `done`.
- With a bad Gemini key/model, the graph returns `status: failed` and a visible configuration response instead of disconnecting.

Tradeoff: this is intentionally a two-node graph shell, not full multi-agent orchestration. It makes LangGraph testable now without introducing speculative agent/tool behavior before Phase 4 and Phase 5.

---

# Phase 4 — Tool Calling

## Goals
- filesystem tools,
- DB tools,
- structured execution.

---

# Phase 5 — Multi-Agent Coordination

## Goals
- planner,
- critic,
- research agent,
- orchestration workflows.

---

# Phase 6 — MCP Integration

## Goals
- filesystem MCP,
- SQLite MCP,
- Git MCP.

---

# Phase 7 — Memory System

## Goals
- episodic memory,
- semantic memory,
- long-term retrieval.

---

# Phase 8 — Production Hardening

## Goals
- retries,
- tracing,
- observability,
- monitoring.

---

# Non-Functional Requirements

# Performance
- async workflows,
- streaming responses,
- background workers.

---

# Reliability
- retries,
- checkpoint recovery,
- workflow persistence.

---

# Security

Initial phase intentionally excludes:
- authentication,
- RBAC,
- multi-tenancy.

Focus remains on:
- orchestration,
- workflows,
- AI architecture.

---

# Future Enhancements

Potential future additions:
- authentication,
- Slack integration,
- GitHub integration,
- browser automation,
- multimodal workflows,
- autonomous agents.

---

# Expected Learning Outcomes

After completing this project, you should understand:
- LangChain deeply,
- LangGraph orchestration,
- multi-agent systems,
- distributed AI architecture,
- MCP integrations,
- structured tool calling,
- AI workflow engineering,
- production AI system design.

---
