import asyncio
from collections.abc import AsyncIterator
from typing import Any

from app.chains.core_chat import core_chat_chain, format_engineering_response


async def stream_core_chat_response(query: str) -> AsyncIterator[str]:
    response = await build_core_chat_response(query)
    for token in tokenize(response):
        await asyncio.sleep(0.035)
        yield token


async def build_core_chat_response(query: str) -> str:
    try:
        structured_response = await run_core_chat_workflow(query)
    except Exception as error:
        return format_ai_error(error)
    return format_engineering_response(structured_response)


async def run_core_chat_workflow(query: str) -> dict:
    return await core_chat_chain.ainvoke({"query": query.strip() or "your engineering request"})


def build_ai_error_response(error: Exception) -> dict[str, Any]:
    message = str(error)
    if "API_KEY_INVALID" in message or "API key not valid" in message:
        reason = "Gemini rejected the configured API key."
        next_action = "Check `ai-service/.env`, replace `GEMINI_API_KEY` with a valid Gemini API key, then restart the AI service."
    elif "404" in message or "not found" in message.lower():
        reason = "Gemini rejected the configured model name."
        next_action = "Check `GEMINI_MODEL` in `ai-service/.env` and use a model available for your Gemini API key."
    else:
        reason = "The AI service failed while calling the configured model."
        next_action = "Check the FastAPI logs for the provider error, then retry after updating configuration."

    return {
        "summary": reason,
        "intent": "configuration_error",
        "assumptions": [
            "The React and NestJS streaming path is reachable.",
            "The failure happened inside the AI service model call.",
        ],
        "steps": [
            {
                "name": "Inspect AI service configuration",
                "detail": "Confirm `GEMINI_API_KEY` and `GEMINI_MODEL` are set in `ai-service/.env`.",
            },
            {
                "name": "Restart the AI service",
                "detail": "Environment changes are read when the FastAPI process starts.",
            },
        ],
        "risks": ["Falling back to the local simulator would hide the provider configuration problem."],
        "next_action": next_action,
    }


def format_ai_error(error: Exception) -> str:
    return format_engineering_response(build_ai_error_response(error))


def tokenize(text: str) -> list[str]:
    parts = text.split(" ")
    return [part + (" " if index < len(parts) - 1 else "") for index, part in enumerate(parts)]
