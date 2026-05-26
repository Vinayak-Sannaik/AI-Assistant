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
  h1: ({ children }) => (
    <h1 className="mb-4 text-3xl font-bold text-ink">
      {children}
    </h1>
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

  p: ({ children }) => (
    <p className="mb-3 leading-7">
      {children}
    </p>
  ),

  code: ({ children }) => (
    <code className="rounded bg-black/10 px-1 py-0.5 text-[0.85em]">
      {children}
    </code>
  ),

  ul: ({ children }) => (
    <ul className="mb-3 ml-5 list-disc space-y-1">
      {children}
    </ul>
  ),

  ol: ({ children }) => (
    <ol className="mb-3 ml-5 list-decimal space-y-1">
      {children}
    </ol>
  ),

  li: ({ children }) => (
    <li className="leading-7">
      {children}
    </li>
  ),
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
