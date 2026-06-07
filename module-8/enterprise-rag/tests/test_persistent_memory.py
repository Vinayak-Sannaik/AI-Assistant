from src.memory.persistent_memory import (
    PersistentMemory
)

memory = PersistentMemory()

memory.set(
    "favorite_database",
    "ChromaDB"
)

print(
    memory.get(
        "favorite_database"
    )
)