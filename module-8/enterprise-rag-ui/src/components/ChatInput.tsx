import { useState } from "react";

interface Props {
  onSend: (message: string) => void;
  loading: boolean;
}

export default function ChatInput({ onSend, loading }: Props) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;

    onSend(text);

    setText("");
  };

  return (
    <div className="border-t bg-white p-4 flex gap-2">
      <input
        className="flex-1 border rounded p-3"
        placeholder="Ask anything..."
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSend();
          }
        }}
      />

      <button
        disabled={loading}
        onClick={handleSend}
        className="bg-blue-600 text-white px-6 rounded"
      >
        {loading ? "Thinking..." : "Send"}
      </button>
    </div>
  );
}
