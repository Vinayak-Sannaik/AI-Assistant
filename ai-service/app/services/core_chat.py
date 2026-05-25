import asyncio
from collections.abc import AsyncIterator

from app.workflows.core_chat import build_structured_output, run_core_chat_graph


async def stream_core_chat_response(query: str) -> AsyncIterator[str]:
    response = await build_core_chat_response(query)
    for token in tokenize(response):
        await asyncio.sleep(0.035)
        yield token


async def build_core_chat_response(query: str) -> str:
    state = await run_core_chat_graph(query)
    return state["markdown"]


async def run_core_chat_workflow(query: str) -> dict:
    state = await run_core_chat_graph(query)
    return build_structured_output(state)


def tokenize(text: str) -> list[str]:
    parts = text.split(" ")
    return [part + (" " if index < len(parts) - 1 else "") for index, part in enumerate(parts)]
