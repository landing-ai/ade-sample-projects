import { NextRequest, NextResponse } from "next/server";
import fs from "node:fs";
import { db } from "@/lib/db";

export const runtime = "nodejs";

export async function GET(req: NextRequest) {
  const id = new URL(req.url).searchParams.get("id");
  const policy = await db.policy.findFirst({
    // With ?id= reopen a specific past policy; otherwise the most recent one.
    where: id ? { id } : { extracted: { not: "" } },
    orderBy: { createdAt: "desc" },
    include: { docs: true },
  });
  if (!policy || !policy.extracted) return NextResponse.json(null);
  return NextResponse.json({
    policyId: policy.id,
    docNames: policy.docs.map((d) => d.filename),
    docs: policy.docs
      .slice()
      .sort((a, b) => a.pageOffset - b.pageOffset)
      .map((d) => ({ id: d.id, filename: d.filename, pageCount: d.pageCount ?? 1 })),
    extracted: JSON.parse(policy.extracted),
    savedAt: policy.createdAt.toISOString(),
  });
}

export async function DELETE(req: NextRequest) {
  const id = new URL(req.url).searchParams.get("id");
  if (!id) return NextResponse.json({ error: "id required" }, { status: 400 });
  try {
    const docs = await db.policyDoc.findMany({ where: { policyId: id } });
    for (const d of docs) {
      if (d.filePath) {
        try {
          fs.unlinkSync(d.filePath);
        } catch (e) {
          const err = e as NodeJS.ErrnoException;
          if (err.code !== "ENOENT") throw e;
        }
      }
    }
    await db.policy.delete({ where: { id } }); // cascades to docs/chunks/sessions
    return NextResponse.json({ ok: true });
  } catch (e) {
    const err = e as any;
    if (err.code === "P2025") {
      return NextResponse.json({ error: "not found" }, { status: 404 });
    }
    console.error("delete failed:", e);
    return NextResponse.json({ error: "delete failed" }, { status: 500 });
  }
}
