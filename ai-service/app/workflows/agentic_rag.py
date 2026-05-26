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
from app.workflows.core_chat import (
    core_chat_chain,
    format_engineering_response,
)

from app.chains.core_chat import format_rag_response
from langgraph.graph import (
    START,
    END,
    StateGraph,
)


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
    human_approved: bool

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

        file_path = (
            retrieval_query
            .replace(
                "Explain",
                "",
            )
            .replace(
                "explain",
                "",
            )
            .strip()
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

    #
    # NO VALID GROUNDING
    #

    if validation_score <= 0:

        markdown = (
            "# Retrieval Failed\n\n"
            "No grounded documents "
            "were available."
        )

        return {
            **state,
            "markdown": markdown,
        }

    #
    # BUILD CONTEXT
    #

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

    #
    # GROUNDED GENERATION
    #

    try:
        final_response = await core_chat_chain.ainvoke(
            {
                "query": (
                    "Answer the user's question "
                    "using ONLY the retrieved "
                    "documents.\n\n"
                    f"User Question:\n"
                    f"{query}\n\n"
                    f"Retrieved Context:\n"
                    f"{context}"
                )
            }
        )
        
    except Exception as error:

        markdown = (
            "# Writer Failure\n\n"
            f"{str(error)}"
        )

        return {
            **state,

            "status": "failed",

            "error": str(error),

            "markdown": markdown,
        }

    markdown = (
        format_rag_response(
            final_response
        )
    )

    # Source-backed responses
    sources = "\n".join(
        [
            f"- {doc['source']}"
            for doc in documents
        ]
    )

    markdown += (
        "\n\n---\n\n"
        "# Sources\n\n"
        f"{sources}"
    )

    return {
        **state,

        "final_response": (
            final_response
        ),

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
        "writer",
    )
    graph.add_edge(
        "writer",
        END,
    )

    return graph.compile()

agentic_rag_graph = (
    build_agentic_rag_graph()
)

async def run_agentic_rag_graph(
    query: str,
):

    return await (
        agentic_rag_graph.ainvoke(
            {
                "query": query,
                "status": "running",
                "workflow_events": [],
            }
        )
    )

async def stream_agentic_rag_graph(
    query: str,
):

    state = await (
        run_agentic_rag_graph(
            query,
        )
    )

    markdown = state.get(
        "markdown",
        "",
    )

    for word in markdown.split():

        yield {
            "type": "token",
            "content": (
                word + " "
            ),
        }