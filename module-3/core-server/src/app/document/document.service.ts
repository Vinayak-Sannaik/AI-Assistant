import { Injectable } from '@nestjs/common';
import { CreateDocumentDto } from './dto/create-document.dto';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Document } from './entities/document.entity';
import { chunkText } from 'src/common/utils/chunk.util';
import { Chunk } from '../chunk/entities/chunk.entity';
import { EmbeddingService } from '../embedding/embedding.service';

@Injectable()
export class DocumentService {
  constructor(
    @InjectRepository(Document)
    private readonly documentsRepository: Repository<Document>,

    @InjectRepository(Chunk)
    private readonly chunksRepository: Repository<Chunk>,

    private readonly embeddingService: EmbeddingService,
  ) {}

  async create(createDocumentDto: CreateDocumentDto) {
    // Create and save the document entity
    const document = this.documentsRepository.create(createDocumentDto);
    await this.documentsRepository.save(document);

    // Chunk the content and associate with the saved document
    const chunks = chunkText(createDocumentDto.content);
    const chunkEntities: Chunk[] = [];

    for (let i = 0; i < chunks.length; i++) {
      const embedding = await this.embeddingService.embed(chunks[i]);

      const chunk = this.chunksRepository.create({
        content: chunks[i],
        order: i,
        document,
        embedding,
      });

      chunkEntities.push(chunk);
    }
    await this.chunksRepository.save(chunkEntities);

    return document;
  }

  findAll() {
    return this.documentsRepository.find();
  }

  // findOne(id: number) {
  //   return this.documentsRepository.findOneBy({ id });
  // }

  remove(id: number) {
    return this.documentsRepository.delete(id);
  }
}
