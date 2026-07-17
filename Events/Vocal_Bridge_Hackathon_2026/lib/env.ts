export type LlmProvider = "ollama" | "openai" | "gemini" | "anthropic";

export function env() {
  const llmProvider = (process.env.LLM_PROVIDER ?? "ollama") as LlmProvider;
  return {
    llmProvider,
    llmModel: process.env.LLM_MODEL ?? "",
    llmBaseUrl: process.env.LLM_BASE_URL ?? "",
    llmApiKey: process.env.LLM_API_KEY ?? "",
    visionAgentApiKey: process.env.VISION_AGENT_API_KEY ?? "",
    vocalBridgeApiKey: process.env.VOCAL_BRIDGE_API_KEY ?? "",
    vocalBridgeAgentId: process.env.VOCAL_BRIDGE_AGENT_ID ?? "",
    deleteRawPdfs: process.env.DELETE_RAW_PDFS_AFTER_EXTRACTION === "true",
  };
}
