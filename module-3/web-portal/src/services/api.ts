export async function askQuestion(query: string) {
  const res = await fetch('http://localhost:3001/chunks/ask', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });

  if (!res.ok) {
    throw new Error('API failed');
  }

  return res.json();
}