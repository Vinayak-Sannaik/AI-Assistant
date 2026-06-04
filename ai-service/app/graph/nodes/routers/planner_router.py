from app.graph.state import AgenticRagState

def route_after_planner(
    state: AgenticRagState,
) -> str:

    if state.get(
    "repository_analysis_required",
    ):
        return "repository_analyzer"

    if state.get(
        "requires_retrieval",
    ):
        return "retriever"

    return "writer"