import ReactMarkdown from 'react-markdown';
import { Bot, User } from 'lucide-react';
import type { ChatMessage as ChatMessageType } from '../../types/chat';

interface ChatMessageProps {
  message: ChatMessageType;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isAssistant = message.role === 'assistant';

  return (
    <article className={`flex gap-3 ${isAssistant ? 'items-start' : 'items-start justify-end'}`}>
      {isAssistant && (
        <div className="grid h-9 w-9 shrink-0 place-items-center rounded-md bg-moss text-white">
          <Bot size={18} />
        </div>
      )}
      <div
        className={`max-w-[78%] rounded-md px-4 py-3 text-sm leading-6 shadow-sm ${
          isAssistant ? 'bg-white text-ink' : 'bg-ink text-white'
        }`}
      >
        <ReactMarkdown
          components={{
            p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
            code: ({ children }) => <code className="rounded bg-black/10 px-1 py-0.5 text-[0.85em]">{children}</code>,
            ul: ({ children }) => <ul className="ml-5 list-disc">{children}</ul>,
            ol: ({ children }) => <ol className="ml-5 list-decimal">{children}</ol>,
          }}
        >
          {message.content || (message.isStreaming ? 'Thinking...' : '')}
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
