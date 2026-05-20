from pydantic import BaseModel, Field


class EngineeringStep(BaseModel):
    name: str = Field(description="Short phase or reasoning step name.")
    detail: str = Field(description="Actionable engineering guidance for this step.")


class EngineeringAssistantResponse(BaseModel):
    summary: str = Field(description="Concise response summary.")
    intent: str = Field(description="Classified engineering intent.")
    assumptions: list[str] = Field(default_factory=list, description="Assumptions made while answering.")
    steps: list[EngineeringStep] = Field(default_factory=list, description="Recommended steps.")
    risks: list[str] = Field(default_factory=list, description="Important risks or tradeoffs.")
    next_action: str = Field(description="Suggested next action for the user or system.")
