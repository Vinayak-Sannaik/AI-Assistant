from app.graph.state import AgenticRagState
from langgraph.types import interrupt


HIGH_RISK_TERMS = [
    "delete",
    "migration",
    "production",
    "deploy",
    "refactor",
    "database",
]

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