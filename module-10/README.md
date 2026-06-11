# AI Email Assistant (LangGraph + Gmail + Groq)

## Overview

AI Email Assistant is a chat-based application that can read emails, summarize them, generate replies, and send emails through Gmail after user approval.

The goal is to learn:

* LangGraph
* LangChain
* Function Calling
* Tool Calling
* Gmail API Integration
* Human-in-the-Loop Workflows
* FastAPI
* React

---

## Problem Statement

Managing emails is repetitive and time-consuming.

Users should be able to interact with their inbox using natural language:

```text
Summarize my latest unread email.

Reply politely to Rahul and tell him we can schedule a meeting next week.

Send the draft.
```

The assistant should decide which Gmail tools to use, generate responses, and require user approval before sending emails.

---

## Features (MVP)

### 1. Read Latest Email

User:

```text
Show my latest unread email.
```

Agent:

```text
Calls Gmail Tool
Returns Email Content
```

---

### 2. Summarize Email

User:

```text
Summarize the latest email.
```

Agent:

```text
Reads Email
Generates Summary
```

---

### 3. Draft Reply

User:

```text
Reply professionally.
```

Agent:

```text
Reads Email
Generates Draft
Shows Draft
```

---

### 4. Human Approval

User:

```text
Send it.
```

Agent:

```text
Checks Draft Exists
Requests Confirmation
Calls Gmail Send Tool
```

No email should be sent automatically.

---

### 5. Send Email

After approval:

```text
Send Email Tool
```

Gmail sends the email.

---

## System Architecture

```text
React Chat UI
       │
       ▼
FastAPI Backend
       │
       ▼
LangGraph Agent
       │
 ┌─────┼─────────────┐
 ▼     ▼             ▼

Groq  Gmail Tools  Memory
LLM
```

---

## Agent Workflow

```text
User Request
      │
      ▼
Agent Node
      │
      ▼
Tool Decision
      │
      ▼
Gmail Tool
      │
      ▼
LLM Response
      │
      ▼
Approval Check
      │
      ▼
Send Email
```

---

## Gmail Tools

### get_latest_email()

Returns:

```json
{
  "subject": "",
  "sender": "",
  "body": ""
}
```

---

### search_emails(query)

Example:

```text
emails from Rahul
```

Returns matching emails.

---

### create_reply_draft()

Input:

```json
{
  "email_content": "",
  "tone": "professional"
}
```

Returns generated draft.

---

### send_email()

Input:

```json
{
  "to": "",
  "subject": "",
  "body": ""
}
```

Sends email through Gmail API.

---

## Tech Stack

### Frontend

* React
* TypeScript
* TailwindCSS

### Backend

* FastAPI
* Python

### AI

* LangGraph
* LangChain
* Groq

### Email

* Gmail API
* OAuth2

---

## Project Structure

```text
ai-email-assistant/

frontend/
├── src/
├── components/
├── pages/

backend/
├── app/
│   ├── agent/
│   ├── tools/
│   ├── gmail/
│   ├── api/
│   └── schemas/

├── main.py
├── requirements.txt

README.md
```

---

## API Endpoints

### POST /chat

Input:

```json
{
  "message": "Reply to Rahul's email"
}
```

Output:

```json
{
  "response": "Generated draft..."
}
```

---

### POST /send

Input:

```json
{
  "draft_id": "123"
}
```

Output:

```json
{
  "status": "sent"
}
```

---

## Learning Outcomes

After completing this project, you will understand:

* LangGraph State Management
* Tool Calling
* Function Calling
* Gmail API Integration
* Agent Workflows
* Human Approval Patterns
* FastAPI Backend Development
* React Chat Interfaces

---

## Future Enhancements

* Email search
* Inbox analytics
* Calendar integration
* Meeting scheduling
* Multi-agent workflow
* MCP Gmail server
* Email categorization
* Vector memory for previous conversations
* RAG over email history

```
```
