import { ZodType } from "zod";
import { env } from "../env";
import { ChatMessage, ChatParams, ChatTransport } from "./types";
import { openAICompatTransport } from "./openai-compat";
import { anthropicTransport } from "./anthropic";

const PRESETS = {
  ollama: { baseUrl: "http://localhost:11434/v1", keyEnv: null, defaultModel: "qwen3" },
  openai: { baseUrl: "https://api.openai.com/v1", keyEnv: "OPENAI_API_KEY", defaultModel: "gpt-4.1" },
  gemini: { baseUrl: "https://generativelanguage.googleapis.com/v1beta/openai", keyEnv: "GEMINI_API_KEY", defaultModel: "gemini-2.5-pro" },
} as const;

export function getTransport(): ChatTransport {
  const e = env();
  const model = e.llmModel || undefined;
  if (e.llmProvider === "anthropic") {
    const apiKey = e.llmApiKey || process.env.ANTHROPIC_API_KEY || "";
    if (!apiKey) throw new Error("anthropic provider selected but no ANTHROPIC_API_KEY set");
    return anthropicTransport({ apiKey, model: model ?? "claude-opus-4-8" });
  }
  const preset = PRESETS[e.llmProvider];
  const apiKey = e.llmApiKey || (preset.keyEnv ? process.env[preset.keyEnv] ?? "" : "");
  return openAICompatTransport({
    baseUrl: e.llmBaseUrl || preset.baseUrl,
    apiKey: apiKey || undefined,
    model: model ?? preset.defaultModel,
  });
}

// Port of prototype parseJsonReply (fineprint-policy-copilot.jsx:54-60)
export function parseJsonReply(raw: string): unknown {
  const clean = raw.replace(/```json|```/g, "").trim();
  const start = clean.indexOf("{");
  const end = clean.lastIndexOf("}");
  if (start === -1 || end === -1) throw new Error("No JSON found in reply");
  return JSON.parse(clean.slice(start, end + 1));
}

export async function chatJSONWith<T>(
  transport: ChatTransport,
  p: ChatParams & { schema: ZodType<T> }
): Promise<T> {
  const attempt = async (messages: ChatMessage[]) => {
    const raw = await transport.chat({ system: p.system, messages, maxTokens: p.maxTokens });
    return p.schema.parse(parseJsonReply(raw));
  };
  try {
    return await attempt(p.messages);
  } catch (err) {
    const feedback: ChatMessage = {
      role: "user",
      content: `Your previous reply was not valid JSON for the required schema. Error: ${String(err).slice(0, 500)}. Respond again with ONLY a corrected JSON object.`,
    };
    return attempt([...p.messages, feedback]);
  }
}

export const chat = (p: ChatParams) => getTransport().chat(p);
export const chatJSON = <T>(p: ChatParams & { schema: ZodType<T> }) => chatJSONWith(getTransport(), p);
