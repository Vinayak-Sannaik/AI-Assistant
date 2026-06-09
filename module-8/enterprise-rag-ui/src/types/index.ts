export interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
}

export interface AskResponse {
  answer: string;
  sources: string[];
  debug?: {
    rewritten_query: string;
    retrieved_chunks: string[];
    reranked_chunks: string[];
  };
}