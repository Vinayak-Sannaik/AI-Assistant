import asyncio
from collections.abc import AsyncIterator


async def stream_core_chat_response(query: str) -> AsyncIterator[str]:
    response = build_core_chat_response(query)
    for token in tokenize(response):
        await asyncio.sleep(0.035)
        yield token


def build_core_chat_response(query: str) -> str:
    normalized = query.strip() or "your engineering request"
    return (
        "I can help with that.\n\n"
        f"**Request understood:** {normalized}\n\n"
        "For Phase 1, this response is streamed from the FastAPI AI service through the NestJS gateway into the React chat UI. "
        "The current service is intentionally lightweight, so the next phases can replace this mock response with LangChain prompts, "
        "LangGraph workflow execution, tools, memory, and MCP integrations without changing the chat contract.\n\n"
        "**Suggested next step:** add LangChain prompt templates and structured workflow events while keeping this SSE path intact."
    )


def tokenize(text: str) -> list[str]:
    parts = text.split(" ")
    return [part + (" " if index < len(parts) - 1 else "") for index, part in enumerate(parts)]
