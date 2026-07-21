// Turn-taking for delegated voice answers.
//
// VocalBridge speaks a delegated answer the moment we send `agent_response`. When the
// voice agent fills the retrieval wait with a follow-up question, delivering the answer
// as soon as the fetch resolves cuts off the caller (or fakes their reply). To honour
// "finish the follow-up → listen to the caller → then answer", the client HOLDS the
// answer and only releases it on a clean turn boundary.
//
// This is the pure decision at the heart of that hold. Everything else in VoiceRail is
// wiring (timers + transcript counting) that feeds these inputs.

export type ReleaseInputs = {
  /** The retrieved answer has arrived from /api/hotline/turn. */
  fetchDone: boolean;
  /** Agent transcript entries that appeared AFTER the query was delegated (the follow-up). */
  newAgentTurns: number;
  /** Caller transcript entries that appeared AFTER the query was delegated (their reply). */
  newUserTurns: number;
  /** A short grace period has elapsed since the fetch resolved (to let a late follow-up register). */
  graceElapsed: boolean;
  /** Safety cap elapsed — release regardless, to stay well under VocalBridge's 60s fallback. */
  maxHoldElapsed: boolean;
};

/**
 * Decide whether the held answer should be spoken now.
 *
 * Order matters:
 *  1. Safety cap always wins — never risk the 60s platform fallback (which answers from
 *     the voice agent's own knowledge and would hallucinate).
 *  2. No answer yet → never release.
 *  3. Caller has replied since we delegated → they answered the follow-up → deliver.
 *  4. Agent asked a follow-up but caller hasn't replied yet → HOLD and keep listening.
 *  5. No follow-up was asked → deliver as soon as the grace window confirms none is coming
 *     (guards the race where the fetch resolves just before the follow-up registers).
 */
export function shouldRelease(i: ReleaseInputs): boolean {
  if (i.maxHoldElapsed) return true;
  if (!i.fetchDone) return false;
  if (i.newUserTurns > 0) return true;
  if (i.newAgentTurns > 0) return false;
  return i.graceElapsed;
}
