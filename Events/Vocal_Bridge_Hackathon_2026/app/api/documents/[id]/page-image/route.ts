import { NextRequest, NextResponse } from "next/server";
import fs from "node:fs";
import { db } from "@/lib/db";
import { pageCachePath, renderPdfPageToPng } from "@/lib/pdf-render";

export const runtime = "nodejs";

export async function GET(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const page = parseInt(new URL(req.url).searchParams.get("page") ?? "", 10);
  if (!Number.isInteger(page) || page < 1) {
    return NextResponse.json({ error: "valid page query param required" }, { status: 400 });
  }
  const doc = await db.policyDoc.findUnique({ where: { id } });
  if (!doc) return NextResponse.json({ error: "document not found" }, { status: 404 });
  if (!doc.filePath || !fs.existsSync(doc.filePath)) {
    // Raw PDF was deleted (privacy toggle) — visual grounding unavailable.
    return NextResponse.json({ error: "source document no longer stored" }, { status: 410 });
  }

  const cachePath = pageCachePath(id, page);
  try {
    if (!fs.existsSync(cachePath)) {
      await renderPdfPageToPng(doc.filePath, page, cachePath);
    }
    const png = fs.readFileSync(cachePath);
    return new NextResponse(new Uint8Array(png), {
      headers: { "Content-Type": "image/png", "Cache-Control": "private, max-age=86400" },
    });
  } catch (e) {
    return NextResponse.json({ error: String(e).slice(0, 200) }, { status: 500 });
  }
}
