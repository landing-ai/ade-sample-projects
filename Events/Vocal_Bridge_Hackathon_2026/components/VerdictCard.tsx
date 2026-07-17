"use client";

import { BRAND, fontStack } from "@/lib/brand";
import type { Verdict } from "@/lib/policy/schema";
import type { GroundBox } from "@/lib/policy/grounded";
import { VERDICT_STYLES, ROLE_STYLES } from "@/components/atoms";

// The grounded verdict, rendered in the voice rail. Each citation with resolved boxes is a
// button that lights the exact line on the stage — grounding is always one gesture away, never
// buried behind a toggle. The Playfair line (the headline) is the one human moment (CONCEPT §4c).
export function VerdictCard({
  result,
  onCite,
}: {
  result: Verdict;
  onCite: (boxes: GroundBox[]) => void;
}) {
  const vs = VERDICT_STYLES[result.verdict];
  return (
    <div style={{ border: `1px solid ${BRAND.midGreen}`, background: "#fffef8", borderRadius: 2, overflow: "hidden" }}>
      <div style={{ background: vs.bg, color: vs.fg, padding: "10px 14px", display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
        <span style={{ fontFamily: fontStack.display, fontWeight: 800, fontSize: 13, letterSpacing: "0.04em", textTransform: "uppercase" }}>
          {vs.label}
        </span>
        {result.benefit && <span style={{ fontFamily: fontStack.body, fontSize: 12, opacity: 0.85 }}>{result.benefit}</span>}
      </div>
      <div style={{ padding: "12px 14px" }}>
        <div style={{ fontFamily: fontStack.accent, fontStyle: "italic", fontSize: 18, color: BRAND.dark, lineHeight: 1.35 }}>
          {result.headline}
        </div>
        <div style={{ fontFamily: fontStack.body, fontSize: 13, color: BRAND.grey, marginTop: 8, lineHeight: 1.55 }}>
          {result.reasoning}
        </div>

        {result.citations.length > 0 && (
          <div style={{ marginTop: 12, display: "flex", flexDirection: "column", gap: 6 }}>
            {result.citations.map((c, i) => {
              const rs = ROLE_STYLES[c.role] ?? ROLE_STYLES.supports;
              const grounded = c.boxes.length > 0;
              return (
                <button
                  key={i}
                  onClick={() => grounded && onCite(c.boxes)}
                  disabled={!grounded}
                  title={grounded ? "Show the exact line on the page" : "No location grounded"}
                  style={{ textAlign: "left", background: "#fff", border: `1px solid ${BRAND.midGreen}`, borderLeft: `4px solid ${rs.bg}`, padding: "8px 12px", cursor: grounded ? "pointer" : "default", fontFamily: fontStack.body }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
                    <span style={{ fontFamily: fontStack.display, fontWeight: 700, fontSize: 9.5, letterSpacing: "0.1em", textTransform: "uppercase", background: rs.bg, color: rs.color, padding: "1px 7px" }}>
                      {rs.label}
                    </span>
                    {grounded && <span style={{ fontSize: 11, color: BRAND.dark }}>show on page →</span>}
                  </div>
                  <div style={{ fontSize: 12.5, color: BRAND.dark, marginTop: 5, lineHeight: 1.45 }}>{c.text}</div>
                </button>
              );
            })}
          </div>
        )}

        {result.deadlines.length > 0 && (
          <div style={{ marginTop: 10, fontFamily: fontStack.body, fontSize: 12, color: "#7a2e1d" }}>
            ⏱ {result.deadlines.join(" · ")}
          </div>
        )}
      </div>
    </div>
  );
}
