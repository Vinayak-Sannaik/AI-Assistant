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

class RagResponse(BaseModel):
    overview: str = Field(description="High-level overview of the system design.")
    architecture_role: str = Field(description="Role of the analyzed code in the overall architecture.")
    key_technical_points: list[str] = Field(default_factory=list, description="Key technical points about the code.")
    design_decisions: list[str] = Field(default_factory=list, description="Design decisions made in the code.")
    extensibility_notes: list[str] = Field(default_factory=list, description="Notes on the extensibility of the code.")
    sources: list[str] = Field(default_factory=list, description="Sources of the retrieved information.")