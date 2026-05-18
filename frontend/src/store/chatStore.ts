import { create } from 'zustand';
import { createConversation, postMessage, streamAssistantResponse } from '../services/chatApi';
import type { ChatMessage, Conversation } from '../types/chat';

interface ChatState {
  conversation: Conversation | null;
  error: string | null;
  isStreaming: boolean;
  sendMessage: (content: string) => Promise<void>;
}

function createStreamingMessage(): ChatMessage {
  return {
    id: crypto.randomUUID(),
    role: 'assistant',
    content: '',
    createdAt: new Date().toISOString(),
    isStreaming: true,
  };
}

export const useChatStore = create<ChatState>((set, get) => ({
  conversation: null,
  error: null,
  isStreaming: false,
  async sendMessage(content) {
    const trimmed = content.trim();
    if (!trimmed || get().isStreaming) return;

    set({ error: null, isStreaming: true });

    try {
      let conversation = get().conversation;

      if (!conversation) {
        conversation = await createConversation(trimmed);
      } else {
        const userMessage = await postMessage(conversation.id, trimmed);
        conversation = {
          ...conversation,
          messages: [...conversation.messages, userMessage],
        };
      }

      const streamingMessage = createStreamingMessage();
      set({
        conversation: {
          ...conversation,
          messages: [...conversation.messages, streamingMessage],
        },
      });

      const source = streamAssistantResponse(conversation.id);

      source.addEventListener('token', (event) => {
        const token = JSON.parse((event as MessageEvent<string>).data) as string;
        set((state) => {
          if (!state.conversation) return state;
          return {
            conversation: {
              ...state.conversation,
              messages: state.conversation.messages.map((message) =>
                message.id === streamingMessage.id
                  ? { ...message, content: message.content + token }
                  : message,
              ),
            },
          };
        });
      });

      source.addEventListener('done', (event) => {
        const savedMessage = JSON.parse((event as MessageEvent<string>).data) as ChatMessage;
        source.close();
        set((state) => {
          if (!state.conversation) return { isStreaming: false };
          return {
            isStreaming: false,
            conversation: {
              ...state.conversation,
              messages: state.conversation.messages.map((message) =>
                message.id === streamingMessage.id ? savedMessage : message,
              ),
            },
          };
        });
      });

      source.onerror = () => {
        source.close();
        set({ error: 'The assistant stream disconnected. Try sending the message again.', isStreaming: false });
      };
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : 'Unable to send the message.',
        isStreaming: false,
      });
    }
  },
}));
