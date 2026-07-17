"use client";

import { BRAND, fontStack } from "@/lib/brand";
import type { GroundBox, GroundedField } from "@/lib/policy/grounded";
import type { Verdict } from "@/lib/policy/schema";
import { Eyebrow } from "@/components/atoms";
import { VerdictCard } from "@/components/VerdictCard";

export type MapTab = "benefits" | "anatomy" | "verdict";

const KIND_LABEL: Record<string, string> = {
  benefit: "Benefits",
  trigger: "Triggers & thresholds",
  exclusion: "Exclusions",
  deadline: "Deadlines",
  pre_existing: "Pre-existing",
  state_override: "State overrides",
};
const ORDER = ["benefit", "trigger", "exclusion", "deadline", "pre_existing", "state_override"];

const ANATOMY_LEGEND: { type: string; label: string; color: string }[] = [
  { type: "text", label: "Text", color: BRAND.blue },
  { type: "table", label: "Tables", color: BRAND.lightGreen },
  { type: "figure", label: "Figures", color: BRAND.lavender },
  { type: "attestation", label: "Attestation", color: "#d8b4fe" },
  { type: "marginalia", label: "Marginalia", color: BRAND.grey },
  { type: "scan_code", label: "Codes", color: "#f0a58a" },
];

export function CoverageMap({
  fields,
  tab,
  onTab,
  verdict,
  onHover,
  onSelect,
}: {
  fields: GroundedField[];
  tab: MapTab;
  onTab: (tab: MapTab) => void;
  /** The latest grounded answer, if any — surfaced as its own tab so the voice rail never moves. */
  verdict: Verdict | null;
  onHover: (boxes: GroundBox[] | null) => void;
  onSelect: (boxes: GroundBox[]) => void;
}) {
  const grouped = ORDER.map((kind) => ({ kind, items: fields.filter((f) => f.kind === kind) })).filter(
    (g) => g.items.length
  );

  const tabs: { id: MapTab; label: string }[] = [
    { id: "benefits", label: "Benefits" },
    { id: "anatomy", label: "Anatomy" },
  ];
  if (verdict) tabs.push({ id: "verdict", label: "Answer" });

  return (
    <div style={{ background: "#fffef8", border: `1px solid ${BRAND.midGreen}`, borderRadius: 2 }}>
      <div style={{ display: "flex", borderBottom: `1px solid ${BRAND.midGreen}` }}>
        {tabs.map((t) => {
          const active = t.id === tab;
          return (
            <button
              key={t.id}
              onClick={() => onTab(t.id)}
              style={{
                flex: 1,
                fontFamily: fontStack.display,
                fontWeight: 700,
                fontSize: 12,
                letterSpacing: "0.08em",
                textTransform: "uppercase",
                padding: "10px 0",
                border: "none",
                cursor: "pointer",
                background: active ? BRAND.dark : "transparent",
                color: active ? BRAND.lime : BRAND.grey,
              }}
            >
              {t.label}
            </button>
          );
        })}
      </div>

      <div style={{ maxHeight: "calc(100vh - 470px)", overflowY: "auto", padding: "10px 12px 14px" }}>
        {tab === "verdict" && verdict ? (
          <VerdictCard result={verdict} onCite={onSelect} />
        ) : tab === "anatomy" ? (
          <div>
            <div style={{ fontFamily: fontStack.body, fontSize: 12, color: BRAND.grey, lineHeight: 1.5, margin: "4px 2px 12px" }}>
              DPT-3&apos;s raw structure — every block the parser found, colored by type, drawn on the page.
            </div>
            {ANATOMY_LEGEND.map((l) => (
              <div key={l.type} style={{ display: "flex", alignItems: "center", gap: 8, padding: "5px 2px", fontFamily: fontStack.body, fontSize: 13, color: BRAND.dark }}>
                <span style={{ width: 14, height: 14, background: l.color, borderRadius: 2, flexShrink: 0 }} />
                {l.label}
              </div>
            ))}
          </div>
        ) : (
          grouped.map((g) => (
            <div key={g.kind} style={{ marginBottom: 12 }}>
              <div style={{ margin: "6px 2px 4px" }}>
                <Eyebrow>{KIND_LABEL[g.kind] ?? g.kind}</Eyebrow>
              </div>
              {g.items.map((f) => (
                <button
                  key={f.ref}
                  onMouseEnter={() => onHover(f.boxes)}
                  onMouseLeave={() => onHover(null)}
                  onClick={() => onSelect(f.boxes)}
                  disabled={!f.boxes.length}
                  title={f.boxes.length ? "Show on the page" : "No location grounded"}
                  style={{
                    display: "block",
                    width: "100%",
                    textAlign: "left",
                    background: "transparent",
                    border: "none",
                    borderLeft: `3px solid ${f.boxes.length ? BRAND.lime : BRAND.midGreen}`,
                    padding: "6px 10px",
                    marginBottom: 3,
                    cursor: f.boxes.length ? "pointer" : "default",
                    fontFamily: fontStack.body,
                  }}
                >
                  <div style={{ fontSize: 13, fontWeight: 500, color: BRAND.dark, lineHeight: 1.35 }}>
                    {f.kind === "benefit" || f.kind === "trigger" ? f.label : f.value}
                  </div>
                  {(f.kind === "benefit" || f.kind === "trigger") && (
                    <div style={{ fontSize: 12, color: BRAND.grey, marginTop: 1 }}>{f.value}</div>
                  )}
                </button>
              ))}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
