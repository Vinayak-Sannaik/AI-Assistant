from app.graph.state import AgenticRagState

async def planner_node(
    state: AgenticRagState,
) -> AgenticRagState:

    query = state[
        "query"
    ].lower()
    
    intent = "explain"

    if any(
        word in query
        for word in [
            "delete",
            "remove",
        ]
    ):
        intent = "delete"
    
    elif any(
    word in query
    for word in [
        "refactor",
        "improve",
        "optimize",
    ]
    ):
        intent = "refactor"

    elif any(
        word in query
        for word in [
            "create",
            "generate",
            "build",
        ]
    ):
        intent = "create"

    elif any(
        word in query
        for word in [
            "explain",
            "analyze",
            "describe",
        ]
    ):
        intent = "explain"

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

    repository_analysis_required = any(
        keyword in query
        for keyword in [
            "repository",
            "architecture",
            "deployment strategy",
            "microservice",
            "service boundaries",
            "technical debt",
            "onboarding",
            "direction"
        ]
    )

    repository_history_required = any(
        keyword in query
        for keyword in [
            "history",
            "evolution",
            "evolved",
            "progress",
            "changes",
            "recent",
            "commits",
            "direction",
            "heading",
        ]
    )

    retrieval_query = (
        state["query"]
        if requires_retrieval
        else ""
    )

    print(
    "repository_analysis_required:",
    repository_analysis_required,
    )
    print(
    "repository_history_required:",
    repository_history_required,
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

        "repository_analysis_required": (
            repository_analysis_required
        ),

        "repository_history_required": (
            repository_history_required
        ),

        "intent": intent,

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