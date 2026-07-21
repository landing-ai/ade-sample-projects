import { describe, it, expect } from "vitest";
import { shouldRelease, type ReleaseInputs } from "./hold-decision";

const base: ReleaseInputs = {
  fetchDone: false,
  newAgentTurns: 0,
  newUserTurns: 0,
  graceElapsed: false,
  maxHoldElapsed: false,
};

describe("shouldRelease", () => {
  it("never releases before the answer has arrived", () => {
    expect(shouldRelease({ ...base, fetchDone: false, graceElapsed: true })).toBe(false);
    // even if the caller has spoken, there is nothing to deliver yet
    expect(shouldRelease({ ...base, fetchDone: false, newUserTurns: 1 })).toBe(false);
  });

  it("fast path: no follow-up asked → deliver once the grace window confirms none is coming", () => {
    // fetch resolved, agent stayed silent, grace not yet elapsed → wait a beat
    expect(shouldRelease({ ...base, fetchDone: true })).toBe(false);
    // grace elapsed, still no follow-up → deliver
    expect(shouldRelease({ ...base, fetchDone: true, graceElapsed: true })).toBe(true);
  });

  it("holds while the agent's follow-up is out and the caller hasn't replied", () => {
    expect(shouldRelease({ ...base, fetchDone: true, newAgentTurns: 1, graceElapsed: true })).toBe(false);
  });

  it("delivers once the caller replies to the follow-up", () => {
    expect(shouldRelease({ ...base, fetchDone: true, newAgentTurns: 1, newUserTurns: 1 })).toBe(true);
  });

  it("caller reply wins even before the grace window elapses", () => {
    expect(shouldRelease({ ...base, fetchDone: true, newAgentTurns: 1, newUserTurns: 1, graceElapsed: false })).toBe(true);
  });

  it("safety cap forces release even mid-follow-up with no reply and no answer", () => {
    expect(shouldRelease({ ...base, maxHoldElapsed: true })).toBe(true);
    expect(shouldRelease({ ...base, fetchDone: true, newAgentTurns: 1, maxHoldElapsed: true })).toBe(true);
  });
});
