import { useState } from "react";

import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import DebugPanel from "./components/DebugPanel";

import { askQuestion } from "./api/ragApi";
import type { Message } from "./types";

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [debug, setDebug] = useState<any>(null);
  const [documents, setDocuments] = useState<string[]>([]);
  const [selectedSource, setSelectedSource] = useState("all");

  const handleSend = async (question: string, source?: string) => {
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: question,
      },
    ]);

    const response = await askQuestion(question, source);

    console.log(response);
    console.log("response.answer", response.answer);
    console.log("response.sources", response.sources);

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: response.answer,
        sources: response.sources,
      },
    ]);

    setDebug({
      ...response.debug,
      sources: response.sources,
      citations: response.citations,
    });
  };

  return (
    <div className="h-screen bg-gray-100 flex">
      <Sidebar documents={documents} setDocuments={setDocuments} />

      <div className="flex flex-col flex-1 min-h-0">
        <header className="bg-white border-b px-6 py-4">
          <h1 className="text-2xl font-bold">Enterprise RAG Assistant</h1>

          <p className="text-sm text-gray-500">
            Ask questions about your knowledge base
          </p>
        </header>

        <div className="flex-1 overflow-y-auto">
          <ChatWindow messages={messages} />
        </div>
        <ChatInput
          onSend={handleSend}
          loading={loading}
          documents={documents}
          selectedSource={selectedSource}
          setSelectedSource={setSelectedSource}
        />
        <DebugPanel debug={debug} />
      </div>
    </div>
  );
}

export default App;
