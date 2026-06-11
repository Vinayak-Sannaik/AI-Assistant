import { Injectable } from '@nestjs/common';
import { CreateChunkDto } from './dto/create-chunk.dto';
import { EmbeddingService } from '../embedding/embedding.service';
import { Chunk } from './entities/chunk.entity';
import { Repository } from 'typeorm';
import { InjectRepository } from '@nestjs/typeorm/dist/common/typeorm.decorators';

export interface ChunkResult {
  content: string;
  distance: number;
}

function toVectorString(vec: number[]): string {
  return `[${vec.join(',')}]`;
}

@Injectable()
export class ChunkService {
  constructor(
    @InjectRepository(Chunk)
    private readonly chunkRepository: Repository<Chunk>,
    private readonly embeddingService: EmbeddingService,
  ) {}

  create(createChunkDto: CreateChunkDto) {
    return 'This action adds a new chunk';
  }

  findAll() {
    return `This action returns all chunk`;
  }

  findOne(id: number) {
    return `This action returns a #${id} chunk`;
  }

  remove(id: number) {
    return `This action removes a #${id} chunk`;
  }

  async searchSimilar(query: string, limit: number = 5): Promise<any[]> {
    // Normalize query: lowercase and trim
    const normalizedQuery = query.toLowerCase().trim();
    const embedding: number[] =
      await this.embeddingService.embed(normalizedQuery);

    const vector = toVectorString(embedding);

    const results: any[] = await this.chunkRepository.query(
      `   
          SELECT 
          content,
          embedding <=> $1 AS vector_distance,
          ts_rank(tsv, plainto_tsquery($2)) AS keyword_score
          FROM chunk
      `,
      [vector, query],
    );

    // normalize + combine
    const hybrid = results.map((r) => {
      const vectorScore = 1 - r.vector_distance; // convert distance → similarity
      const keywordScore = r.keyword_score;

      return {
        content: r.content,
        distance: 0.7 * vectorScore + 0.3 * keywordScore,
      };
    });

    return hybrid.sort((a, b) => b.distance - a.distance).slice(0, 3);
  }
}
