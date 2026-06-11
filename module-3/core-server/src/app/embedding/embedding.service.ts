// import { Injectable } from '@nestjs/common';
// import { GoogleGenerativeAI } from '@google/generative-ai';

// @Injectable()
// export class EmbeddingService {
//   private genAI: GoogleGenerativeAI;

//   constructor() {
//     const apiKey = process.env.GEMINI_API_KEY;
//     if (!apiKey) {
//       throw new Error('GEMINI_API_KEY environment variable is not set');
//     }
//     this.genAI = new GoogleGenerativeAI(apiKey);
//   }

//   async embed(text: string): Promise<number[]> {
//     const model = this.genAI.getGenerativeModel({
//       model: 'text-embedding-004',
//     });

//     const result = await model.embedContent({
//       content: {
//         role: 'user',
//         parts: [{ text }],
//       },
//     });

//     return result.embedding.values;
//   }
// }

import { Injectable } from '@nestjs/common';
import axios from 'axios';

@Injectable()
export class EmbeddingService {
  async embed(text: string): Promise<number[]> {
    const res = await axios.post('http://localhost:8000/embed', {
      text,
    });

    // Explicitly type the result as EmbedContentResponse
    const embeddingResult = res.data as { embedding: number[] };
    return embeddingResult.embedding;
  }
}
