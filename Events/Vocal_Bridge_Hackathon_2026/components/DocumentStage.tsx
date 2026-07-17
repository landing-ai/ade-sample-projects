"use client";

import { useEffect, useRef, useState } from "react";
import { BRAND, fontStack, type PolicyDocRef } from "@/lib/brand";
import type { GroundBox } from "@/lib/policy/grounded";
import { HighlightBox } from "@/components/HighlightLayer";

type Rect = { l: number; t: number; r: number; b: number };
type Part = { span: [number, number]; rect: Rect };
type Block = { id: string; type: string; page: number; rect: Rect | null; parts: Part[] };
type CanvasData = { pages: { page: number; width: number; height: number; dpi: number }[]; blocks: Block[] };

// Anatomy x-ray palette (opt-in). The page stays paper+lime by default; color lives only here.
const TYPE_COLOR: Record<string, string> = {
  text: BRAND.blue,
  table: BRAND.lightGreen,
  table_cell: BRAND.lightGreen,
  figure: BRAND.lavender,
  marginalia: BRAND.grey,
  attestation: "#d8b4fe",
  logo: BRAND.midGreen,
  scan_code: "#f0a58a",
};

export type StageHighlight = { boxes: GroundBox[]; token: number } | null;

export function DocumentStage({
  docs,
  reading,
  anatomy,
  highlight,
  spotlight,
}: {
  docs: PolicyDocRef[];
  reading: boolean;
  anatomy: boolean;
  highlight: StageHighlight;
  spotlight: GroundBox[] | null;
}) {
  const [canvas, setCanvas] = useState<Record<string, CanvasData>>({});
  const scrollRef = useRef<HTMLDivElement | null>(null);
  const pageRefs = useRef<Record<string, HTMLDivElement | null>>({});

  useEffect(() => {
    let cancelled = false;
    (async () => {
      for (const d of docs) {
        try {
          const data = (await (await fetch(`/api/documents/${d.id}/canvas`)).json()) as CanvasData;
          if (!cancelled && data.pages) setCanvas((prev) => ({ ...prev, [d.id]: data }));
        } catch {
          /* canvas optional — page images still render */
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [docs]);

  // Scroll the cited line into view when a new answer arrives.
  useEffect(() => {
    const first = highlight?.boxes[0];
    if (!first) return;
    const el = pageRefs.current[`${first.docId}:${first.page}`];
    if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
  }, [highlight]);

  const boxesFor = (list: GroundBox[] | undefined, docId: string, page: number): Rect[] =>
    (list ?? []).filter((b) => b.docId === docId && b.page === page).map((b) => b.rect);

  return (
    <div
      ref={scrollRef}
      style={{
        background: BRAND.dark,
        padding: 18,
        borderRadius: 2,
        maxHeight: "calc(100vh - 190px)",
        overflowY: "auto",
      }}
    >
      {docs.map((doc) => {
        const c = canvas[doc.id];
        const pageCount = doc.pageCount || c?.pages.length || 1;
        return Array.from({ length: pageCount }, (_, i) => i + 1).map((page) => {
          const key = `${doc.id}:${page}`;
          const pageBlocks = (c?.blocks ?? []).filter((b) => b.page === page);
          let readIdx = 0;
          const answerRects = boxesFor(highlight?.boxes, doc.id, page);
          const spotRects = boxesFor(spotlight ?? undefined, doc.id, page);
          return (
            <div
              key={key}
              ref={(el) => {
                pageRefs.current[key] = el;
              }}
              style={{ position: "relative", background: "#fff", marginBottom: 16, boxShadow: "0 1px 0 rgba(0,0,0,0.4)" }}
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={`/api/documents/${doc.id}/page-image?page=${page}`}
                alt={`${doc.filename} page ${page}`}
                loading="lazy"
                style={{ display: "block", width: "100%", height: "auto" }}
              />
              {/* Anatomy x-ray: color every block by type */}
              {anatomy &&
                pageBlocks.map((b, bi) =>
                  b.rect ? <HighlightBox key={`a${bi}`} box={b.rect} mood="spot" color={TYPE_COLOR[b.type] ?? BRAND.blue} /> : null
                )}
              {/* Watch it read: brisk monochrome sweep across every line */}
              {reading &&
                !anatomy &&
                pageBlocks.flatMap((b, bi) =>
                  b.parts.map((p, pi) => <HighlightBox key={`r${bi}-${pi}`} box={p.rect} mood="read" index={readIdx++} />)
                )}
              {/* Coverage-map spotlight */}
              {spotRects.map((r, si) => (
                <HighlightBox key={`s${si}`} box={r} mood="spot" />
              ))}
              {/* The answer: the cited line, blooming and holding */}
              {answerRects.map((r, ai) => (
                <HighlightBox key={`ans${ai}`} box={r} mood="answer" />
              ))}
              <div
                style={{
                  position: "absolute",
                  bottom: 6,
                  right: 8,
                  fontFamily: fontStack.body,
                  fontSize: 10,
                  color: BRAND.grey,
                  background: "rgba(255,255,255,0.7)",
                  padding: "1px 6px",
                  borderRadius: 2,
                }}
              >
                {docs.length > 1 ? `${doc.filename} · ` : ""}p.{page}
              </div>
            </div>
          );
        });
      })}
    </div>
  );
}
