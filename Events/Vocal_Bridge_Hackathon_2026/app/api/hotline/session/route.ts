import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  const { policyId, channel, transcript } = await req.json();
  if (!policyId || (channel !== "browser" && channel !== "vocalbridge")) {
    return NextResponse.json({ error: "policyId and valid channel required" }, { status: 400 });
  }
  try {
    const session = await db.hotlineSession.create({
      data: { policyId, channel, transcript: JSON.stringify(transcript ?? []) },
    });
    return NextResponse.json({ id: session.id });
  } catch (e) {
    return NextResponse.json({ error: `could not save session: ${String(e).slice(0, 200)}` }, { status: 500 });
  }
}
