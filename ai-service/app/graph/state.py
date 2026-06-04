from typing import Any, TypedDict


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

    intent: str

    # REPOSITORY ANALYSIS
    repository_analysis_required: bool
    repository_context: str

    # ERROR
    error: str