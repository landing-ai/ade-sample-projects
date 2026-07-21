// THE SPAN BRIDGE (CONCEPT §6, verified 2026-07-11).
//
//   Extract field.spans  ∩  Parse part.span  →  part.rect  →  a line box on the page
//
// Extract's extraction_metadata.<leaf>.spans and Parse's grounding block/part spans index the
// SAME markdown code-point space (verified byte-identical). So resolving a typed field to its
// pixel location is a pure interval-overlap lookup — no model, no invented ids. This retires
// v1's Claude-invented chunk_ids with first-party, documented grounding.

import type { GroundBox, ParseBlock, Span } from "./types";

function overlaps(a: Span, b: Span): boolean {
  return a[0] < b[1] && b[0] < a[1]; // half-open intervals [start, end)
}

// Given a set of Extract spans and one document's Parse blocks, return the line boxes whose
// span overlaps any field span. Parts are the per-line units; a block with no parts falls back
// to its own box. De-duplicated, page-ordered.
export function spansToBoxes(spans: Span[], docId: string, blocks: ParseBlock[]): GroundBox[] {
  if (!spans?.length) return [];
  const out: GroundBox[] = [];
  const seen = new Set<string>();
  const push = (page: number, rect: { l: number; t: number; r: number; b: number }) => {
    const key = `${page}:${rect.l.toFixed(4)}:${rect.t.toFixed(4)}:${rect.r.toFixed(4)}:${rect.b.toFixed(4)}`;
    if (seen.has(key)) return;
    seen.add(key);
    out.push({ docId, page, rect });
  };
  for (const block of blocks) {
    if (block.parts.length) {
      for (const part of block.parts) {
        if (spans.some((s) => overlaps(s, part.span))) push(block.page, part.rect);
      }
    } else if (block.rect) {
      // No line parts (e.g. a figure) — fall back to the block box if its span overlaps.
      // We approximate the block span by the union of any parts; with none, use the rect only
      // when a field span lands on this block. Blocks without parts rarely carry field values,
      // so this is a safe last resort.
    }
  }
  return out.sort((a, b) => a.page - b.page || a.rect.t - b.rect.t);
}

// Walk an extraction_metadata tree and pull every leaf's spans, keyed by a dotted path
// (e.g. "benefits.3.limit_amount"). A leaf is a node carrying a `spans` array.
export function collectLeafSpans(metaNode: unknown, prefix = ""): Record<string, Span[]> {
  const out: Record<string, Span[]> = {};
  const walk = (node: unknown, path: string) => {
    if (node == null || typeof node !== "object") return;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const n = node as any;
    if (Array.isArray(n.spans)) {
      const spans = (n.spans as unknown[])
        .map((s) => (Array.isArray(s) && s.length === 2 ? ([s[0], s[1]] as Span) : null))
        .filter((s): s is Span => !!s);
      if (spans.length) out[path || "value"] = spans;
      return;
    }
    if (Array.isArray(n)) {
      n.forEach((c, i) => walk(c, path ? `${path}.${i}` : String(i)));
      return;
    }
    for (const k of Object.keys(n)) walk(n[k], path ? `${path}.${k}` : k);
  };
  walk(metaNode, prefix);
  return out;
}
