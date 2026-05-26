import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.chains.core_chat import format_engineering_response
from app.services.core_chat import run_core_chat_workflow, stream_core_chat_response
from app.workflows.core_chat import stream_core_chat_graph
from app.services.workflow_router import WORKFLOW_RUNNERS
from app.services.workflow_router import WORKFLOW_STREAMS

router = APIRouter()


class WorkflowRequest(BaseModel):
    workflow_type: str = Field(alias="workflowType")
    query: str
    conversation_id: str = Field(alias="conversationId")

    model_config = {"populate_by_name": True}


@router.post("/execute-workflow/stream")
async def execute_workflow_stream(
    request: WorkflowRequest,
) -> StreamingResponse:

    async def event_stream():

        stream_runner = (
            WORKFLOW_STREAMS[
                request.workflow_type
            ]
        )
        async for event in stream_runner(
            request.query
        ):

            event_type = event.get("type", "message")

            yield (
                f"event: {event_type}\n"
                f"data: {json.dumps(event)}\n\n"
            )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )


@router.post("/execute-workflow")
async def execute_workflow(request: WorkflowRequest) -> dict[str, object]:
    workflow_runner = WORKFLOW_RUNNERS.get(
        request.workflow_type,
    )
    structured_response = await workflow_runner(request.query)
    response = format_engineering_response(structured_response)
    workflow_run = structured_response.get("workflowRun", {})

    return {
        "status": workflow_run.get("status", "completed"),
        "result": response,
        "structuredOutput": structured_response,
        "steps": structured_response["steps"],
        "toolsUsed": [],
        "conversationId": request.conversation_id,
        "workflowType": request.workflow_type,
    }
