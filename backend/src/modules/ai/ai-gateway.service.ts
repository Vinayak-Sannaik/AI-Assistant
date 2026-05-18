import { Injectable, ServiceUnavailableException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Observable } from 'rxjs';

interface WorkflowRequest {
  workflowType: string;
  query: string;
  conversationId: string;
}

@Injectable()
export class AiGatewayService {
  private readonly aiServiceUrl: string;

  constructor(configService: ConfigService) {
    this.aiServiceUrl = configService.get<string>('AI_SERVICE_URL') ?? 'http://localhost:8000';
  }

  streamWorkflow(payload: WorkflowRequest): Observable<string> {
    return new Observable<string>((subscriber) => {
      const controller = new AbortController();
      let pendingChunk = '';

      void fetch(`${this.aiServiceUrl}/ai/execute-workflow/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
        signal: controller.signal,
      })
        .then(async (response) => {
          if (!response.ok || !response.body) {
            throw new ServiceUnavailableException(`AI service returned ${response.status}`);
          }

          const reader = response.body.getReader();
          const decoder = new TextDecoder();

          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            pendingChunk = this.readSseChunk(pendingChunk + chunk, (token) => subscriber.next(token));
          }

          if (pendingChunk) {
            this.readSseChunk(`${pendingChunk}\n`, (token) => subscriber.next(token));
          }

          subscriber.complete();
        })
        .catch((error) => {
          if (!controller.signal.aborted) {
            subscriber.error(error);
          }
        });

      return () => controller.abort();
    });
  }

  private readSseChunk(chunk: string, onToken: (token: string) => void): string {
    const lines = chunk.split('\n');
    const pendingLine = lines.pop() ?? '';

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        onToken(JSON.parse(line.slice(6)) as string);
      }
    }

    return pendingLine;
  }
}
