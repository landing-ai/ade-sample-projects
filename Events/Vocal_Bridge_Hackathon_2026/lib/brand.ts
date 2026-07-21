import type { GroundedPolicy } from "@/lib/policy/grounded";

export const BRAND = {
  dark: "#1F232C",
  light: "#E8E9D6",
  midGreen: "#b0aea5",
  lightGreen: "#C7DCCD",
  lime: "#DBFF9B",
  lavender: "#E2E4F9",
  blue: "#ABC2EB",
  grey: "#797665",
} as const;

export const fontStack = {
  display: "'Urbanist', 'DM Sans', sans-serif",
  body: "'Inter', 'DM Sans', sans-serif",
  accent: "'Playfair Display', Georgia, serif",
} as const;

export const DISCLAIMER =
  "Informational pre-check only — not insurance advice and not a claims decision. Your insurer makes all final determinations." as const;

export type PolicyDocRef = { id: string; filename: string; pageCount: number };

export type LoadedPolicy = {
  policyId: string;
  docNames: string[];
  docs: PolicyDocRef[];
  extracted: GroundedPolicy;
  savedAt: string;
};
