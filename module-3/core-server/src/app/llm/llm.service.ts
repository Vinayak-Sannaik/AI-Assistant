import { Injectable } from '@nestjs/common';
import { GeminiProvider } from './providers/gemini.provider';
import { GroqProvider } from './providers/groq.provider';

@Injectable()
export class LlmService {
  constructor(
    private readonly geminiProvider: GeminiProvider,
    private readonly groqProvider: GroqProvider,
  ) {}

  async generateAnswer(prompt: string): Promise<string> {
    const provider = process.env.LLM_PROVIDER || 'gemini';

    switch (provider) {
      case 'groq':
        return this.groqProvider.generateAnswer(prompt);

      case 'gemini':
      default:
        return this.geminiProvider.generateAnswer(prompt);
    }
  }
}
