import warnings
from typing import Any, AsyncGenerator, TypedDict

warnings.filterwarnings(
    "ignore",
    message="The default value of `allowed_objects` will change in a future version.*",
    category=Warning,
    module="langgraph.checkpoint.base",
)

from langgraph.graph import END, START, StateGraph

from app.chains.core_chat import core_chat_chain, format_engineering_response

from app.tools.registry import TOOLS

# shared workflow memory structure shared between nodes.
# Every node:
# reads state,
# modifies state,
# returns updated state.
class CoreChatState(TypedDict, total=False):
    query: str
    status: str
    structured_response: dict[str, Any]
    markdown: str
    workflow_events: list[dict[str, str]]
    error: str
    # workflow state must carry tool execution data
    tool_name: str
    tool_input:dict[str, Any]
    tool_output: dict[str, Any]

async def tool_node(
    state: CoreChatState,
) -> CoreChatState:

    events = append_event(
        state,
        "tool_executor",
        "started",
    )

    tool_name = state.get(
        "tool_name",
    )

    tool_input = state.get(
        "tool_input",
        {},
    )

    tool_function = TOOLS.get(
    tool_name,
    )

    if not tool_function:

        tool_output = {
            "success": False,
            "error": (
                f"Unknown tool: "
                f"{tool_name}"
            ),
        }

    else:

        tool_output = tool_function(
            **tool_input,
        )

    return {
        **state,

        "tool_output": tool_output,

        "workflow_events": [
            *events,
            {
                "node": "tool_executor",
                "status": "completed",
            },
        ],
    }


def append_event(
    state: CoreChatState,
    node: str,
    status: str,
) -> list[dict[str, str]]:
    existing_events = state.get("workflow_events", [])

    return [
        *existing_events,
        {
            "node": node,
            "status": status,
        },
    ]


async def planner_node(state: CoreChatState) -> CoreChatState:
    started_events = append_event(
        state,
        "planner",
        "started",
    )

    query = state["query"].lower()

    if ( query.startswith("read ") and ".py" in query ):
        file_path = (
            query.replace(
                "read",
                "",
            )
            .strip()
        )

        return {
            **state,

            "status": "completed",

            "tool_name": "read_file",

            "tool_input": {
                "path": file_path,
            },

            "workflow_events": [
                *started_events,
                {
                    "node": "planner",
                    "status": "completed",
                },
            ],
        }
    elif ( query.startswith("list") ):
        dir_path = (
            query.replace(
                "list",
                "",
            )
            .strip()
        )

        return {
            **state,

            "status": "completed",

            "tool_name": "list_files",

            "tool_input": {
                "path": dir_path,
            },

            "workflow_events": [
                *started_events,
                {
                    "node": "planner",
                    "status": "completed",
                },
            ],
        }

    try:
        structured_response = await core_chat_chain.ainvoke(
            {"query": state["query"]}
        )

        completed_state: CoreChatState = {
            **state,
            "status": "completed",
            "structured_response": structured_response,
            "workflow_events": [
                *started_events,
                {
                    "node": "planner",
                    "status": "completed",
                },
            ],
        }

        return completed_state

    except Exception as error:
        failed_state: CoreChatState = {
            **state,
            "status": "failed",
            "structured_response": build_ai_error_response(error),
            "workflow_events": [
                *started_events,
                {
                    "node": "planner",
                    "status": "failed",
                },
            ],
            "error": type(error).__name__,
        }

        return failed_state


async def writer_node(state: CoreChatState) -> CoreChatState:
    started_events = append_event(
        state,
        "writer",
        "started",
    )

    if state.get("tool_output"):
        tool_name = state.get(
        "tool_name",
        )

        tool_output = state[
            "tool_output"
        ]    

        # TOOL FAILED
        if not tool_output.get(
            "success",
        ):

            markdown = (
                "Tool execution failed:\n\n"
                f"{tool_output.get('error')}"
            )
        
        # READ FILE TOOL
        elif (
            tool_name == "read_file"
        ):

            markdown = (
                "# File Content\n\n"
                "```\n"
                f"{tool_output.get('content', '')}\n"
                "```"
            )

        # LIST FILES TOOL
        elif (
            tool_name == "list_files"
        ):

            files = tool_output.get(
                "files",
                [],
            )

            rendered_files = "\n".join(
                [
                    f"- [{item['type']}] {item['name']}"
                    for item in files
                ]
            )

            markdown = (
                "# Directory Listing\n\n"
                f"{rendered_files}"
            )

        # UNKNOWN TOOL
        else:

            markdown = (
                "Unknown tool output."
            )

    else:
        markdown = format_engineering_response(
            state["structured_response"]
        )

    completed_state: CoreChatState = {
        **state,
        "markdown": markdown,
        "workflow_events": [
            *started_events,
            {
                "node": "writer",
                "status": "completed",
            },
        ],
    }

    return completed_state

def route_after_planner(
    state: CoreChatState,
) -> str:

    if state.get("tool_name"):
        return "tool"

    return "writer"

