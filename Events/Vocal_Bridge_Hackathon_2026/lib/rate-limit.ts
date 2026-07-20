// In-memory sliding-window rate limiter. Process-local — fine for a personal,
// single-instance app; swap for a shared store if ever deployed multi-instance.
//
// Note on keys: callers key this on a client-supplied signal (x-forwarded-for),
// which is spoofable. This limiter is a best-effort abuse guard for a local-first,
// no-auth app — not a security boundary. The stale sweep below bounds memory even
// under key-rotation, so a spoofing client can't grow the map without limit.
const hits = new Map<string, number[]>();

let lastSweep = 0;
const SWEEP_INTERVAL_MS = 60_000;
const STALE_MS = 3_600_000; // drop keys untouched for 1h (>> any window we use)

export function rateLimit(key: string, max: number, windowMs: number): boolean {
  const now = Date.now();

  // Periodically evict keys nobody has touched recently, so distinct/rotated
  // keys can't accumulate unbounded entries in the map.
  if (now - lastSweep > SWEEP_INTERVAL_MS) {
    lastSweep = now;
    for (const [k, ts] of hits) {
      if (ts.length === 0 || ts[ts.length - 1] < now - STALE_MS) hits.delete(k);
    }
  }

  const arr = (hits.get(key) ?? []).filter((t) => now - t < windowMs);
  if (arr.length >= max) {
    hits.set(key, arr);
    return false;
  }
  arr.push(now);
  hits.set(key, arr);
  return true;
}
