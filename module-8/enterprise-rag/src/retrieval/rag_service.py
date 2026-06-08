# question
#    ↓
# rewrite
#    ↓
# retrieval_pipeline.retrieve()
#    ↓
# context
#    ↓
# llm.invoke()


from src.llm.gemini_service import GeminiService
from src.memory.conversation_memory import ConversationMemory
from src.retrieval.query_rewriter import QueryRewriter
from src.retrieval.retrieval_pipeline import RetrievalPipeline


class RAGService:

    def __init__(self):
        self.llm = GeminiService()
        self.memory = ConversationMemory()
        self.query_rewriter = QueryRewriter()
        self.retrieval_pipeline = RetrievalPipeline()

    def ask(self, question: str):

        history = self.memory.get_history()

        standalone_question = self.query_rewriter.rewrite(
            question=question,
            conversation_history=history,
        )


        context_chunks = self.retrieval_pipeline.retrieve(
            standalone_question
        )

        context = "\n\n".join(
            context_chunks
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