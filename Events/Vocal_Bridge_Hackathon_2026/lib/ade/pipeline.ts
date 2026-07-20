import fs from "node:fs";
import path from "node:path";
import { db } from "../db";
import { env } from "../env";
import { parseDocumentV2 } from "./parse";
import { extractFieldsV2 } from "./extract";
import { BENEFITS_SCHEMA, CONSTRAINTS_SCHEMA, EXTRACT_PASSES } from "./schemas";
import { collectLeafSpans, spansToBoxes } from "./span-bridge";
import type { GroundBox, ParseBlock, ParseResult, Span } from "./types";
import { GroundedFieldSchema, GroundedPolicySchema, type GroundedField } from "../policy/grounded";

const UPLOAD_DIR = path.join(process.cwd(), "uploads");

// Per-doc parse artifact (markdown + page dims + blocks) cached to disk for the canvas route.
export function parseArtifactPath(docId: string): string {
  return path.join(UPLOAD_DIR, `${docId}-parse.json`);
}

// --- pass-status serialization (ported from v1: overlapping writers must not race) ---
const statusQueue = new Map<string, Promise<void>>();
function serialize<T>(key: string, fn: () => Promise<T>): Promise<T> {
  const prev = statusQueue.get(key) ?? Promise.resolve();
  const result = prev.then(fn, fn);
  statusQueue.set(key, result.then(() => undefined, () => undefined));
  return result;
}
async function setPassStatus(policyId: string, patch: Record<string, string>) {
  await serialize(policyId, async () => {
    const p = await db.policy.findUniqueOrThrow({ where: { id: policyId } });
    const status = { ...JSON.parse(p.passStatus || "{}"), ...patch };
    await db.policy.update({ where: { id: policyId }, data: { passStatus: JSON.stringify(status) } });
  });
}

// All spans beneath an extraction_metadata subtree (every atomic leaf).
function allSpans(metaSubtree: unknown): Span[] {
  return Object.values(collectLeafSpans(metaSubtree)).flat();
}

function triggerValue(t: Record<string, unknown>): string {
  const bits: string[] = [];
  if (typeof t.threshold_hours === "number") bits.push(`${t.threshold_hours}h`);
  if (typeof t.threshold_days === "number") bits.push(`${t.threshold_days}d`);
  if (t.pays) bits.push(String(t.pays));
  return bits.join(" · ") || "See policy";
}

// Build grounded fields for one document from its two extractions + its parse blocks.
function buildDocFields(
  docId: string,
  blocks: ParseBlock[],
  benefits: { extraction: Record<string, unknown>; metadata: unknown },
  constraints: { extraction: Record<string, unknown>; metadata: unknown },
  refSeed: { n: number }
): { fields: GroundedField[]; plan_name?: string | null; underwriter?: string | null } {
  const fields: GroundedField[] = [];
  const boxesFor = (spans: Span[]): GroundBox[] => spansToBoxes(spans, docId, blocks);
  const nextRef = (letter: string) => `${letter}${refSeed.n++}`;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const bMeta = benefits.metadata as any;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const cMeta = constraints.metadata as any;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const bx = benefits.extraction as any;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const cx = constraints.extraction as any;

  for (const [i, b] of (bx.benefits ?? []).entries()) {
    const value = [b.limit_amount, b.per_item_cap].filter(Boolean).join(" · ") || "See policy";
    fields.push(GroundedFieldSchema.parse({
      ref: nextRef("b"), kind: "benefit", label: String(b.name ?? "Benefit"),
      value, boxes: boxesFor(allSpans(bMeta?.benefits?.[i])),
    }));
  }
  for (const [i, t] of (bx.triggers ?? []).entries()) {
    fields.push(GroundedFieldSchema.parse({
      ref: nextRef("t"), kind: "trigger", label: String(t.peril ?? "Trigger"),
      value: triggerValue(t), boxes: boxesFor(allSpans(bMeta?.triggers?.[i])),
    }));
  }
  for (const [i, x] of (cx.exclusions ?? []).entries()) {
    fields.push(GroundedFieldSchema.parse({
      ref: nextRef("x"), kind: "exclusion", label: "Exclusion",
      value: String(x.text ?? ""), boxes: boxesFor(allSpans(cMeta?.exclusions?.[i])),
    }));
  }
  for (const [i, d] of (cx.deadlines ?? []).entries()) {
    const value = [d.rule, typeof d.days === "number" ? `${d.days} days` : null].filter(Boolean).join(" — ");
    fields.push(GroundedFieldSchema.parse({
      ref: nextRef("d"), kind: "deadline", label: "Deadline",
      value, boxes: boxesFor(allSpans(cMeta?.deadlines?.[i])),
    }));
  }
  if (cx.pre_existing && (cx.pre_existing.lookback_days != null || cx.pre_existing.waiver_conditions)) {
    const pe = cx.pre_existing;
    const value = [
      pe.lookback_days != null ? `${pe.lookback_days}-day lookback` : null,
      pe.waiver_conditions ? `waiver: ${pe.waiver_conditions}` : null,
    ].filter(Boolean).join(" · ");
    fields.push(GroundedFieldSchema.parse({
      ref: nextRef("pre"), kind: "pre_existing", label: "Pre-existing conditions",
      value: value || "See policy", boxes: boxesFor(allSpans(cMeta?.pre_existing)),
    }));
  }
  for (const [i, s] of (cx.state_overrides ?? []).entries()) {
    fields.push(GroundedFieldSchema.parse({
      ref: nextRef("s"), kind: "state_override", label: "State override",
      value: String(s.text ?? ""), boxes: boxesFor(allSpans(cMeta?.state_overrides?.[i])),
    }));
  }
  return { fields, plan_name: bx.plan_name ?? null, underwriter: bx.underwriter ?? null };
}

