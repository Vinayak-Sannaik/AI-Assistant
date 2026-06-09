import { useState } from "react";

import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
// import DebugPanel from "./components/DebugPanel";

import { askQuestion } from "./api/ragApi";
import type { Message } from "./types";

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [debug, setDebug] = useState<any>(null);

  const handleSend = async (question: string) => {
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: question,
      },
    ]);

    const response = await askQuestion(question);

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: response.answer,
        sources: response.sources
      },
    ]);

    setDebug(response.debug);
  };

  return (
    <div className="h-screen bg-gray-100 flex">
      <Sidebar />

      <div className="flex flex-col flex-1">
        <header className="bg-white border-b px-6 py-4">
          <h1 className="text-2xl font-bold">Enterprise RAG Assistant</h1>

          <p className="text-sm text-gray-500">
            Ask questions about your knowledge base
          </p>
        </header>

        <div className="flex-1 overflow-hidden">
          <ChatWindow messages={messages} />
        </div>

        <ChatInput onSend={handleSend} loading={loading} />

        {/* <DebugPanel debug={debug} /> */}
      </div>
    </div>
  );
}

export default App;
