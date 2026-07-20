"use client";

import { type ReactNode } from "react";
import { BRAND, fontStack } from "@/lib/brand";

export function Eyebrow({ children, color = BRAND.grey }: { children: ReactNode; color?: string }) {
  return (
    <div style={{ fontFamily: fontStack.display, fontWeight: 700, fontSize: 11, letterSpacing: "0.18em", textTransform: "uppercase", color }}>
      {children}
    </div>
  );
}

export const VERDICT_STYLES = {
  likely_covered: { label: "Likely covered", bg: BRAND.lime, fg: BRAND.dark },
  likely_not_covered: { label: "Likely not covered", bg: BRAND.dark, fg: BRAND.light },
  it_depends: { label: "It depends", bg: BRAND.lavender, fg: BRAND.dark },
  need_more_info: { label: "Need more info", bg: BRAND.blue, fg: BRAND.dark },
} as const;

export const ROLE_STYLES = {
  supports: { label: "Supports", color: "#3d5c34", bg: BRAND.lightGreen },
  limits: { label: "Limits", color: "#4a4f7a", bg: BRAND.lavender },
  excludes: { label: "Exclusion", color: BRAND.light, bg: BRAND.dark },
  defines: { label: "Definition", color: BRAND.dark, bg: BRAND.blue },
} as const;
