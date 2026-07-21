import { z } from "zod";

// A grounded box: a normalized rect on a specific document page.
export const GroundBoxSchema = z.object({
  docId: z.string(),
  page: z.number(),
  rect: z.object({ l: z.number(), t: z.number(), r: z.number(), b: z.number() }),
});
export type GroundBox = z.infer<typeof GroundBoxSchema>;

export type FieldKind =
  | "benefit"
  | "trigger"
  | "exclusion"
  | "deadline"
  | "pre_existing"
  | "state_override";

// Every atomic grounded fact carries a STABLE `ref`. Claude reasons over these fields and cites
// them by ref — it can only pick refs that exist, so no invented citation can enter the chain.
// The server resolves ref → boxes for the document highlight. This is v1's chunk_ids, made
// first-party and un-hallucinatable.
export const GroundedFieldSchema = z.object({
  ref: z.string(), // e.g. "b3", "t1", "x2", "d1", "s1", "pre"
  kind: z.enum(["benefit", "trigger", "exclusion", "deadline", "pre_existing", "state_override"]),
  label: z.string(),
  value: z.string(),
  boxes: z.array(GroundBoxSchema).default([]),
});
export type GroundedField = z.infer<typeof GroundedFieldSchema>;

export const GroundedPolicySchema = z.object({
  plan_name: z.string().nullish(),
  underwriter: z.string().nullish(),
  fields: z.array(GroundedFieldSchema).default([]),
  incomplete: z.array(z.string()).default([]),
});
export type GroundedPolicy = z.infer<typeof GroundedPolicySchema>;

// What Claude sees: the fields WITHOUT boxes (keeps the prompt lean; boxes are resolved
// server-side from the ref). Values + refs only.
export function fieldsForPrompt(g: GroundedPolicy) {
  return {
    plan_name: g.plan_name ?? null,
    underwriter: g.underwriter ?? null,
    coverages: g.fields
      .filter((f) => f.kind === "benefit" || f.kind === "trigger")
      .map((f) => ({ ref: f.ref, label: f.label, value: f.value })),
    exclusions: g.fields.filter((f) => f.kind === "exclusion").map((f) => ({ ref: f.ref, text: f.value })),
    deadlines: g.fields.filter((f) => f.kind === "deadline").map((f) => ({ ref: f.ref, text: f.value })),
    pre_existing: g.fields.filter((f) => f.kind === "pre_existing").map((f) => ({ ref: f.ref, text: f.value })),
    state_overrides: g.fields.filter((f) => f.kind === "state_override").map((f) => ({ ref: f.ref, text: f.value })),
  };
}

// Resolve a list of refs to their grounded boxes (for enriching an assessment's citations).
export function boxesForRefs(g: GroundedPolicy, refs: string[]): GroundBox[] {
  const byRef = new Map(g.fields.map((f) => [f.ref, f]));
  const out: GroundBox[] = [];
  const seen = new Set<string>();
  for (const ref of refs) {
    const f = byRef.get(ref);
    if (!f) continue;
    for (const b of f.boxes) {
      const key = `${b.docId}:${b.page}:${b.rect.l.toFixed(3)}:${b.rect.t.toFixed(3)}`;
      if (seen.has(key)) continue;
      seen.add(key);
      out.push(b);
    }
  }
  return out;
}
