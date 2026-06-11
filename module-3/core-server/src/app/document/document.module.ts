import { Module } from '@nestjs/common';
import { DocumentService } from './document.service';
import { DocumentController } from './document.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Document } from './entities/document.entity';
import { Chunk } from '../chunk/entities/chunk.entity';
import { EmbeddingModule } from '../embedding/embedding.module';

@Module({
  imports: [TypeOrmModule.forFeature([Document, Chunk]), EmbeddingModule],
  controllers: [DocumentController],
  providers: [DocumentService],
})
export class DocumentModule {}
