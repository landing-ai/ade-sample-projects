import { NextResponse } from "next/server";
import { env } from "@/lib/env";

export const runtime = "nodejs";

// Reports key presence only — never the key itself.
export async function GET() {
  return NextResponse.json({ enabled: !!env().vocalBridgeApiKey });
}
