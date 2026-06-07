from src.retrieval.vector_store import VectorStore
from src.llm.gemini_service import GeminiService
from src.memory.conversation_memory import ConversationMemory
from src.retrieval.query_rewriter import QueryRewriter


class RAGService:

    def __init__(self):
        self.vector_store = VectorStore()
        self.llm = GeminiService()
        self.memory = ConversationMemory()
        self.query_rewriter = QueryRewriter()

    def ask(self, question: str):

        history = self.memory.get_history()

        standalone_question = self.query_rewriter.rewrite(
            question=question,
            conversation_history=history,
        )
        # print("\nRewritten Query:")
        # print(standalone_question)
        results = self.vector_store.search(
            standalone_question,
            top_k=3,
        )

        # Directly using original q some time not retrievable results, so using rewritten query for retrieval.
        # results = self.vector_store.search(
        #     question,
        #     top_k=3,
        # )

        context = "\n\n".join(
            results["documents"][0]
        )

        prompt = f"""
            You are a helpful assistant.

            Conversation History:
            {history}

            Context:
            {context}

            Question:
            {question}

            Answer ONLY from context and conversation history.
            If answer is unavailable, say "I don't know".
            """

        answer = self.llm.invoke(prompt)

        self.memory.add_user_message(question)
        self.memory.add_assistant_message(answer)

        return answer