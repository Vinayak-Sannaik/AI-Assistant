import { Injectable } from '@nestjs/common';
import Groq from 'groq-sdk';
import { LLMProvider } from './llm-provider.interface';

@Injectable()
export class GroqProvider implements LLMProvider {
  private groq: Groq;

  constructor() {
    const apiKey = process.env.GROQ_API_KEY;

    if (!apiKey) {
      throw new Error('GROQ_API_KEY not found');
    }

    this.groq = new Groq({
      apiKey,
    });
  }

  async generateAnswer(prompt: string): Promise<string> {
    const response = await this.groq.chat.completions.create({
      model: 'llama-3.3-70b-versatile',
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
      temperature: 0.2,
    });

    return response.choices[0]?.message?.content ?? '';
  }
}
