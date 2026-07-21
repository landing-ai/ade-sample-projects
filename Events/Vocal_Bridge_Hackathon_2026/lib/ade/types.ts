// DPT-3 / ADE v2 types — modelled on the VERIFIED live response shape
// (see docs/API-CONTRACT.md). Boxes normalized to 0..1 for resolution-independent overlay.

export type Rect = { l: number; t: number; r: number; b: number };
export type Span = [number, number]; // [start, end) code-point offsets into markdown

// One visual line (a grounding `part`): its markdown span + its box on the page.
export type LinePart = { span: Span; rect: Rect };

// A flattened parse block: type + page + its line parts, ready for canvas + bridge.
export type ParseBlock = {
  id: string;
  type: string; // text | table | table_cell | figure | marginalia | ...
  page: number; // 1-indexed, doc-local
  rect: Rect | null; // block bounding box
  parts: LinePart[]; // per-line boxes
};

export type ParsePage = { page: number; width: number; height: number; dpi: number };

export type ParseResult = {
  markdown: string;
  pages: ParsePage[];
  blocks: ParseBlock[];
  pageCount: number;
  failedPages: number[];
};

// Extract v2: each leaf carries the value + the markdown spans that produced it.
export type ExtractLeafMeta = { spans: Span[]; value: unknown };
export type ExtractResult = {
  extraction: Record<string, unknown>;
  metadata: unknown; // extraction_metadata tree — shape mirrors `extraction`
  markdown: string; // echoed back; VERIFIED === the markdown we sent
};

// A grounded box tied to a specific document + page, normalized.
export type GroundBox = { docId: string; page: number; rect: Rect };
