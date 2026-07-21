import { ChatParams, ChatTransport } from "./types";

export function openAICompatTransport(cfg: { baseUrl: string; apiKey?: string; model: string }): ChatTransport {
  return {
    async chat({ system, messages, maxTokens }: ChatParams): Promise<string> {
      const res = await fetch(`${cfg.baseUrl.replace(/\/$/, "")}/chat/completions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(cfg.apiKey ? { Authorization: `Bearer ${cfg.apiKey}` } : {}),
        },
        body: JSON.stringify({
          model: cfg.model,
          max_tokens: maxTokens ?? 2048,
          messages: [{ role: "system", content: system }, ...messages],
        }),
      });
      if (!res.ok) throw new Error(`LLM ${res.status}: ${(await res.text()).slice(0, 300)}`);
      const data = await res.json();
      const content = data.choices?.[0]?.message?.content;
      if (typeof content !== "string") throw new Error("LLM returned no text content");
      return content;
    },
  };
}
