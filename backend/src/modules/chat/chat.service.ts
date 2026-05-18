import { Injectable, NotFoundException } from '@nestjs/common';
import { Conversation, ChatMessage } from './chat.types';

@Injectable()
export class ChatService {
  private readonly conversations = new Map<string, Conversation>();

  createConversation(message: string): Conversation {
    const now = new Date().toISOString();
    const conversation: Conversation = {
      id: crypto.randomUUID(),
      title: this.createTitle(message),
      createdAt: now,
      messages: [
        {
          id: crypto.randomUUID(),
          role: 'user',
          content: message,
          createdAt: now,
        },
      ],
    };

    this.conversations.set(conversation.id, conversation);
    return conversation;
  }

  addUserMessage(conversationId: string, content: string): ChatMessage {
    const conversation = this.getConversation(conversationId);
    const message: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content,
      createdAt: new Date().toISOString(),
    };
    conversation.messages.push(message);
    return message;
  }

  addAssistantMessage(conversationId: string, content: string): ChatMessage {
    const conversation = this.getConversation(conversationId);
    const message: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'assistant',
      content,
      createdAt: new Date().toISOString(),
    };
    conversation.messages.push(message);
    return message;
  }

  getConversation(conversationId: string): Conversation {
    const conversation = this.conversations.get(conversationId);
    if (!conversation) {
      throw new NotFoundException(`Conversation ${conversationId} was not found`);
    }
    return conversation;
  }

  getLatestUserMessage(conversationId: string): ChatMessage {
    const conversation = this.getConversation(conversationId);
    const message = [...conversation.messages].reverse().find((item) => item.role === 'user');
    if (!message) {
      throw new NotFoundException(`Conversation ${conversationId} has no user messages`);
    }
    return message;
  }

  private createTitle(message: string): string {
    const title = message.trim().replace(/\s+/g, ' ').slice(0, 54);
    return title.length < message.trim().length ? `${title}...` : title || 'New conversation';
  }
}
