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

from uuid import uuid4
from langgraph.types import Command

from app.graph.graph import agentic_rag_graph
async def run_agentic_rag_graph(
    query: str,
):
    workflow_id = str(uuid4())
    
    return await (
        agentic_rag_graph.ainvoke(
            {
                "query": query,
                "workflow_id": workflow_id,
                "status": "running",
                "workflow_events": [],
            },
            config={
                "configurable": {
                    "thread_id": workflow_id,
                }
            },
        )
    )

async def resume_agentic_rag_graph(
    workflow_id: str,
    human_approved: bool,
):

    return await (
        agentic_rag_graph.ainvoke(
            Command(
                resume=human_approved
            ),

            config={
                "configurable": {
                    "thread_id": workflow_id,
                }
            },
        )
    )

async def stream_resume_agentic_rag_graph(
    workflow_id: str,
    human_approved: bool,
):

    async for chunk in (
        agentic_rag_graph.astream(
            Command(
                resume=human_approved
            ),

            config={
                "configurable": {
                    "thread_id": workflow_id,
                }
            },

            stream_mode="updates",
        )
    ):

        #
        # WRITER OUTPUT
        #

        if "writer" in chunk:

            writer_state = chunk[
                "writer"
            ]

            markdown = writer_state.get(
                "markdown",
                "",
            )

            for line in markdown.splitlines(
                keepends=True,
            ):

                yield {
                    "type": "token",
                    "content": line,
                }

async def stream_agentic_rag_graph(
    query: str,
):

    workflow_id = str(uuid4())

    async for chunk in (
        agentic_rag_graph.astream(
            {
                "query": query,
                "workflow_id": workflow_id,
                "status": "running",
                "workflow_events": [],
            },

            config={
                "configurable": {
                    "thread_id": workflow_id,
                }
            },

            stream_mode="updates",
        )
    ):

        #
        # INTERRUPT EVENT
        #

        if "__interrupt__" in chunk:

            interrupt_data = (
                chunk["__interrupt__"][0]
                .value
            )

            yield {
                "type": (
                    "human_review_required"
                ),

                "reason": interrupt_data.get(
                    "reason",
                    "",
                ),

                "workflow_id": workflow_id,
            }

            return

        #
        # WRITER OUTPUT
        #

        if "writer" in chunk:

            writer_state = chunk[
                "writer"
            ]

            markdown = writer_state.get(
                "markdown",
                "",
            )

            for line in markdown.splitlines(
                keepends=True,
            ):

                yield {
                    "type": "token",
                    "content": line,
                }