# create workflow runtime
def build_core_chat_graph():
    graph = StateGraph(CoreChatState)

    graph.add_node("planner", planner_node)
    graph.add_node("writer", writer_node)
    graph.add_node("tool_executor", tool_node)

    graph.add_edge(START, "planner")
    graph.add_conditional_edges("planner",route_after_planner,
        {
            "tool": "tool_executor",
            "writer": "writer",
        },
    )
    graph.add_edge(
    "tool_executor",
    "analyzer",
    )
    graph.add_edge("writer", END)

    return graph.compile()


core_chat_graph = build_core_chat_graph()


async def run_core_chat_graph(
    query: str,
) -> CoreChatState:
    normalized_query = query.strip() or "your engineering request"

    initial_state: CoreChatState = {
        "query": normalized_query,
        "status": "running",
        "workflow_events": [
            {
                "node": "start",
                "status": "completed",
            }
        ],
    }

    return await core_chat_graph.ainvoke(initial_state)


async def stream_core_chat_graph(
    query: str,
) -> AsyncGenerator[dict[str, Any], None]:

    normalized_query = query.strip() or "your engineering request"

    state: CoreChatState = {
        "query": normalized_query,
        "status": "running",
        "workflow_events": [],
    }

    #
    # START EVENT
    #

    start_event = {
        "type": "workflow",
        "node": "start",
        "status": "completed",
    }

    yield start_event

    #
    # PLANNER STARTED
    #

    planner_started_event = {
        "type": "workflow",
        "node": "planner",
        "status": "started",
    }

    yield planner_started_event

    #
    # RUN PLANNER
    #

    state = await planner_node(state)

    #
    # PLANNER RESULT
    #

    planner_final_status = (
        "failed"
        if state.get("status") == "failed"
        else "completed"
    )

    planner_completed_event = {
        "type": "workflow",
        "node": "planner",
        "status": planner_final_status,
    }

    yield planner_completed_event

    if state.get("tool_name"):
        tool_started_event = {
            "type": "workflow",
            "node": "tool_executor",
            "status": "started",
        }

        yield tool_started_event

        state = await tool_node(state)

        tool_completed_event = {
            "type": "workflow",
            "node": "tool_executor",
            "status": "completed",
        }

        yield tool_completed_event

    #
    # WRITER STARTED
    #

    writer_started_event = {
        "type": "workflow",
        "node": "writer",
        "status": "started",
    }

    yield writer_started_event

    #
    # RUN WRITER
    #

    state = await writer_node(state)

    #
    # STREAM MARKDOWN TOKENS
    #

    markdown = state.get("markdown", "")

    for token in markdown.split(" "):
        yield {
            "type": "token",
            "content": token + " ",
        }

    #
    # WRITER COMPLETED
    #

    writer_completed_event = {
        "type": "workflow",
        "node": "writer",
        "status": "completed",
    }

    yield writer_completed_event

    #
    # DONE
    #

    yield {
        "type": "done",
        "workflowRun": {
            "name": "core_chat_graph",
            "status": state.get("status", "completed"),
            "events": state.get("workflow_events", []),
            "error": state.get("error"),
        },
    }


def build_structured_output(
    state: CoreChatState,
) -> dict[str, Any]:
    return {
        **state["structured_response"],
        "workflowRun": {
            "name": "core_chat_graph",
            "status": state["status"],
            "events": state.get("workflow_events", []),
            "error": state.get("error"),
        },
    }


def build_ai_error_response(
    error: Exception,
) -> dict[str, Any]:

    message = str(error)

    if (
        "API_KEY_INVALID" in message
        or "API key not valid" in message
    ):
        reason = "Gemini rejected the configured API key."

        next_action = (
            "Check `ai-service/.env`, replace "
            "`GEMINI_API_KEY` with a valid "
            "Gemini API key, then restart "
            "the AI service."
        )

    elif (
        "404" in message
        or "not found" in message.lower()
    ):
        reason = "Gemini rejected the configured model name."

        next_action = (
            "Check `GEMINI_MODEL` in "
            "`ai-service/.env` and use a "
            "model available for your "
            "Gemini API key."
        )

    else:
        reason = (
            "The AI service failed while "
            "calling the configured model."
        )

        next_action = (
            "Check the FastAPI logs for the "
            "provider error, then retry "
            "after updating configuration."
        )

    return {
        "summary": reason,
        "intent": "configuration_error",
        "assumptions": [
            "The React and NestJS streaming path is reachable.",
            "The failure happened inside the AI service workflow.",
        ],
        "steps": [
            {
                "name": "Inspect AI service configuration",
                "detail": (
                    "Confirm `GEMINI_API_KEY` "
                    "and `GEMINI_MODEL` are "
                    "set in `ai-service/.env`."
                ),
            },
            {
                "name": "Restart the AI service",
                "detail": (
                    "Environment changes are "
                    "read when the FastAPI "
                    "process starts."
                ),
            },
        ],
        "risks": [
            "Falling back to the local simulator "
            "would hide the provider configuration problem."
        ],
        "next_action": next_action,
    }