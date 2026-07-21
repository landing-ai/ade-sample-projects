import { env } from "../env";
import type { ExtractResult } from "./types";

const EXTRACT_URL = "https://api.ade.landing.ai/v2/extract";

// Extract v2 over the parsed markdown. Response: { extraction, extraction_metadata, markdown }.
// We send Parse's markdown; VERIFIED that the echoed `markdown` is identical, so
// extraction_metadata.<leaf>.spans index the SAME code-point space as Parse's block/part spans.
export async function extractFieldsV2(markdown: string, schema: object): Promise<ExtractResult> {
  const apiKey = env().visionAgentApiKey;
  if (!apiKey) throw new Error("VISION_AGENT_API_KEY is not set");
  const form = new FormData();
  form.append("markdown", new Blob([markdown], { type: "text/markdown" }), "doc.md");
  form.append("schema", JSON.stringify(schema));

  const doFetch = async (attempt: number): Promise<Response> => {
    try {
      return await fetch(EXTRACT_URL, { method: "POST", headers: { Authorization: `Bearer ${apiKey}` }, body: form });
    } catch (e) {
      if (attempt < 2) {
        await new Promise((r) => setTimeout(r, 1500));
        return doFetch(attempt + 1);
      }
      throw e;
    }
  };
  const res = await doFetch(0);
  if (!res.ok) throw new Error(`ADE extract ${res.status}: ${(await res.text()).slice(0, 400)}`);
  const data = await res.json();
  return {
    extraction: data.extraction ?? {},
    metadata: data.extraction_metadata ?? {},
    markdown: String(data.markdown ?? markdown),
  };
}
