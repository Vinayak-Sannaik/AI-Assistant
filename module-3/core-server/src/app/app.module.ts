import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm/dist/typeorm.module';
import { DataSource } from 'typeorm';
import { DocumentModule } from './document/document.module';
import { ChunkModule } from './chunk/chunk.module';
import { EmbeddingService } from './embedding/embedding.service';
import { EmbeddingModule } from './embedding/embedding.module';
import { LlmService } from './llm/llm.service';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
      // load: [configuration],
    }),

    TypeOrmModule.forRootAsync({
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        type: 'postgres',
        host: config.get<string>('DB_HOST'),
        port: Number(config.get('DB_PORT')),
        username: config.get<string>('DB_USERNAME'),
        password: config.get<string>('DB_PASSWORD'),
        database: config.get<string>('DB_NAME'),
        autoLoadEntities: true,
        synchronize: false,
        ssl: {
          rejectUnauthorized: false,
        },
      }),
    }),

    DocumentModule,

    ChunkModule,

    EmbeddingModule,
  ],
  controllers: [AppController],
  providers: [AppService, EmbeddingService, LlmService],
})
export class AppModule {
  constructor(private dataSource: DataSource) {
    console.log('DB Connected:', this.dataSource.isInitialized);
  }
}
