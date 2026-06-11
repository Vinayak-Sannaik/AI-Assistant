from typing import TypedDict


class AgentState(TypedDict):
    message: str
    route: str
    email: dict | None
    response: str