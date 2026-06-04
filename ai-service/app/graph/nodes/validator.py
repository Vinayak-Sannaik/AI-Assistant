from app.graph.state import AgenticRagState

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
