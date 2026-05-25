import { create } from "zustand";

import {
  createConversation,
  postMessage,
  streamAssistantResponse,
} from "../services/chatApi";

import type { ChatMessage, Conversation } from "../types/chat";

// WORKFLOW EVENT
interface WorkflowEvent {
  type: "workflow";
  node: string;
  status: string;
}
// TOKEN EVENT
interface TokenEvent {
  type: "token";
  content: string;
}

// STORE STATE
interface ChatState {
  conversation: Conversation | null;
  error: string | null;
  isStreaming: boolean;
  sendMessage: (content: string) => Promise<void>;
}

// CREATE STREAMING MESSAGE
function createStreamingMessage(): ChatMessage {
  return {
    id: crypto.randomUUID(),
    role: 'assistant',
    content: '',
    createdAt: new Date().toISOString(),
    isStreaming: true,
  };
}

// STORE
export const useChatStore = create<ChatState>((set, get) => ({
  conversation: null,
  error: null,
  isStreaming: false,
  // SEND MESSAGE
  async sendMessage(content) {
    const trimmed = content.trim();
    if (!trimmed || get().isStreaming) {
      return;
    }

    set({
      error: null,
      isStreaming: true,
    });

    try {
      let conversation = get().conversation;
      // CREATE CONVERSATION
      if (!conversation) {
        conversation = await createConversation(trimmed);
      } else {
        // ADD USER MESSAGE
        const userMessage = await postMessage(conversation.id, trimmed);
        conversation = {
          ...conversation,
          messages: [...conversation.messages, userMessage],
        };
      }
      // STREAMING ASSISTANT MESSAGE
      const streamingMessage = createStreamingMessage();
      set({
        conversation: {
          ...conversation,
          messages: [...conversation.messages, streamingMessage],
        },
      });

      // OPEN SSE STREAM
      const source = streamAssistantResponse(conversation.id);

      // WORKFLOW EVENTS
      source.addEventListener("workflow", (event) => {
        const parsed = JSON.parse(
          (event as MessageEvent<string>).data,
        ) as WorkflowEvent;

        // console.log("WORKFLOW EVENT", parsed);
      });
      // TOKEN EVENTS
      source.addEventListener("token", (event) => {
        const parsed = JSON.parse(
          (event as MessageEvent<string>).data,
        ) as TokenEvent;
        // Ignore invalid token
        if (parsed.type !== "token") {
          return;
        }
        // APPEND TOKEN TO STREAMING MESSAGE
        set((state) => {
          if (!state.conversation) {
            return state;
          }

          return {
            conversation: {
              ...state.conversation,

              messages: state.conversation.messages.map((message) =>
                message.id === streamingMessage.id
                  ? {
                      ...message,

                      content: message.content + parsed.content,
                    }
                  : message,
              ),
            },
          };
        });
      });

      // DONE EVENT
      source.addEventListener("done", () => {
        // console.log("DONE EVENT");

        source.close();

        set({
          isStreaming: false,
        });
      });
      // Error handling for SSE
      source.onerror = () => {
        // console.error("SSE ERROR");

        source.close();

        set({
          error:
            "The assistant stream disconnected. Try sending the message again.",

          isStreaming: false,
        });
      };
    } catch (error) {
      console.error(error);

      set({
        error:
          error instanceof Error
            ? error.message
            : "Unable to send the message.",

        isStreaming: false,
      });
    }
  },
}));
