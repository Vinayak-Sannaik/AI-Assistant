# START
#  ↓
# planner
#  ↓
# requires retrieval?
#  /              \
# yes              no
#  ↓                ↓
# retriever        writer
#  ↓
# validator
#  ↓
# writer
#  ↓
# END

from copy import error
from typing import Any, TypedDict
from pathlib import Path
from uuid import uuid4
from app.workflows.core_chat import (
    core_chat_chain,
    format_engineering_response,
)
from langgraph.checkpoint.memory import (
    MemorySaver,
)
from app.chains.core_chat import format_rag_response
from langgraph.graph import (
    START,
    END,
    StateGraph,
)
from app.schemas.engineering_response import RagResponse
from langgraph.types import ( interrupt, Command)

from app.providers.llm import llm

HIGH_RISK_TERMS = [
    "delete",
    "migration",
    "production",
    "deploy",
    "refactor",
    "database",
]

class AgenticRagState(
    TypedDict,
    total=False,
):
    # USER INPUT
    query: str

    # WORKFLOW STATUS
    status: str
    workflow_events: list[
        dict[str, str]
    ]

    # PLANNER OUTPUT
    requires_retrieval: bool
    retrieval_query: str

    # RETRIEVAL OUTPUT
    retrieved_documents: list[
        dict[str, Any]
    ]

    # VALIDATION OUTPUT
    validation_score: float
    validation_reason: str

    # HUMAN REVIEW
    requires_human_review: bool
    human_approved: bool | None # none- pending/not reviewed yet
    human_review_reason: str
    workflow_id: str

    # FINAL RESPONSE
    final_response: dict[
        str,
        Any,
    ]
    markdown: str

    # ERROR
    error: str

def route_after_planner(
    state: AgenticRagState,
) -> str:

    if state.get(
        "requires_retrieval",
    ):

        return "retriever"

    return "writer"


async def planner_node(
    state: AgenticRagState,
) -> AgenticRagState:

    query = state[
        "query"
    ].lower()

    requires_retrieval = any(
        keyword in query
        for keyword in [
            "codebase",
            "repository",
            "workflow",
            "file",
            ".py",
            "architecture",
            "service",
            "module",
        ]
    )

    retrieval_query = (
        state["query"]
        if requires_retrieval
        else ""
    )

    return {
        **state,

        "status": "completed",

        "requires_retrieval": (
            requires_retrieval
        ),

        "retrieval_query": (
            retrieval_query
        ),

        "workflow_events": [
            *state.get(
                "workflow_events",
                [],
            ),
            {
                "node": "planner",
                "status": "completed",
            },
        ],
    }

def route_human_review(
    state: AgenticRagState,
):
    print("Routing human review with state:")
    print(state)

    if state.get(
        "requires_human_review"
    ):
        return "await_human"

    return "writer"

def human_review_node(
    state: AgenticRagState,
):
    
    print("Human review node received state:")
    print(state)

    query = state.get(
        "query",
        "",
    ).lower()

    risky = any(
        term in query
        for term in HIGH_RISK_TERMS
    )

    #
    # INTERRUPT WORKFLOW
    #

    if risky:
        approval = interrupt({
            "type": (
                "human_review_required"
            ),

            "reason": (
                "High-risk engineering "
                "request detected."
            ),

            "workflow_id": state.get(
                "workflow_id",
            ),
        })

        return {
            **state,

            "human_approved": approval,

            "requires_human_review": False,
        }

    #
    # SAFE TO CONTINUE
    #

    return {
        **state,

        "requires_human_review": (
            False
        ),

        "human_approved": True,
    }

ACTION_WORDS = [
    "explain",
    "read",
    "refactor",
    "delete",
    "analyze",
]
def extract_file_path(
    query: str,
) -> str:
    cleaned = query.lower()

    for word in ACTION_WORDS:
        cleaned = cleaned.replace(
            word,
            "",
        )

    return cleaned.strip()

