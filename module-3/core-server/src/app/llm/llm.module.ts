// llm.module.ts

import { Module } from '@nestjs/common';
import { LlmService } from './llm.service';
import { GeminiProvider } from './providers/gemini.provider';
import { GroqProvider } from './providers/groq.provider';

@Module({
  providers: [LlmService, GeminiProvider, GroqProvider],
  exports: [LlmService],
})
export class LlmModule {}
