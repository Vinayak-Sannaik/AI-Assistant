import { FormEvent, useState } from 'react';
import { SendHorizontal } from 'lucide-react';

interface ChatComposerProps {
  disabled: boolean;
  onSend: (message: string) => Promise<void>;
}

export function ChatComposer({ disabled, onSend }: ChatComposerProps) {
  const [message, setMessage] = useState('');

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const value = message.trim();
    if (!value) return;
    setMessage('');
    await onSend(value);
  }

  return (
    <form className="sticky bottom-0 z-10 flex gap-3 border-t border-ink/10 bg-paper/95 p-4 backdrop-blur">
      <textarea
        className="min-h-12 flex-1 resize-none rounded-md border border-ink/15 bg-white px-4 py-3 text-sm leading-6 text-ink outline-none transition focus:border-moss focus:ring-2 focus:ring-moss/20"
        placeholder="Ask for an architecture review, repository analysis, or engineering plan..."
        value={message}
        disabled={disabled}
        rows={2}
        onChange={(event) => setMessage(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            void handleSubmit(event);
          }
        }}
      />
      <button
        className="grid h-12 w-12 shrink-0 place-items-center rounded-md bg-coral text-white transition hover:bg-coral/90 disabled:cursor-not-allowed disabled:bg-sage"
        type="submit"
        disabled={disabled || !message.trim()}
        title="Send message"
        aria-label="Send message"
      >
        <SendHorizontal size={20} />
      </button>
    </form>
  );
}
