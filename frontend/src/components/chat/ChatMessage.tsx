import ReactMarkdown from "react-markdown";
import { Bot, User } from "lucide-react";
import type { ChatMessage as ChatMessageType } from "../../types/chat";
import { useChatStore } from "../../store/chatStore";

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isAssistant = message.role === "assistant";
  const resumeWorkflow = useChatStore((s) => s.resumeWorkflow);
  const rejectReview = useChatStore((s) => s.rejectReview);

  return (
    <article
      className={`flex gap-3 ${isAssistant ? "items-start" : "items-start justify-end"}`}
    >
      {isAssistant && (
        <div className="grid h-9 w-9 shrink-0 place-items-center rounded-md bg-moss text-white">
          <Bot size={18} />
        </div>
      )}
      <div
        className={`max-w-[78%] rounded-md px-4 py-3 text-sm leading-6 shadow-sm ${
          isAssistant ? "bg-white text-ink" : "bg-ink text-white"
        }`}
      >
        {message.status === "waiting_human_review" && (
          <div className="mb-3 rounded-md border border-coral/20 bg-coral/10 p-3 text-sm text-coral">
            <p className="mb-2 flex items-center gap-2">
              <span className="text-coral">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </span>
              ⚠ Approval required
            </p>
            <p className="mb-3">
              Reason: <span className="font-medium">{message.reviewReason}</span>
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => message.workflowId && resumeWorkflow(message.workflowId, message.id)}
                disabled={!message.workflowId}
                className="rounded-md bg-coral text-white hover:bg-coral/80 focus:outline-none focus:ring-2 focus:ring-coral/50 disabled:opacity-50 min-w-[120px] px-4 py-2"
              >
                Approve
              </button>
              <button
                onClick={() => rejectReview(message.id)}
                className="rounded-md bg-ink text-white hover:bg-ink/80 focus:outline-none focus:ring-2 focus:ring-ink/50 min-w-[120px] px-4 py-2"
              >
                Reject
              </button>
            </div>
          </div>
        )}
        <ReactMarkdown
          components={{
            h1: ({ children }) => (
              <h1 className="mb-4 text-3xl font-bold text-ink">{children}</h1>
            ),

            h2: ({ children }) => (
              <h2 className="mb-3 mt-6 text-2xl font-bold text-ink">
                {children}
              </h2>
            ),

            h3: ({ children }) => (
              <h3 className="mb-2 mt-5 text-xl font-semibold text-ink">
                {children}
              </h3>
            ),

            p: ({ children }) => <p className="mb-3 leading-7">{children}</p>,

            code: ({ children }) => (
              <code className="rounded bg-black/10 px-1 py-0.5 text-[0.85em]">
                {children}
              </code>
            ),

            ul: ({ children }) => (
              <ul className="mb-3 ml-5 list-disc space-y-1">{children}</ul>
            ),

            ol: ({ children }) => (
              <ol className="mb-3 ml-5 list-decimal space-y-1">{children}</ol>
            ),

            li: ({ children }) => <li className="leading-7">{children}</li>,
          }}
        >
          {message.content || (message.isStreaming ? "Thinking..." : "")}
        </ReactMarkdown>
      </div>
      {!isAssistant && (
        <div className="grid h-9 w-9 shrink-0 place-items-center rounded-md bg-coral text-white">
          <User size={18} />
        </div>
      )}
    </article>
  );
}
