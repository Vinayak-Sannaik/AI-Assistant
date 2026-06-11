export interface LLMProvider {
  generateAnswer(prompt: string): Promise<string>;
}
