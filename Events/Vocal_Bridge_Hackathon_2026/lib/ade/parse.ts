import { env } from "../env";
import type { LinePart, ParseBlock, ParsePage, ParseResult, Rect, Span } from "./types";

const PARSE_URL = "https://api.ade.landing.ai/v2/parse";
const MODEL = "dpt-3-pro-latest";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Node = any;

function asSpan(s: unknown): Span | null {
  return Array.isArray(s) && s.length === 2 && typeof s[0] === "number" && typeof s[1] === "number"
    ? [s[0], s[1]]
    : null;
}

// box:[l,t,r,b] px at page dpi → normalized 0..1 rect by the page's width/height.
function normBox(box: unknown, w: number, h: number): Rect | null {
  if (!Array.isArray(box) || box.length < 4 || w <= 0 || h <= 0) return null;
  const [l, t, r, b] = box as number[];
  if ([l, t, r, b].some((v) => typeof v !== "number")) return null;
  return { l: l / w, t: t / h, r: r / w, b: b / h };
}

// Collect every leaf line-part under a grounding block: prefer its own `parts`, else recurse
// into `children` (tables expose per-cell/row boxes), else fall back to the block box.
function collectParts(node: Node, w: number, h: number): LinePart[] {
  const out: LinePart[] = [];
  const walk = (n: Node) => {
    if (!n || typeof n !== "object") return;
    if (Array.isArray(n.parts) && n.parts.length) {
      for (const p of n.parts) {
        const span = asSpan(p.span);
        const rect = normBox(p.box, w, h);
        if (span && rect) out.push({ span, rect });
      }
      return;
    }
    if (Array.isArray(n.children) && n.children.length) {
      for (const c of n.children) walk(c);
      return;
    }
    const span = asSpan(n.span);
    const rect = normBox(n.box, w, h);
    if (span && rect) out.push({ span, rect });
  };
  walk(node);
  return out;
}

// Flatten { structure, grounding } into per-page dims + a flat block list with normalized
// boxes and per-line parts. Structure carries page width/height/dpi + block nesting; grounding
// carries the boxes/parts. We zip them by page index and read boxes from grounding.
export function normalizeParseV2(raw: Node): ParseResult {
  const markdown = String(raw?.markdown ?? "");
  const structPages: Node[] = raw?.structure?.children ?? [];
  const groundPages: Node[] = raw?.grounding?.children ?? [];

  const pages: ParsePage[] = [];
  const blocks: ParseBlock[] = [];

  for (const sp of structPages) {
    const page0 = typeof sp.page === "number" ? sp.page : 0;
    const page = page0 + 1; // 1-indexed, doc-local
    const width = Number(sp.width) || 0;
    const height = Number(sp.height) || 0;
    const dpi = Number(sp.dpi) || 0;
    pages.push({ page, width, height, dpi });

    const gp = groundPages.find((g) => (typeof g.page === "number" ? g.page : -1) === page0);
    const gBlocks: Node[] = gp?.children ?? [];
    for (const gb of gBlocks) {
      const parts = collectParts(gb, width, height);
      blocks.push({
        id: String(gb.id ?? `${page}-${blocks.length}`),
        type: String(gb.type ?? "text"),
        page,
        rect: normBox(gb.box, width, height),
        parts,
      });
    }
  }

  return {
    markdown,
    pages,
    blocks,
    pageCount: Number(raw?.metadata?.page_count) || pages.length,
    failedPages: Array.isArray(raw?.metadata?.failed_pages) ? raw.metadata.failed_pages : [],
  };
}

export async function parseDocumentV2(
  file: { buffer: Buffer; mimeType: string; filename: string },
  opts?: { pages?: number[] }
): Promise<ParseResult> {
  const apiKey = env().visionAgentApiKey;
  if (!apiKey) throw new Error("VISION_AGENT_API_KEY is not set");
  const form = new FormData();
  form.append("document", new Blob([new Uint8Array(file.buffer)], { type: file.mimeType }), file.filename);
  form.append("model", MODEL);
  if (opts?.pages) form.append("options", JSON.stringify({ pages: opts.pages }));

  // One retry — the large-upload TLS reset we saw in probing is transient.
  const doFetch = async (attempt: number): Promise<Response> => {
    try {
      return await fetch(PARSE_URL, { method: "POST", headers: { Authorization: `Bearer ${apiKey}` }, body: form });
    } catch (e) {
      if (attempt < 2) {
        await new Promise((r) => setTimeout(r, 1500));
        return doFetch(attempt + 1);
      }
      throw e;
    }
  };
  const res = await doFetch(0);
  if (!res.ok) throw new Error(`ADE parse ${res.status}: ${(await res.text()).slice(0, 400)}`);
  return normalizeParseV2(await res.json());
}