async def retriever_node(
    state: AgenticRagState,
) -> AgenticRagState:
    
    print("Retriever node received state:")
    print(state)

    retrieval_query = state.get(
        "retrieval_query",
        "",
    )

    retrieved_documents = []

    #
    # SIMPLE FILE RETRIEVAL
    #

    if ".py" in retrieval_query:

        # file_path = (
        #     retrieval_query
        #     .replace(
        #         "Explain",
        #         "",
        #     )
        #     .replace(
        #         "explain",
        #         "",
        #     )
        #     .strip()
        # )
        file_path = extract_file_path(
            retrieval_query,
        )

        path = Path(file_path)

        if path.exists():

            try:

                content = (
                    path.read_text()
                )

                retrieved_documents.append(
                    {
                        "source": file_path,
                        "content": content,
                    }
                )

            except Exception as error:

                return {
                    **state,
                    "status": "failed",
                    "error": str(error),
                }

    return {
        **state,

        "retrieved_documents": (
            retrieved_documents
        ),

        "workflow_events": [
            *state.get(
                "workflow_events",
                [],
            ),
            {
                "node": "retriever",
                "status": "completed",
            },
        ],
    }


async def validator_node(
    state: AgenticRagState,
) -> AgenticRagState:

    documents = state.get(
        "retrieved_documents",
        [],
    )

    #
    # NO DOCUMENTS
    #

    if not documents:

        return {
            **state,

            "validation_score": 0.0,

            "validation_reason": (
                "No documents retrieved."
            ),

            "workflow_events": [
                *state.get(
                    "workflow_events",
                    [],
                ),
                {
                    "node": "validator",
                    "status": "failed",
                },
            ],
        }

    #
    # SIMPLE VALIDATION
    #

    validation_score = 1.0

    validation_reason = (
        "Retrieved documents available."
    )

    return {
        **state,

        "validation_score": (
            validation_score
        ),

        "validation_reason": (
            validation_reason
        ),

        "workflow_events": [
            *state.get(
                "workflow_events",
                [],
            ),
            {
                "node": "validator",
                "status": "completed",
            },
        ],
    }

async def writer_node(
    state: AgenticRagState,
) -> AgenticRagState:

    try:

        query = state.get(
            "query",
            "",
        )

        documents = state.get(
            "retrieved_documents",
            [],
        )

        validation_score = state.get(
            "validation_score",
            0.0,
        )
        # NO VALID GROUNDING
        if validation_score <= 0:

            return {
                **state,

                "status": "failed",

                "markdown": (
                    "# Retrieval Failed\n\n"
                    "No grounded documents "
                    "were available."
                ),

                "workflow_events": [
                    *state.get(
                        "workflow_events",
                        [],
                    ),
                    {
                        "node": "writer",
                        "status": "failed",
                    },
                ],
            }

        # BUILD RETRIEVED CONTEXT
        context = "\n\n".join(
            [
                (
                    f"Source: "
                    f"{doc['source']}\n\n"
                    f"{doc['content']}"
                )
                for doc in documents
            ]
        )

        # STRUCTURED OUTPUT MODEL
        structured_llm = llm.with_structured_output(
            RagResponse
        )

        # GENERATE STRUCTURED RESPONSE
        response = await structured_llm.ainvoke(
            f"""
            You are a senior staff software engineer.

            Analyze the retrieved code deeply.

            Focus on:
            - architectural role
            - design decisions
            - extensibility
            - engineering tradeoffs
            - how components interact
            - why the implementation exists

            Do not just summarize code.

            User Question:
            {query}

            Retrieved Context:
            {context}
            """
        )

        # CONVERT STRUCTURED RESPONSE TO MARKDOWN
        markdown = format_rag_response(
            response
        )


        # RETURN FINAL STATE
        return {
            **state,

            "status": "completed",

            "markdown": markdown,

            "workflow_events": [
                *state.get(
                    "workflow_events",
                    [],
                ),
                {
                    "node": "writer",
                    "status": "completed",
                },
            ],
        }

    except Exception as error:

        print(
            "Writer node failed:",
            str(error),
        )

        return {
            **state,

            "status": "failed",

            "error": str(error),

            "markdown": (
                "# Writer Error\n\n"
                f"{str(error)}"
            ),

            "workflow_events": [
                *state.get(
                    "workflow_events",
                    [],
                ),
                {
                    "node": "writer",
                    "status": "failed",
                },
            ],
        }

