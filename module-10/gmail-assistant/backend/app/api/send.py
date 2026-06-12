from fastapi import APIRouter

from app.schemas.email import SendEmailRequest

router = APIRouter()


@router.post("/send")
async def send_email(request: SendEmailRequest):

    return {
        "status": "sent",
        "draft_id": request.draft_id
    }