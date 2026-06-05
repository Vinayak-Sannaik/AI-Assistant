from dataclasses import dataclass, field


@dataclass
class Todo:
    id: int
    title: str
    description: str
    status: str = "pending"
    priority: str = "medium"
    tags: list[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""