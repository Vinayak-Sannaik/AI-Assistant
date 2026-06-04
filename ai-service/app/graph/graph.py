from app.graph.state import AgenticRagState

from langgraph.graph import (
    START,
    END,
    StateGraph,
)
from langgraph.checkpoint.memory import (
    MemorySaver,
)

from app.graph.nodes.planner import planner_node
from app.graph.nodes.retriever import retriever_node
from app.graph.nodes.validator import validator_node
from app.graph.nodes.human_review import human_review_node
from app.graph.nodes.explain import explain_node
from app.graph.nodes.refactor import refactor_node
from app.graph.nodes.delete import delete_node
from app.graph.nodes.create import create_node
from app.graph.nodes.writer import writer_node
from app.graph.nodes.repository_analyzer import repository_analyzer_node

from app.graph.nodes.routers.planner_router import route_after_planner
from app.graph.nodes.routers.human_review_router import route_after_human_review

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

    graph.add_node(
        "explain",
        explain_node,
    )

    graph.add_node(
        "refactor",
        refactor_node,
    )

    graph.add_node(
        "delete",
        delete_node,
    )

    graph.add_node(
        "create",
        create_node,
    )

    graph.add_node(
        "repository_analyzer",
        repository_analyzer_node,
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
            "repository_analyzer":
                "repository_analyzer",

            "retriever":
                "retriever",

            "writer":
                "writer",
        },
    )

    graph.add_edge(
        "repository_analyzer",
        "writer",
    )
    graph.add_edge(
        "retriever",
        "validator",
    )

    graph.add_conditional_edges(
        "human_review",
        route_after_human_review,
        {
            "explain": "explain",
            "refactor": "refactor",
            "delete": "delete",
            "create": "create",
        },
    )
    
    graph.add_edge(
        "explain",
        "writer",
    )

    graph.add_edge(
        "refactor",
        "writer",
    )

    graph.add_edge(
        "delete",
        "writer",
    )

    graph.add_edge(
        "create",
        "writer",
    )
    graph.add_edge(
        "validator",
        "human_review",
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
