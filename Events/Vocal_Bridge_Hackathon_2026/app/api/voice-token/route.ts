import { NextRequest, NextResponse } from "next/server";
import { env } from "@/lib/env";
import { rateLimit } from "@/lib/rate-limit";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  const ip = req.headers.get("x-forwarded-for") ?? "local";
  if (!rateLimit(`voice-token:${ip}`, 10, 60_000)) {
    return NextResponse.json({ error: "Too many requests" }, { status: 429 });
  }
  const { vocalBridgeApiKey, vocalBridgeAgentId } = env();
  if (!vocalBridgeApiKey) {
    return NextResponse.json({ error: "VocalBridge not configured" }, { status: 503 });
  }
  try {
    const res = await fetch("https://vocalbridgeai.com/api/v1/token", {
      method: "POST",
      headers: {
        "X-API-Key": vocalBridgeApiKey,
        "Content-Type": "application/json",
        ...(vocalBridgeAgentId ? { "X-Agent-Id": vocalBridgeAgentId } : {}),
      },
      body: JSON.stringify({ participant_name: "FinePrint user" }),
    });
    if (!res.ok) {
      return NextResponse.json({ error: `token fetch failed (${res.status})` }, { status: 502 });
    }
    return NextResponse.json(await res.json());
  } catch (e) {
    return NextResponse.json({ error: `token fetch error: ${String(e).slice(0, 200)}` }, { status: 502 });
  }
}
