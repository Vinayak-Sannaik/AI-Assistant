import type { AskResponse } from "../types";

export const askQuestion = async (
  question: string
): Promise<AskResponse> => {
  console.log("Question:", question);

  await new Promise((resolve) => setTimeout(resolve, 1000));

  return {
    answer:
      "ChromaDB is an open-source vector database used for storing embeddings and performing semantic search.",

    sources: ["chromadb.md"],

    debug: {
      rewritten_query:
        "Explain ChromaDB vector database architecture",

      retrieved_chunks: [
        "ChromaDB is a vector database...",
        "Embeddings are numerical representations..."
      ],

      reranked_chunks: [
        "Score 10.2 - ChromaDB is a vector database...",
        "Score 8.9 - Embeddings are numerical..."
      ]
    }
  };
};


export const uploadDocument = async (
  file: File
) => {
  console.log("Uploading:", file.name);

  await new Promise((resolve) =>
    setTimeout(resolve, 1000)
  );

  return {
    success: true,
  };
};

export const getKnowledgeBase =
  async () => {
    return {
      documents: [
        "enterprise-rag.pdf",
        "chromadb.md",
      ],
      total_documents: 2,
      total_chunks: 127,
    };
  };