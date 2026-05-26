import { Body, Controller, Param, Post, Sse } from "@nestjs/common";
import { Observable, concat, defer, map, of } from "rxjs";
import { AiGatewayService } from "../ai/ai-gateway.service";
import { ChatService } from "./chat.service";
import { ChatMessage, Conversation } from "./chat.types";
import { selectWorkflowType } from "./helper";

// DTOs
interface CreateConversationDto {
  message: string;
}

interface AddMessageDto {
  content: string;
}
// SSE Event Returned To Frontend
interface MessageEvent {
  type: string;
  data: string;
}

// AI Stream Events
interface WorkflowEvent {
  type: "workflow";
  node: string;
  status: string;
}

interface TokenEvent {
  type: "token";
  content: string;
}

interface DoneEvent {
  type: "done";
  workflowRun?: unknown;
}

type StreamEvent = WorkflowEvent | TokenEvent | DoneEvent;

@Controller("chat")
export class ChatController {
  constructor(
    private readonly chatService: ChatService,
    private readonly aiGateway: AiGatewayService,
  ) {}

  // CREATE CONVERSATION
  @Post("conversations")
  createConversation(@Body() body: CreateConversationDto): Conversation {
    return this.chatService.createConversation(body.message);
  }

  // ADD USER MESSAGE
  @Post("conversations/:conversationId/messages")
  addMessage(
    @Param("conversationId")
    conversationId: string,

    @Body()
    body: AddMessageDto,
  ): ChatMessage {
    return this.chatService.addUserMessage(conversationId, body.content);
  }

  // STREAM AI RESPONSE
  @Sse("conversations/:conversationId/stream")
  stream(
    @Param("conversationId")
    conversationId: string,
  ): Observable<MessageEvent> {
    // Latest user message
    const latestMessage = this.chatService.getLatestUserMessage(conversationId);

    // AI orchestration stream
    const eventStream = this.aiGateway.streamWorkflow({
      conversationId,
      query: latestMessage.content,
      workflowType: selectWorkflowType(latestMessage.content),
    });

    // SSE observable
    return new Observable<MessageEvent>((subscriber) => {
      let fullResponse = "";

      const subscription = concat(
        // STREAM EVENTS
        eventStream.pipe(
          map((event: StreamEvent) => {
            // Accumulate only token text
            if (event.type === "token") {
              fullResponse += event.content;
            }
            // Forward original SSE event type
            return {
              type: event.type,
              data: JSON.stringify(event),
            };
          }),
        ),
        // FINAL DONE EVENT
        defer(() => {
          const savedMessage = this.chatService.addAssistantMessage(
            conversationId,
            fullResponse,
          );

          return of({
            type: "done",
            data: JSON.stringify(savedMessage),
          });
        }),
      ).subscribe(subscriber);

      // Cleanup
      return () => {
        subscription.unsubscribe();
      };
    });
  }
}
