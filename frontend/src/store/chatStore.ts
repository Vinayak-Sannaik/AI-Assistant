import { create } from "zustand";

import {
  createConversation,
  postMessage,
  streamAssistantResponse,
  streamResumeWorkflow,
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
  resumeWorkflow: (workflowId: string, messageId: string) => Promise<void>;
  rejectReview: (messageId: string) => void;
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

interface HumanReviewEvent {
  type: "human_review_required";
  workflow_id: string;
  reason: string;
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
      // Local flag to distinguish intentional workflow suspension from network errors
      let interruptedForReview = false;

      // WORKFLOW EVENTS
      source.addEventListener("workflow", (event) => {
        const parsed = JSON.parse(
          (event as MessageEvent<string>).data,
        ) as WorkflowEvent;

        // console.log("WORKFLOW EVENT", parsed);
      });

      // HUMAN REVIEW REQUIRED EVENT
      source.addEventListener("human_review_required", (event) => {
        const parsed = JSON.parse(
          (event as MessageEvent<string>).data,
        ) as HumanReviewEvent;
        // Mark that the stream was intentionally interrupted for human review
        interruptedForReview = true;

        // Stop global streaming indicator before closing the stream
        set({ isStreaming: false });

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

                      status: "waiting_human_review",
                      workflowId: parsed.workflow_id,
                      reviewReason: parsed.reason,
                    }
                  : message,
              ),
            },
          };
        });

        // Close the SSE connection now that we've recorded the paused state
        source.close();
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
      // Error handling for SSE - ignore errors if we intentionally interrupted for review
      source.onerror = () => {
        if (interruptedForReview) {
          // intentional suspension of workflow; do not treat as an error
          return;
        }

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
  async resumeWorkflow(workflowId, messageId) {
    if (!workflowId) return;

    set({
      error: null,
      isStreaming: true,
    });

    try {
      // Mark message as streaming and remove review UI metadata
      set((state) => {
        if (!state.conversation) return state;

        return {
          conversation: {
            ...state.conversation,

            messages: state.conversation.messages.map((m) =>
              m.id === messageId
                ? {
                    ...m,
                    status: "streaming",
                    isStreaming: true,
                    reviewReason: undefined,
                    workflowId: undefined,
                  }
                : m,
            ),
          },
        };
      });

      const conversation = get().conversation;
      if (!conversation) {
        set({ error: "No active conversation to resume.", isStreaming: false });
        return;
      }

      const source = streamResumeWorkflow(conversation.id, workflowId, true);

      source.addEventListener("token", (event) => {
        const parsed = JSON.parse((event as MessageEvent<string>).data) as TokenEvent;

        if (parsed.type !== "token") return;

        set((state) => {
          if (!state.conversation) return state;

          return {
            conversation: {
              ...state.conversation,

              messages: state.conversation.messages.map((m) =>
                m.id === messageId ? { ...m, content: m.content + parsed.content } : m,
              ),
            },
          };
        });
      });

      source.addEventListener("done", () => {
        source.close();

        set((state) => {
          if (!state.conversation) return state;

          return {
            conversation: {
              ...state.conversation,
              messages: state.conversation.messages.map((m) =>
                m.id === messageId ? { ...m, isStreaming: false, status: "completed" } : m,
              ),
            },
            isStreaming: false,
          };
        });
      });

      source.onerror = () => {
        source.close();

        set({
          error: "The assistant stream disconnected. Try approving again.",
          isStreaming: false,
        });
      };
    } catch (error) {
      console.error(error);

      set({
        error: error instanceof Error ? error.message : "Unable to resume the workflow.",
        isStreaming: false,
      });
    }
  },
  rejectReview(messageId) {
    // Local-only rejection: mark the assistant message as failed and clear streaming state
    set({ error: null, isStreaming: false });

    set((state) => {
      if (!state.conversation) return state;

      return {
        conversation: {
          ...state.conversation,

          messages: state.conversation.messages.map((m) =>
            m.id === messageId
              ? {
                  ...m,
                  status: "failed",
                  isStreaming: false,
                  content: "Request rejected by reviewer.",
                  workflowId: undefined,
                  reviewReason: undefined,
                }
              : m,
          ),
        },
      };
    });
  },
}));
