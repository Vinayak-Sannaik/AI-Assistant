import { Injectable } from '@nestjs/common';
import { GoogleGenAI } from '@google/genai';
import { LLMProvider } from './llm-provider.interface';

@Injectable()
export class GeminiProvider implements LLMProvider {
  private ai: GoogleGenAI;

  constructor() {
    const apiKey = process.env.GEMINI_API_KEY;

    if (!apiKey) {
      throw new Error('GEMINI_API_KEY not found');
    }

    this.ai = new GoogleGenAI({ apiKey });
  }

  async generateAnswer(prompt: string): Promise<string> {
    const response: any = await this.ai.models.generateContent({
      model: 'gemini-2.0-flash-lite',
      contents: prompt,
    });

    return response.text;
  }
}
