import { Injectable, ServiceUnavailableException } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { Observable } from "rxjs";

interface WorkflowRequest {
  workflowType: string;
  query: string;
  conversationId: string;
}

// STREAM EVENTS
export interface WorkflowStreamEvent {
  type: "workflow";
  node: string;
  status: string;
}

export interface TokenStreamEvent {
  type: "token";
  content: string;
}

export interface DoneStreamEvent {
  type: "done";
  workflowRun?: unknown;
}

export type StreamEvent =
  | WorkflowStreamEvent
  | TokenStreamEvent
  | DoneStreamEvent;

@Injectable()
export class AiGatewayService {
  private readonly aiServiceUrl: string;

  constructor(configService: ConfigService) {
    this.aiServiceUrl =
      configService.get<string>("AI_SERVICE_URL") ?? "http://localhost:8000";
  }

  // STREAM WORKFLOW
  streamWorkflow(payload: WorkflowRequest): Observable<StreamEvent> {
    return new Observable<StreamEvent>((subscriber) => {
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
            throw new ServiceUnavailableException(
              `AI service returned ${response.status}`,
            );
          }

          const reader = response.body.getReader();
          const decoder = new TextDecoder();

          // READ SSE STREAM
          while (true) {
            const { done, value } = await reader.read();

            if (done) {
              break;
            }

            const chunk = decoder.decode(value, {
              stream: true,
            });

            pendingChunk = this.readSseChunk(pendingChunk + chunk, (event) =>
              subscriber.next(event),
            );
          }

          // FINAL PENDING CHUNK
          if (pendingChunk) {
            this.readSseChunk(`${pendingChunk}\n`, (event) =>
              subscriber.next(event),
            );
          }

          subscriber.complete();
        })
        .catch((error) => {
          if (!controller.signal.aborted) {
            subscriber.error(error);
          }
        });

      // CLEANUP
      return () => {
        controller.abort();
      };
    });
  }

  streamResumeWorkflow(
  workflowId: string,
  humanApproved: boolean,
): Observable<StreamEvent> {

  return new Observable<StreamEvent>(
    (subscriber) => {

      const controller =
        new AbortController();

      let pendingChunk = "";

      const url = new URL(
        `${this.aiServiceUrl}/ai/resume-workflow/stream`,
      );

      url.searchParams.set(
        "workflow_id",
        workflowId,
      );

      url.searchParams.set(
        "human_approved",
        String(humanApproved),
      );

      void fetch(url.toString(), {
        method: "GET",
        signal: controller.signal,
      })
        .then(async (response) => {

          if (
            !response.ok ||
            !response.body
          ) {

            throw new ServiceUnavailableException(
              `AI service returned ${response.status}`,
            );
          }

          const reader =
            response.body.getReader();

          const decoder =
            new TextDecoder();

          while (true) {

            const {
              done,
              value,
            } = await reader.read();

            if (done) {
              break;
            }

            const chunk =
              decoder.decode(value, {
                stream: true,
              });

            pendingChunk =
              this.readSseChunk(
                pendingChunk + chunk,
                (event) =>
                  subscriber.next(
                    event,
                  ),
              );
          }

          if (pendingChunk) {

            this.readSseChunk(
              `${pendingChunk}\n`,
              (event) =>
                subscriber.next(event),
            );
          }

          subscriber.complete();
        })
        .catch((error) => {

          if (
            !controller.signal.aborted
          ) {

            subscriber.error(error);
          }
        });

      return () => {
        controller.abort();
      };
    },
  );
}


  // SSE PARSER
  private readSseChunk(
    chunk: string,
    onEvent: (event: StreamEvent) => void,
  ): string {
    const lines = chunk.split("\n");

    const pendingLine = lines.pop() ?? "";

    let currentEventType = "message";

    for (const line of lines) {
      // SSE EVENT TYPE
      if (line.startsWith("event: ")) {
        currentEventType = line.slice(7).trim()
        continue;
      }
      // SSE DATA
      if (line.startsWith("data: ")) {
        const parsed = JSON.parse(line.slice(6)) as StreamEvent;

        // Preserve SSE event type
        parsed.type = currentEventType as StreamEvent["type"];

        onEvent(parsed);
      }
    }

    return pendingLine;
  }
}
