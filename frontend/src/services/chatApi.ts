import axios from 'axios';
import type { ChatMessage, Conversation } from '../types/chat';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:3000';

export async function createConversation(message: string): Promise<Conversation> {
  const response = await axios.post<Conversation>(`${API_BASE_URL}/chat/conversations`, { message });
  return response.data;
}

export async function postMessage(conversationId: string, content: string): Promise<ChatMessage> {
  const response = await axios.post<ChatMessage>(`${API_BASE_URL}/chat/conversations/${conversationId}/messages`, {
    content,
  });
  return response.data;
}

export function streamAssistantResponse(conversationId: string): EventSource {
  return new EventSource(`${API_BASE_URL}/chat/conversations/${conversationId}/stream`);
}

export function streamResumeWorkflow(conversationId: string, workflowId: string, humanApproved = true): EventSource {
  const params = new URLSearchParams();
  params.set("workflowId", workflowId);
  params.set("humanApproved", humanApproved ? "true" : "false");

  return new EventSource(
    `${API_BASE_URL}/chat/conversations/${encodeURIComponent(conversationId)}/resume-stream?${params.toString()}`,
  );
}
