import { NextRequest, NextResponse } from "next/server";
import fs from "node:fs";
import { parseArtifactPath } from "@/lib/ade/pipeline";

export const runtime = "nodejs";

// Serves one document's cached DPT-3 parse artifact — page dims + flattened blocks (type + per-line
// boxes). Powers "watch it read" and the Anatomy x-ray. Not the markdown (kept server-side).
export async function GET(_req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const p = parseArtifactPath(id);
  if (!fs.existsSync(p)) return NextResponse.json({ error: "no parse artifact for this document" }, { status: 404 });
  try {
    const { pages, blocks } = JSON.parse(fs.readFileSync(p, "utf8"));
    return NextResponse.json({ pages, blocks });
  } catch (e) {
    return NextResponse.json({ error: String(e).slice(0, 200) }, { status: 500 });
  }
}