def build_agentic_rag_graph():
    graph = StateGraph( AgenticRagState)

    # NODES
    graph.add_node(
        "planner",
        planner_node,
    )
    graph.add_node(
        "retriever",
        retriever_node,
    )
    graph.add_node(
        "validator",
        validator_node,
    )
    graph.add_node(
        "writer",
        writer_node,
    )
    graph.add_node(
        "human_review",
        human_review_node,
    )

    # EDGES
    graph.add_edge(
        START,
        "planner",
    )
    graph.add_conditional_edges(
        "planner",
        route_after_planner,
        {
            "retriever": "retriever",
            "writer": "writer",
        },
    )
    graph.add_edge(
        "retriever",
        "validator",
    )
    graph.add_edge(
        "validator",
        "human_review",
    )

    graph.add_conditional_edges(
        "human_review",
        route_human_review,
        {
            "await_human": END,
            "writer": "writer",
        },
    )
    graph.add_edge(
        "writer",
        END,
    )

    # pause
    # → save graph state
    # → resume later
    memory = MemorySaver()

    return graph.compile(
        checkpointer=memory,
    )

agentic_rag_graph = (
    build_agentic_rag_graph()
)

async def run_agentic_rag_graph(
    query: str,
):
    workflow_id = str(uuid4())
    
    return await (
        agentic_rag_graph.ainvoke(
            {
                "query": query,
                "workflow_id": workflow_id,
                "status": "running",
                "workflow_events": [],
            },
            config={
                "configurable": {
                    "thread_id": workflow_id,
                }
            },
        )
    )

async def resume_agentic_rag_graph(
    workflow_id: str,
    human_approved: bool,
):

    return await (
        agentic_rag_graph.ainvoke(
            Command(
                resume=human_approved
            ),

            config={
                "configurable": {
                    "thread_id": workflow_id,
                }
            },
        )
    )

async def stream_resume_agentic_rag_graph(
    workflow_id: str,
    human_approved: bool,
):

    async for chunk in (
        agentic_rag_graph.astream(
            Command(
                resume=human_approved
            ),

            config={
                "configurable": {
                    "thread_id": workflow_id,
                }
            },

            stream_mode="updates",
        )
    ):

        #
        # WRITER OUTPUT
        #

        if "writer" in chunk:

            writer_state = chunk[
                "writer"
            ]

            markdown = writer_state.get(
                "markdown",
                "",
            )

            for line in markdown.splitlines(
                keepends=True,
            ):

                yield {
                    "type": "token",
                    "content": line,
                }

async def stream_agentic_rag_graph(
    query: str,
):

    workflow_id = str(uuid4())

    async for chunk in (
        agentic_rag_graph.astream(
            {
                "query": query,
                "workflow_id": workflow_id,
                "status": "running",
                "workflow_events": [],
            },

            config={
                "configurable": {
                    "thread_id": workflow_id,
                }
            },

            stream_mode="updates",
        )
    ):

        #
        # INTERRUPT EVENT
        #

        if "__interrupt__" in chunk:

            interrupt_data = (
                chunk["__interrupt__"][0]
                .value
            )

            yield {
                "type": (
                    "human_review_required"
                ),

                "reason": interrupt_data.get(
                    "reason",
                    "",
                ),

                "workflow_id": workflow_id,
            }

            return

        #
        # WRITER OUTPUT
        #

        if "writer" in chunk:

            writer_state = chunk[
                "writer"
            ]

            markdown = writer_state.get(
                "markdown",
                "",
            )

            for line in markdown.splitlines(
                keepends=True,
            ):

                yield {
                    "type": "token",
                    "content": line,
                }