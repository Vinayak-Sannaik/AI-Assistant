import type { Message } from "../types";

interface Props {
  messages: Message[];
}

export default function ChatWindow({ messages }: Props) {
  console.log("messages", messages);
  return (
    <div className="h-full overflow-y-auto p-6 flex flex-col gap-4">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`mb-4 flex ${
            msg.role === "user" ? "justify-end" : "justify-start"
          }`}
        >
          <div className="max-w-[700px]">
            <div className="text-sm text-gray-500 mb-1">
              {msg.role === "user" ? "You" : "Assistant"}
            </div>

            <div
              className={`p-4 rounded-xl ${
                msg.role === "user" ? "bg-white text-black" : "bg-white"
              }`}
            >
              {msg.content}

              {msg.role === "assistant" &&
                msg.sources &&
                msg.sources.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <div className="text-xs font-semibold text-gray-500 mb-1">
                      Sources
                    </div>

                    {msg.sources.map((source, index) => (
                      <div
                        key={`${source}-${index}`}
                        className="text-xs text-gray-600"
                      >
                        • {source}
                      </div>
                    ))}
                  </div>
                )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
