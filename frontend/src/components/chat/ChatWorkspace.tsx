import { useEffect, useRef } from 'react';
import { GitBranch, PanelsTopLeft } from 'lucide-react';
import { useChatStore } from '../../store/chatStore';
import { ChatComposer } from './ChatComposer';
import { ChatMessage } from './ChatMessage';

export function ChatWorkspace() {
  const { conversation, error, isStreaming, sendMessage } = useChatStore();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [conversation?.messages]);

  return (
    <main className="grid min-h-screen bg-paper text-ink lg:grid-cols-[280px_1fr]">
      <aside className="hidden border-r border-ink/10 bg-white/70 p-5 lg:block">
        <div className="mb-8 flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-md bg-moss text-white">
            <GitBranch size={20} />
          </div>
          <div>
            <h1 className="text-base font-semibold">AI Assistant</h1>
            <p className="text-xs text-ink/60">Software Engineering Assistant</p>
          </div>
        </div>
        <div className="space-y-3 text-sm">
          <div className="rounded-md border border-ink/10 bg-paper p-3">
            <div className="mb-1 flex items-center gap-2 font-medium">
              <PanelsTopLeft size={16} />
              Active workspace
            </div>
            <p className="text-ink/65">{conversation?.title ?? 'New engineering thread'}</p>
          </div>
        </div>
      </aside>

      <section className="flex min-h-screen flex-col">

        <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-6">
          <div className="mx-auto flex max-w-4xl flex-col gap-5">
            {conversation?.messages.length ? (
              conversation.messages.map((message) => <ChatMessage key={message.id} message={message} />)
            ) : (
              <div className="rounded-md border border-ink/10 bg-white p-6 shadow-soft">
                <p className="mb-3 text-lg font-semibold">Start with a software engineering question.</p>
                <p className="text-sm leading-6 text-ink/65">
                  Try “Design a migration strategy from monolith to microservices” to watch the Phase 1 stream.
                </p>
              </div>
            )}
            {error && <p className="rounded-md bg-coral/10 px-4 py-3 text-sm text-coral">{error}</p>}
          </div>
        </div>

        <ChatComposer disabled={isStreaming} onSend={sendMessage} />
      </section>
    </main>
  );
}
