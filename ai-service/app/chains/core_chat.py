import json
from typing import Any

from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.settings import get_settings
from app.parsers.engineering_response import engineering_response_parser
from app.prompts.core_chat import CORE_CHAT_PROMPT
from app.schemas.engineering_response import EngineeringAssistantResponse


def _simulate_structured_model(prompt_value: Any) -> str:
    query = _extract_human_query(prompt_value)
    intent = _classify_intent(query)
    payload = EngineeringAssistantResponse(
        summary=f"Created a practical {intent.replace('_', ' ')} response for: {query}",
        intent=intent,
        assumptions=[
            "The system deterministic and local so the streaming contract remains stable.",
            "External model calls will be introduced behind the same LCEL chain interface later.",
        ],
        steps=[
            {
                "name": "Clarify the engineering objective",
                "detail": "Restate the request, identify the target system boundary, and name the decision the user needs to make.",
            },
            {
                "name": "Plan the workflow",
                "detail": "Break the work into promptable steps that can later become LangGraph nodes or agent tasks.",
            },
            {
                "name": "Return structured output",
                "detail": "Emit validated JSON so the gateway, UI, and future workflow engine can consume predictable fields.",
            },
        ],
        risks=[
            "A deterministic local chain is useful for scaffolding but does not replace model reasoning.",
            "Future LLM responses must be validated and retried when structured parsing fails.",
        ],
        next_action="Add a real chat model binding and retry policy while preserving the existing parser contract.",
    )
    return payload.model_dump_json()


def _extract_human_query(prompt_value: Any) -> str:
    messages = prompt_value.to_messages()
    for message in reversed(messages):
        if message.type == "human":
            return str(message.content).strip() or "the engineering request"
    return "the engineering request"


def _classify_intent(query: str) -> str:
    normalized = query.lower()
    if any(term in normalized for term in ["document", "docs", "api documentation"]):
        return "documentation"
    if any(term in normalized for term in ["repository", "repo", "codebase", "scalability"]):
        return "repository_analysis"
    if any(term in normalized for term in ["deploy", "workflow", "roadmap", "plan"]):
        return "workflow_planning"
    return "architecture_assistant"

def build_core_chat_chain():
    settings = get_settings()
    if settings.gemini_api_key:
        model = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.gemini_api_key,
            temperature=0,
        )
        #LangChain Expression Language. 
        return CORE_CHAT_PROMPT | model | engineering_response_parser

    return CORE_CHAT_PROMPT | RunnableLambda(_simulate_structured_model) | engineering_response_parser


core_chat_chain = build_core_chat_chain()


def format_engineering_response(response: dict[str, Any]) -> str:
    steps = response.get("steps", [])
    assumptions = response.get("assumptions", [])
    risks = response.get("risks", [])

    sections = [
        response["summary"],
        f"**Intent:** `{response['intent']}`",
        _format_list("Assumptions", assumptions),
        _format_steps(steps),
        _format_list("Risks", risks),
        f"**Next action:** {response['next_action']}",
    ]
    return "\n\n".join(section for section in sections if section)


def _format_list(title: str, items: list[str]) -> str:
    if not items:
        return ""
    rendered = "\n".join(f"- {item}" for item in items)
    return f"**{title}:**\n{rendered}"


def _format_steps(steps: list[dict[str, str]]) -> str:
    if not steps:
        return ""
    rendered = "\n".join(f"{index}. **{step['name']}**: {step['detail']}" for index, step in enumerate(steps, start=1))
    return f"**Recommended steps:**\n{rendered}"


def response_to_json(response: dict[str, Any]) -> str:
    return json.dumps(response, indent=2)
