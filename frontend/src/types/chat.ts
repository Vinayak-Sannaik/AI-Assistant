export type ChatRole = 'user' | 'assistant';

export interface ChatMessage {
  id: string;
  role: ChatRole;
  content: string;
  createdAt: string;
  isStreaming?: boolean;
  
  status?:
  | "streaming"
  | "waiting_human_review"
  | "completed"
  | "failed";

  workflowId?: string;

  reviewReason?: string;
}

export interface Conversation {
  id: string;
  title: string;
  createdAt: string;
  messages: ChatMessage[];
}
