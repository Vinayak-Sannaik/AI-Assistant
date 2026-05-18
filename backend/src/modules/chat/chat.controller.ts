import { Body, Controller, Param, Post, Sse } from '@nestjs/common';
import { Observable, concat, defer, map, of } from 'rxjs';
import { AiGatewayService } from '../ai/ai-gateway.service';
import { ChatService } from './chat.service';
import { ChatMessage, Conversation } from './chat.types';

interface CreateConversationDto {
  message: string;
}

interface AddMessageDto {
  content: string;
}

interface MessageEvent {
  type: string;
  data: string;
}

@Controller('chat')
export class ChatController {
  constructor(
    private readonly chatService: ChatService,
    private readonly aiGateway: AiGatewayService,
  ) {}

  @Post('conversations')
  createConversation(@Body() body: CreateConversationDto): Conversation {
    return this.chatService.createConversation(body.message);
  }

  @Post('conversations/:conversationId/messages')
  addMessage(@Param('conversationId') conversationId: string, @Body() body: AddMessageDto): ChatMessage {
    return this.chatService.addUserMessage(conversationId, body.content);
  }

  @Sse('conversations/:conversationId/stream')
  stream(@Param('conversationId') conversationId: string): Observable<MessageEvent> {
    const latestMessage = this.chatService.getLatestUserMessage(conversationId);
    const tokenStream = this.aiGateway.streamWorkflow({
      conversationId,
      query: latestMessage.content,
      workflowType: 'core_chat',
    });

    return new Observable<MessageEvent>((subscriber) => {
      let fullResponse = '';
      const subscription = concat(
        tokenStream.pipe(
          map((token) => {
            fullResponse += token;
            return { type: 'token', data: JSON.stringify(token) };
          }),
        ),
        defer(() => {
          const savedMessage = this.chatService.addAssistantMessage(conversationId, fullResponse);
          return of({ type: 'done', data: JSON.stringify(savedMessage) });
        }),
      ).subscribe(subscriber);

      return () => subscription.unsubscribe();
    });
  }
}
