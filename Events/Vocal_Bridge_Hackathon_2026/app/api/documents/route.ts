import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { env } from "@/lib/env";
import { runExtractionV2 } from "@/lib/ade/pipeline";
import { EXTRACT_PASSES } from "@/lib/ade/schemas";
import { rateLimit } from "@/lib/rate-limit";

export const runtime = "nodejs";

const OK_TYPES = ["application/pdf", "image/png", "image/jpeg", "image/webp"];
const MAX_BYTES = 8 * 1024 * 1024;

export async function POST(req: NextRequest) {
  const ip = req.headers.get("x-forwarded-for") ?? "local";
  if (!rateLimit(`documents:${ip}`, 5, 60_000)) {
    return NextResponse.json({ error: "Too many requests" }, { status: 429 });
  }
  if (!env().visionAgentApiKey) {
    return NextResponse.json(
      { error: "Extraction is not configured: set VISION_AGENT_API_KEY in fineprint/.env." },
      { status: 503 }
    );
  }
  const form = await req.formData();
  const uploads = form.getAll("files").filter((f): f is File => f instanceof File);
  if (!uploads.length) return NextResponse.json({ error: "No files uploaded." }, { status: 400 });
  for (const f of uploads) {
    if (!OK_TYPES.includes(f.type))
      return NextResponse.json({ error: `"${f.name}" skipped — PDFs and images only.` }, { status: 400 });
    if (f.size > MAX_BYTES)
      return NextResponse.json({ error: `"${f.name}" skipped — keep files under 8 MB.` }, { status: 400 });
  }
  const files = await Promise.all(
    uploads.map(async (f) => ({ buffer: Buffer.from(await f.arrayBuffer()), mimeType: f.type, filename: f.name }))
  );
  const policy = await db.policy.create({
    data: { passStatus: JSON.stringify(Object.fromEntries(EXTRACT_PASSES.map((p) => [p.id, "pending"]))) },
  });
  runExtractionV2(policy.id, files).catch((e) => console.error("extraction crashed:", e)); // fire and forget; status route reports progress
  return NextResponse.json({ policyId: policy.id }, { status: 202 });
}
