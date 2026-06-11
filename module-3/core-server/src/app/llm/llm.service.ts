import { Injectable } from '@nestjs/common';
import { GoogleGenAI } from '@google/genai';

@Injectable()
export class LlmService {
  private ai: GoogleGenAI;

  constructor() {
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) {
      throw new Error('GEMINI_API_KEY environment variable is not set');
    }

    this.ai = new GoogleGenAI({ apiKey });
  }

  async listModels() {
    const models = await this.ai.models.list();
    console.log('Available models:', models);
  }

  async generateAnswer(prompt: string): Promise<string> {
    const response: any = await this.ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
    });

    return response.text;
  }
}
