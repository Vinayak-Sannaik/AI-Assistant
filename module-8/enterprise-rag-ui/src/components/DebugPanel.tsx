interface Props {
  debug: any;
}

import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

export default function DebugPanel({ debug }: Props) {
  const [expanded, setExpanded] = useState(false);

  if (!debug) return null;

  debug.generated_queries.map((query: string) => console.log(query));

  return (
    <div className="bg-white border-t p-4">
      <button
        onClick={() => setExpanded(!expanded)}
        className="flex items-center gap-2 font-bold"
      >
        {expanded ? <ChevronDown size={18} /> : <ChevronRight size={18} />}
        Retrieval Debug
      </button>

      {expanded && (
        <>
          <div className="mb-4">
            <p className="font-semibold">Retrieval Query</p>
            <p className="text-sm text-gray-700">{debug.retrieval_query}</p>
          </div>

          <div className="mb-4">
            <p className="font-semibold">Generated Queries</p>

            <ul className="text-sm text-gray-700 list-disc ml-5">
              {debug.generated_queries?.map(
                (generatedQuery: string, index: number) => (
                  <li key={index}>{generatedQuery}</li>
                ),
              )}
            </ul>
          </div>

          <div>
            <p className="font-semibold">Chunks Used</p>
            <p className="text-sm text-gray-700">{debug.chunks_used}</p>
          </div>
          <div className="mt-4">
            <p className="font-semibold">Sources</p>

            <ul className="text-sm">
              {debug.sources?.map((source: string) => (
                <li key={source}>• {source}</li>
              ))}
            </ul>
          </div>
          <div className="mt-4">
            <p className="font-semibold">Citations</p>

            <ul className="text-sm">
              {debug.citations?.map((citation: any, index: number) => (
                <li key={index}>
                  {citation.source}
                  {" | "}
                  chunk {citation.chunk_id}
                  {" | "}
                  score {citation.score.toFixed(2)}
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
}
