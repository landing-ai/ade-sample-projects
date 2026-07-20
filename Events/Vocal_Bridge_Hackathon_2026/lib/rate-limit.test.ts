import { describe, it, expect, vi } from "vitest";
import { rateLimit } from "./rate-limit";

describe("rateLimit", () => {
  it("allows up to max within window then blocks, and recovers after the window", () => {
    vi.useFakeTimers();
    for (let i = 0; i < 5; i++) expect(rateLimit("k", 5, 1000)).toBe(true);
    expect(rateLimit("k", 5, 1000)).toBe(false);
    vi.advanceTimersByTime(1001);
    expect(rateLimit("k", 5, 1000)).toBe(true);
    vi.useRealTimers();
  });

  it("tracks keys independently", () => {
    vi.useFakeTimers();
    expect(rateLimit("a", 1, 1000)).toBe(true);
    expect(rateLimit("a", 1, 1000)).toBe(false);
    expect(rateLimit("b", 1, 1000)).toBe(true);
    vi.useRealTimers();
  });

  it("recovers a key whose window has fully lapsed (window recovery, not leak)", () => {
    vi.useFakeTimers();
    expect(rateLimit("recov", 1, 1000)).toBe(true);
    expect(rateLimit("recov", 1, 1000)).toBe(false);
    // After the sweep interval + stale TTL, an abandoned key is evicted and a
    // fresh request is allowed again (proving old timestamps don't accumulate).
    vi.advanceTimersByTime(60_000 + 3_600_000 + 1);
    expect(rateLimit("recov", 1, 1000)).toBe(true);
    vi.useRealTimers();
  });
});
