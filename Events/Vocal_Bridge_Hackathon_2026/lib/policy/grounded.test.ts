import { describe, it, expect } from "vitest";
import { GroundedPolicySchema, boxesForRefs, fieldsForPrompt } from "./grounded";

const g = GroundedPolicySchema.parse({
  plan_name: "Test Plan",
  underwriter: "Test Insurer",
  fields: [
    { ref: "b1", kind: "benefit", label: "Trip Cancellation", value: "$1,000", boxes: [{ docId: "d1", page: 1, rect: { l: 0, t: 0, r: 1, b: 0.1 } }] },
    { ref: "t1", kind: "trigger", label: "Trip Delay", value: "12h · $500", boxes: [{ docId: "d1", page: 2, rect: { l: 0, t: 0.3, r: 1, b: 0.33 } }] },
    { ref: "x1", kind: "exclusion", label: "Exclusion", value: "war", boxes: [] },
  ],
});

describe("anti-hallucination grounding", () => {
  it("resolves real refs to their boxes", () => {
    expect(boxesForRefs(g, ["b1"])).toHaveLength(1);
    expect(boxesForRefs(g, ["b1", "t1"])).toHaveLength(2);
  });

  it("IGNORES an invented ref — Claude cannot conjure a box for a clause that doesn't exist", () => {
    // The core guardrail: even if the model returns a made-up ref, it resolves to NO location.
    expect(boxesForRefs(g, ["b1", "TOTALLY_MADE_UP"])).toHaveLength(1);
    expect(boxesForRefs(g, ["nope", "nonexistent"])).toHaveLength(0);
  });

  it("de-duplicates boxes across repeated refs", () => {
    expect(boxesForRefs(g, ["b1", "b1"])).toHaveLength(1);
  });
});

describe("fieldsForPrompt", () => {
  it("exposes refs + values but NEVER boxes to the model (boxes are server-only)", () => {
    const fp = fieldsForPrompt(g);
    expect(JSON.stringify(fp)).not.toContain("rect");
    expect(JSON.stringify(fp)).not.toContain("boxes");
    expect(fp.coverages.map((c) => c.ref)).toEqual(["b1", "t1"]);
    expect(fp.exclusions[0]).toMatchObject({ ref: "x1", text: "war" });
  });
});
