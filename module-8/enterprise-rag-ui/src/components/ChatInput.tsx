import { useState } from "react";

interface Props {
  onSend: (question: string, source?: string) => void;
  loading: boolean;
  documents: string[];
  selectedSource: string;
  setSelectedSource: (value: string) => void;
}

export default function ChatInput({
  onSend,
  loading,
  documents,
  selectedSource,
  setSelectedSource,
}: Props) {
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;

    onSend(text, selectedSource === "all" ? undefined : selectedSource);

    setText("");
  };

  return (
    <div className="border-t bg-white p-4 flex gap-2">
      <select
        value={selectedSource}
        onChange={(e) => setSelectedSource(e.target.value)}
        className="h-12 w-48 border rounded px-3 bg-white text-sm shrink-0"
      >
        <option value="all">All Documents</option>

        {documents.map((doc) => (
          <option key={doc} value={doc}>
            {doc}
          </option>
        ))}
      </select>

      <input
        className="flex-1 h-12 border rounded px-3"
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
        className="h-12 bg-blue-600 text-white px-6 rounded"
      >
        {loading ? "Thinking..." : "Send"}
      </button>
    </div>
  );
}
