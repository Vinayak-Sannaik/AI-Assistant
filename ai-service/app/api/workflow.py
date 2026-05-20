import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.chains.core_chat import format_engineering_response
from app.services.core_chat import build_ai_error_response, run_core_chat_workflow, stream_core_chat_response

router = APIRouter()


class WorkflowRequest(BaseModel):
    workflow_type: str = Field(alias="workflowType")
    query: str
    conversation_id: str = Field(alias="conversationId")

    model_config = {"populate_by_name": True}


@router.post("/execute-workflow/stream")
async def execute_workflow_stream(request: WorkflowRequest) -> StreamingResponse:
    async def event_stream():
        async for token in stream_core_chat_response(request.query):
            yield f"data: {json.dumps(token)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/execute-workflow")
async def execute_workflow(request: WorkflowRequest) -> dict[str, object]:
    status = "completed"
    try:
        structured_response = await run_core_chat_workflow(request.query)
    except Exception as error:
        status = "failed"
        structured_response = build_ai_error_response(error)
    response = format_engineering_response(structured_response)

    return {
        "status": status,
        "result": response,
        "structuredOutput": structured_response,
        "steps": structured_response["steps"],
        "toolsUsed": [],
        "conversationId": request.conversation_id,
        "workflowType": request.workflow_type,
    }
