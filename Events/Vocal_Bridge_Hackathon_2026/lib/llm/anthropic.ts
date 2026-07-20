import Anthropic from "@anthropic-ai/sdk";
import { ChatParams, ChatTransport } from "./types";

export function anthropicTransport(cfg: { apiKey: string; model: string }): ChatTransport {
  const client = new Anthropic({ apiKey: cfg.apiKey });
  return {
    async chat({ system, messages, maxTokens }: ChatParams): Promise<string> {
      const response = await client.messages.create({
        model: cfg.model,
        max_tokens: maxTokens ?? 2048,
        system,
        messages,
      });
      return response.content
        .filter((b): b is Anthropic.TextBlock => b.type === "text")
        .map((b) => b.text)
        .join("\n");
    },
  };
}
