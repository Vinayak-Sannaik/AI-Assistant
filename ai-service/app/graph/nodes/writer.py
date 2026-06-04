from app.graph.state import AgenticRagState
from app.providers.llm import llm
from app.schemas.engineering_response import RagResponse
from app.chains.core_chat import format_rag_response

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

        repository_context = state.get(
            "repository_context",
        )

        print(
            "REPOSITORY CONTEXT IN WRITER NODE",
            repository_context,
        )

        if repository_context:

            structured_llm = (
                llm.with_structured_output(
                    RagResponse
                )
            )

            response = await (
                structured_llm.ainvoke(
                    f"""
                    You are a senior staff software engineer.

                    Analyze this repository.

                    Repository Context:

                    {repository_context}

                    Provide:

                    - project purpose
                    - technology stack
                    - architecture overview
                    - component responsibilities
                    - design observations
                    - improvement opportunities

                    Base your answer ONLY on
                    the repository context.

                    Only use evidence present in the repository context.
                    Do not assume databases, microservices, cloud providers, or external systems unless explicitly present.
                    """
                )
            )

            markdown = (
                format_rag_response(
                    response
                )
            )

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