export async function runExtractionV2(
  policyId: string,
  files: { buffer: Buffer; mimeType: string; filename: string }[]
): Promise<void> {
  try {
    await setPassStatus(policyId, Object.fromEntries(EXTRACT_PASSES.map((p) => [p.id, "pending"])));
    fs.mkdirSync(UPLOAD_DIR, { recursive: true });

    // 1. Parse each doc with DPT-3, cache its artifact, record the doc.
    await setPassStatus(policyId, { parse: "running" });
    let pageOffset = 0;
    const parsed: { docId: string; parse: ParseResult }[] = [];
    for (const f of files) {
      const doc = await db.policyDoc.create({
        data: { filename: f.filename, mimeType: f.mimeType, filePath: "", policyId, pageOffset },
      });
      const safeName = path.basename(f.filename);
      const filePath = path.join(UPLOAD_DIR, `${doc.id}-${safeName}`);
      fs.writeFileSync(filePath, f.buffer);
      const parse = await parseDocumentV2(f);
      fs.writeFileSync(parseArtifactPath(doc.id), JSON.stringify({ markdown: parse.markdown, pages: parse.pages, blocks: parse.blocks }));
      await db.policyDoc.update({ where: { id: doc.id }, data: { filePath, pageCount: parse.pageCount } });
      parsed.push({ docId: doc.id, parse });
      pageOffset += parse.pageCount;
    }
    await setPassStatus(policyId, { parse: "done" });

    // 2. Extract both concern-scoped schemas per doc (spans align with that doc's markdown).
    await setPassStatus(policyId, { benefits: "running", constraints: "running" });
    const refSeed = { n: 1 };
    const allFields: GroundedField[] = [];
    const failed: string[] = [];
    let planName: string | null = null;
    let underwriter: string | null = null;

    for (const { docId, parse } of parsed) {
      let benefits: { extraction: Record<string, unknown>; metadata: unknown } = { extraction: {}, metadata: {} };
      let constraints: { extraction: Record<string, unknown>; metadata: unknown } = { extraction: {}, metadata: {} };
      try {
        const r = await extractFieldsV2(parse.markdown, BENEFITS_SCHEMA);
        benefits = { extraction: r.extraction, metadata: r.metadata };
      } catch (e) { console.error("benefits extract failed:", e); failed.push("Benefits"); }
      try {
        const r = await extractFieldsV2(parse.markdown, CONSTRAINTS_SCHEMA);
        constraints = { extraction: r.extraction, metadata: r.metadata };
      } catch (e) { console.error("constraints extract failed:", e); failed.push("Constraints"); }

      const built = buildDocFields(docId, parse.blocks, benefits, constraints, refSeed);
      allFields.push(...built.fields);
      planName = planName ?? built.plan_name ?? null;
      underwriter = underwriter ?? built.underwriter ?? null;
    }
    await setPassStatus(policyId, {
      benefits: failed.includes("Benefits") ? "failed" : "done",
      constraints: failed.includes("Constraints") ? "failed" : "done",
    });

    // 3. Assemble + persist the grounded policy.
    const grounded = GroundedPolicySchema.parse({
      plan_name: planName, underwriter, fields: allFields, incomplete: [...new Set(failed)],
    });
    await db.policy.update({
      where: { id: policyId },
      data: { extracted: JSON.stringify(grounded), name: planName, incomplete: JSON.stringify([...new Set(failed)]) },
    });

    if (env().deleteRawPdfs) {
      const docs = await db.policyDoc.findMany({ where: { policyId } });
      for (const d of docs) if (d.filePath && fs.existsSync(d.filePath)) fs.unlinkSync(d.filePath);
      await db.policyDoc.updateMany({ where: { policyId }, data: { filePath: "" } });
    }
  } catch (e) {
    console.error("v2 extraction pipeline failed:", e);
    await setPassStatus(policyId, Object.fromEntries(EXTRACT_PASSES.map((p) => [p.id, "failed"])));
  }
}
