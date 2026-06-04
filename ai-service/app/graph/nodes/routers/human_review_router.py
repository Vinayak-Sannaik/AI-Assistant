from app.graph.state import AgenticRagState

def route_after_human_review(
    state: AgenticRagState,
):
    return state.get(
        "intent",
        "explain",
    )