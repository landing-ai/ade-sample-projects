export type ChatMessage = { role: "user" | "assistant"; content: string };
export type ChatParams = { system: string; messages: ChatMessage[]; maxTokens?: number };
export interface ChatTransport {
  chat(p: ChatParams): Promise<string>;
}
