"use client";

import { BRAND } from "@/lib/brand";
import { bboxToStyle, type Bbox } from "@/lib/bbox";

export type Mood = "read" | "answer" | "spot";

// The ONE highlight primitive (CONCEPT §4c) — three moods, one implementation. Lime is the
// highlighter: a translucent lime mark over the text on paper. `read` sweeps briefly (watch it
// read), `answer` blooms and holds (the cited line), `spot` is the coverage-map mark.
export function HighlightBox({
  box,
  mood,
  index = 0,
  color,
}: {
  box: Bbox;
  mood: Mood;
  index?: number;
  color?: string;
}) {
  const s = bboxToStyle(box);
  const cls = mood === "read" ? "fp-read" : mood === "answer" ? "fp-answer" : "fp-spot";
  const fill = color ?? BRAND.lime;
  const answerish = mood === "answer";
  return (
    <div
      className={cls}
      style={{
        position: "absolute",
        left: s.left,
        top: s.top,
        width: s.width,
        height: s.height,
        background: mood === "spot" ? `${fill}59` : `${fill}66`,
        borderBottom: answerish ? `2px solid ${BRAND.dark}` : "none",
        borderRadius: 2,
        mixBlendMode: "multiply",
        pointerEvents: "none",
        animationDelay: mood === "read" ? `${index * 11}ms` : undefined,
      }}
    />
  );
}
