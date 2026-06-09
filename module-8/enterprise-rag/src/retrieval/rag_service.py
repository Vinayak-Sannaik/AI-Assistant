# VectorStore
#     ↓
# RetrievalDocument
#     ↓
# BM25
#     ↓
# Hybrid
#     ↓
# RRF
#     ↓
# Reranker
#     ↓
# RetrievalPipeline
#     ↓
# RAGService
#     ↓
# FastAPI
#     ↓
# UI


from src.llm.llm_service import LLMService
from src.memory.conversation_memory import ConversationMemory
from src.retrieval.query_rewriter import QueryRewriter
from src.retrieval.retrieval_pipeline import RetrievalPipeline


class RAGService:

    def __init__(self):
        self.llm = LLMService()
        self.memory = ConversationMemory()
        self.query_rewriter = QueryRewriter()
        self.retrieval_pipeline = RetrievalPipeline()

    def ask(self, question: str, source: str | None = None,):

        history = self.memory.get_history()

        if (
            source
            and self.is_document_query(
                question
            )
        ):
            print("question---------->", question)
            return self.summarize_document(
                source
            )

        if source:
            standalone_question = question

        elif not history:
            standalone_question = question

        else:
            standalone_question = self.query_rewriter.rewrite(
                question=question,
                conversation_history=history,
            )

        retrieval_result = self.retrieval_pipeline.retrieve(
            standalone_question,
            source=source
        )

        retrieved_documents = retrieval_result[
            "retrieved_documents"
        ]

        if not retrieved_documents:
            return {
                "answer": "I don't know.",
                "sources": [],
                "citations": [],
                "debug": {
                    "retrieval_query": standalone_question,
                    "chunks_used": 0,
                },
            }

        context_chunks = [
            doc["content"]
            for doc in retrieved_documents
        ]

        context = "\n\n".join(
            context_chunks
        )

        print("\nQuestion:")
        print(question)

        print("\nStandalone Question:")
        print(standalone_question)

        # print("\nRetrieved Documents:")

        # for chunk, source, score in zip(
        #     context_chunks,
        #     sources,
        #     scores,
        # ):
        #     print("\n---")
        #     print("Source:", source)
        #     print("Score:", score)
        #     print(chunk)

        # print("\nContext:")
        # print(context)

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

        citations = [
            {
                "source": doc["source"],
                "chunk_id": doc["chunk_id"],
                "score": doc["score"],
            }
            for doc in retrieved_documents
        ]

        debug = {
            "retrieval_query": standalone_question,
            "chunks_used": len(
                retrieved_documents
            ),
            "mode": "retrieval"
        }

        return {
            "answer": answer,
            "sources": list(
                dict.fromkeys(
                    [
                        doc["source"]
                        for doc in retrieved_documents
                    ]
                )
            ),
            "citations": citations,
            "debug": debug,
        }
    
    def is_document_query(
        self,
        question: str,
    ):
        question = question.lower()

        keywords = [
            "summary",
            "summarize",
            "overview",
            "content",
            "document",
            ".txt",
            ".pdf"
        ]

        return any(
            keyword in question
            for keyword in keywords
        )
    
    def summarize_document(
        self,
        source: str,
    ):
        chunks = (
            self.retrieval_pipeline.get_document_chunks(
                source
            )
        )

        context = "\n\n".join(
            chunks
        )

        prompt = f"""
        Summarize the following document.

        Document:
        {context}
        """

        answer = self.llm.invoke(
            prompt
        )

        return {
            "answer": answer,
            "sources": [source],
            "citations": [],
            "debug": {
                "mode": "document_summary",
                "chunks_used": len(chunks),
                "mode": "document_summary",
            },
        }