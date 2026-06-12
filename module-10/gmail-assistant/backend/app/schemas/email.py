from pydantic import BaseModel


class SendEmailRequest(BaseModel):
    draft_id: str