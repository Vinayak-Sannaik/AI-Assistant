import { Controller, Get, Post, Body, Param, Delete } from '@nestjs/common';
import { ChunkService } from './chunk.service';
import { CreateChunkDto } from './dto/create-chunk.dto';
import { aiAssistant } from '../../common/prompts/ai-assistant';
import { LlmService } from '../llm/llm.service';

@Controller('chunks')
export class ChunkController {
  constructor(
    private readonly chunkService: ChunkService,
    private readonly llmService: LlmService,
  ) {}

  @Post()
  create(@Body() createChunkDto: CreateChunkDto) {
    return this.chunkService.create(createChunkDto);
  }

  @Get()
  findAll() {
    return this.chunkService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.chunkService.findOne(+id);
  }

  @Post('search')
  async search(@Body() body: { query: string }) {
    // console.log('Received search query:', body.query);
    return this.chunkService.searchSimilar(body.query);
  }

  @Post('ask')
  async ask(@Body() body: { query: string }) {
    const chunks = await this.chunkService.searchSimilar(body.query);
    // const v = await this.llmService.listModels();
    const context = chunks.map((c) => c.content).join('\n');
    const prompt = aiAssistant(context, body.query);
    const answer: string = await this.llmService.generateAnswer(prompt);
    return {
      answer,
      chunks,
    };
  }

  // @Patch(':id')
  // update(@Param('id') id: string, @Body() updateChunkDto: UpdateChunkDto) {
  //   return this.chunkService.update(+id, updateChunkDto);
  // }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.chunkService.remove(+id);
  }
}
