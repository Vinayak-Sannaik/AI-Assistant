from typing import TypedDict


class EmailDraft(TypedDict):
    to: str
    subject: str
    body: str


class AgentState(TypedDict):
    message: str
    route: str
    email: dict | None
    draft: EmailDraft | None
    response: str