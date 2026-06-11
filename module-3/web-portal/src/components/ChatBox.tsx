import { useState } from 'react';
import { askQuestion } from '../services/api';

export default function ChatBox() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [chunks, setChunks] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!query) return;

    setLoading(true);
    try {
      const data = await askQuestion(query);
      setAnswer(data.answer);
      setChunks(data.chunks);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>RAG Chat</h2>

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask something..."
        style={{ width: '60%', padding: 10 }}
      />

      <button disabled = { loading || !query} onClick={handleAsk} style={{ marginLeft: 10 }}>
        Ask
      </button>

      {loading && <p>Loading...</p>}

      {answer && (
        <div style={{ marginTop: 20 }}>
          <h3>Answer</h3>
          <p>{answer}</p>
        </div>
      )}

      {chunks.length > 0 && (
        <div style={{ marginTop: 20 }}>
          <h4>Retrieved Chunks</h4>
          {chunks.map((c, i) => (
            <div key={i} style={{ marginBottom: 10 }}>
              <li>
                <ul>{c.content}</ul>
              </li>
              {/* <small>Distance: {c.distance}</small> */}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}