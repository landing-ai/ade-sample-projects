import { NextResponse } from "next/server";
import { db } from "@/lib/db";

export const runtime = "nodejs";

// The library: every policy ever read, most recent first. Parse artifacts and
// uploaded files persist on disk, so any of these can be reopened and used again.
export async function GET() {
  const policies = await db.policy.findMany({
    where: { extracted: { not: "" } },
    orderBy: { createdAt: "desc" },
    include: { docs: true },
  });
  return NextResponse.json(
    policies.map((p) => {
      let planName: string | null = null;
      let fieldCount = 0;
      try {
        const e = JSON.parse(p.extracted);
        planName = e.plan_name ?? null;
        fieldCount = Array.isArray(e.fields) ? e.fields.length : 0;
      } catch {
        /* a malformed row still lists by its filenames */
      }
      return {
        policyId: p.id,
        planName,
        fieldCount,
        docNames: p.docs.map((d) => d.filename),
        pageCount: p.docs.reduce((n, d) => n + (d.pageCount ?? 1), 0),
        savedAt: p.createdAt.toISOString(),
      };
    })
  );
}
