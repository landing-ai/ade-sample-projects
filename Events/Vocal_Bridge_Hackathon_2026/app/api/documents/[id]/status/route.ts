import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

export const runtime = "nodejs";

export async function GET(_req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const policy = await db.policy.findUnique({ where: { id } });
  if (!policy) return NextResponse.json({ error: "not found" }, { status: 404 });
  const passStatus = JSON.parse(policy.passStatus || "{}") as Record<string, string>;
  const done = Object.values(passStatus).length > 0 &&
    Object.values(passStatus).every((s) => s === "done" || s === "failed");
  return NextResponse.json({
    passStatus,
    done,
    extracted: done && policy.extracted ? JSON.parse(policy.extracted) : null,
    incomplete: policy.incomplete ? JSON.parse(policy.incomplete) : [],
  });
}
