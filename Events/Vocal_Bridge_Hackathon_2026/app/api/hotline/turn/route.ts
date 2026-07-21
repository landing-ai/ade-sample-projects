import { NextRequest, NextResponse } from "next/server";
import { db } from "@/lib/db";
import { chatJSON } from "@/lib/llm/client";
import { buildHotlineSystem } from "@/lib/policy/prompts";
import { HotlineReplySchema } from "@/lib/policy/schema";
import { GroundedPolicySchema, boxesForRefs } from "@/lib/policy/grounded";
import { rateLimit } from "@/lib/rate-limit";

export const runtime = "nodejs";

type Turn = { role: "user" | "agent"; content: string };

export async function POST(req: NextRequest) {
  const ip = req.headers.get("x-forwarded-for") ?? "local";
  if (!rateLimit(`hotline:${ip}`, 20, 60_000)) {
    return NextResponse.json({ error: "Too many requests" }, { status: 429 });
  }
  const { policyId, messages } = await req.json();
  const policy = await db.policy.findUnique({ where: { id: policyId } });
  if (!policy?.extracted) {
    return NextResponse.json({ error: "policy not found" }, { status: 404 });
  }
  const grounded = GroundedPolicySchema.parse(JSON.parse(policy.extracted));
  try {
    const result = await chatJSON({
      system: buildHotlineSystem(grounded),
      messages: ((messages ?? []) as Turn[]).map((m) => ({
        role: (m.role === "agent" ? "assistant" : "user") as "assistant" | "user",
        content: String(m.content),
      })),
      maxTokens: 2048,
      schema: HotlineReplySchema,
    });
    // Resolve grounded refs → document line boxes (the span bridge, server-side). Claude never
    // sees or invents boxes; it can only pick refs that exist.
    if (result.assessment) {
      for (const c of result.assessment.citations) {
        c.boxes = boxesForRefs(grounded, c.refs);
      }
    }
    return NextResponse.json(result);
  } catch {
    return NextResponse.json({
      reply: "Sorry — let me pull that up again. Could you say that once more?",
      assessment: null,
    });
  }
}
