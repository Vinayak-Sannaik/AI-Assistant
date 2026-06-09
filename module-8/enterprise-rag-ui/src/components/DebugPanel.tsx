interface Props {
  debug: any;
}

export default function DebugPanel({
  debug,
}: Props) {
  if (!debug) return null;

  return (
    <div className="bg-white border-t p-4">
      <h3 className="font-bold mb-3">
        Retrieval Debug
      </h3>

      <p>
        <strong>Rewritten Query:</strong>
      </p>

      <p className="mb-4">
        {debug.rewritten_query}
      </p>

      <p>
        <strong>Retrieved Chunks:</strong>
      </p>

      <ul className="mb-4">
        {debug.retrieved_chunks.map(
          (chunk: string, idx: number) => (
            <li key={idx}>• {chunk}</li>
          )
        )}
      </ul>

      <p>
        <strong>Reranked Chunks:</strong>
      </p>

      <ul>
        {debug.reranked_chunks.map(
          (chunk: string, idx: number) => (
            <li key={idx}>• {chunk}</li>
          )
        )}
      </ul>
    </div>
  );
}