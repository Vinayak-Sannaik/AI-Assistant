from src.memory.conversation_memory import ConversationMemory

memory = ConversationMemory()

memory.add_user_message(
    "What is ChromaDB?"
)

memory.add_assistant_message(
    "ChromaDB is a vector database."
)

print(memory.get_history())