export function chunkText(text: string, size = 150, overlap = 30): string[] {
  const sentences = text.split('. ');
  const chunks: string[] = [];

  let currentChunk = '';

  for (const sentence of sentences) {
    if ((currentChunk + sentence).length < size) {
      currentChunk += sentence + '. ';
    } else {
      chunks.push(currentChunk.trim());
      currentChunk = sentence + '. ';
    }
  }

  if (currentChunk) {
    chunks.push(currentChunk.trim());
  }

  return chunks;
}
