import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { chatJSON } from "@/lib/llm/client";
import { VerdictSchema } from "@/lib/policy/schema";
import { buildPrecheckSystem } from "@/lib/policy/prompts";
import { GroundedPolicySchema, boxesForRefs } from "@/lib/policy/grounded";
import { rateLimit } from "@/lib/rate-limit";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  const ip = req.headers.get("x-forwarded-for") ?? "local";
  if (!rateLimit(`precheck:${ip}`, 20, 60_000)) {
    return NextResponse.json({ error: "Too many requests" }, { status: 429 });
  }
  const { policyId, situation } = await req.json();
  if (!policyId || !situation?.trim()) {
    return NextResponse.json({ error: "policyId and situation required" }, { status: 400 });
  }
  const policy = await db.policy.findUnique({ where: { id: policyId } });
  if (!policy?.extracted) {
    return NextResponse.json({ error: "policy not found" }, { status: 404 });
  }
  const grounded = GroundedPolicySchema.parse(JSON.parse(policy.extracted));
  try {
    const verdict = await chatJSON({
      system: buildPrecheckSystem(grounded),
      messages: [{ role: "user", content: `Traveler's situation:\n${situation.trim()}` }],
      maxTokens: 2048,
      schema: VerdictSchema,
    });
    for (const c of verdict.citations) c.boxes = boxesForRefs(grounded, c.refs);
    return NextResponse.json(verdict);
  } catch (e) {
    return NextResponse.json(
      { error: `The assessment engine hit a snag: ${String(e).slice(0, 200)}` },
      { status: 422 }
    );
  }
}
