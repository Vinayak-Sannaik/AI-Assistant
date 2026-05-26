from app.workflows.core_chat import (
    run_core_chat_graph,
    stream_core_chat_graph,
)

from app.workflows.agentic_rag import (
    run_agentic_rag_graph,
)

from app.workflows.agentic_rag import (
    stream_agentic_rag_graph,
)

WORKFLOW_RUNNERS = {
    "core_chat": (
        run_core_chat_graph
    ),

    "agentic_rag": (
        run_agentic_rag_graph
    ),
}


WORKFLOW_STREAMS = {
    "core_chat": (
        stream_core_chat_graph
    ),

    "agentic_rag": (
        stream_agentic_rag_graph
    ),
}