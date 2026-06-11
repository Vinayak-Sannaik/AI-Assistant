export function aiAssistant(context: string, question: string): string {
  return `
      You are a strict AI assistant.

      Answer ONLY using the context below.
      Do NOT add any external knowledge.
      If the answer is not clearly present, say "I don't know".

      Context:
      ${context}

      Question:
      ${question}

      Answer:
`;
}
