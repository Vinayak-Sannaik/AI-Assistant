# Todo MCP Server — Project Specification

## Overview

A learning-focused MCP (Model Context Protocol) server built with Python and FastMCP that demonstrates all major MCP concepts including Tools, Resources, Prompts, stdio transport, validation, persistence, and MCP internals.

The project is intentionally designed to teach both practical MCP development and the underlying protocol architecture used by AI agents.

---

## Technology Stack

| Component         | Choice                  |
| ----------------- | ----------------------- |
| Language          | Python                  |
| MCP Framework     | FastMCP                 |
| Learning Approach | FastMCP + MCP Internals |
| Transport         | stdio                   |
| Storage           | todos.json              |
| User Model        | Single User             |
| Validation        | Strict                  |
| Response Format   | Structured JSON         |

---

## Todo Schema

```json
{
  "id": 1,
  "title": "Learn MCP",
  "description": "Read MCP architecture docs",
  "status": "pending",
  "priority": "high",
  "tags": ["learning", "ai"],
  "created_at": "2026-06-04T10:00:00Z",
  "updated_at": "2026-06-04T10:00:00Z"
}
```

### Status Values

* pending
* in_progress
* completed
* cancelled

### Priority Values

* low
* medium
* high
* critical

---

## Validation Rules

### Title

* Required
* Minimum length: 3
* Maximum length: 200

### Description

* Optional
* Maximum length: 2000

### Status

Allowed values:

* pending
* in_progress
* completed
* cancelled

### Priority

Allowed values:

* low
* medium
* high
* critical

### Tags

* Optional
* Unique values only

---

## Tool Definitions

### Core CRUD Tools

```text
add_todo
get_todo
list_todos
update_todo
delete_todo
```

### Search Tool

```text
search_todos
```

Supported filters:

```text
query
status
priority
tags
limit
offset
sort_by
order
```

### Pagination

```python
list_todos(limit=20, offset=0)

search_todos(
    status="pending",
    limit=20,
    offset=40
)
```

### Sorting

Supported fields:

```text
created_at
updated_at
priority
title
```

Supported orders:

```text
asc
desc
```

---

## Resource Definitions

Read-only MCP resources:

```text
resource://todos

resource://todos/pending

resource://todos/completed

resource://todos/high-priority

resource://todos/recent

resource://tags
```

Purpose:

* Demonstrate MCP Resource registration
* Learn Resource URI design
* Understand Tool vs Resource responsibilities

---

## Prompt Definitions

Context-aware MCP prompts:

```text
plan_my_day

prioritize_my_work

sprint_summary

learning_roadmap
```

Purpose:

* Demonstrate Prompt registration
* Learn prompt templating
* Understand Prompt vs Tool differences
* Inject todo context into LLM workflows

---

## Response Format

All tools return structured JSON.

### Success Response

```json
{
  "success": true,
  "message": "Todo created successfully",
  "data": {}
}
```

### Error Response

```json
{
  "success": false,
  "message": "Invalid priority",
  "error_code": "INVALID_PRIORITY"
}
```

---

## Project Structure

```text
todo-mcp-server/
│
├── src/
│   ├── server.py
│   ├── models/
│   ├── tools/
│   ├── resources/
│   ├── prompts/
│   ├── storage/
│   ├── validators/
│   └── utils/
│
├── data/
│   └── todos.json
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

## Learning Roadmap

### Phase 1 — MCP Tools

Learn:

* MCP fundamentals
* FastMCP basics
* Tool registration
* stdio transport

Build:

```text
add_todo
get_todo
list_todos
```

---

### Phase 2 — Persistence & Validation

Learn:

* JSON persistence
* Input validation
* Tool schemas
* Error handling

Build:

```text
update_todo
delete_todo
search_todos
```

---

### Phase 3 — MCP Resources

Learn:

* Resource registration
* Resource URIs
* Read-only data exposure

Build:

```text
resource://todos
resource://tags
resource://todos/pending
...
```

---

### Phase 4 — MCP Prompts

Learn:

* Prompt registration
* Prompt templates
* Context injection

Build:

```text
plan_my_day
prioritize_my_work
sprint_summary
learning_roadmap
```

---

### Phase 5 — MCP Internals

Study complete execution flow:

```text
VS Code / Claude Desktop
        ↓
MCP Client
        ↓
stdio
        ↓
FastMCP Server
        ↓
Tools / Resources / Prompts
        ↓
todos.json
```

Goal:

Understand both how to build MCP servers and how the MCP protocol works internally.
