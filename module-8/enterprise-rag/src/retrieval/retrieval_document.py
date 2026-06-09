from dataclasses import dataclass

# frozen=True makes it immutable and hashable.
@dataclass(frozen=True)
class RetrievalDocument:
    content: str
    source: str
    chunk_id: int | None = None