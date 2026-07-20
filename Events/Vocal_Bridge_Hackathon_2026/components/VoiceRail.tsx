"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { VocalBridgeProvider, useVocalBridge, useTranscript, useAIAgent } from "@vocalbridgeai/react";
import { ConnectionState } from "@vocalbridgeai/sdk";
import { BRAND, fontStack, DISCLAIMER, type LoadedPolicy } from "@/lib/brand";
import type { Verdict } from "@/lib/policy/schema";
import type { GroundBox } from "@/lib/policy/grounded";
import { Eyebrow } from "@/components/atoms";
import { shouldRelease } from "@/lib/voice/hold-decision";

// Turn-taking hold (see lib/voice/hold-decision.ts):
const GRACE_MS = 1500; // after the answer arrives, wait this long to see if a follow-up is still coming
const MAX_HOLD_MS = 25000; // safety cap — never hold past this (VocalBridge falls back to its own knowledge at 60s)

const ERROR_COPY: Record<string, string> = {
  MICROPHONE_ERROR: "Allow microphone access to talk to your policy.",
  USAGE_LIMIT_EXCEEDED: "Voice usage limit reached — try the browser voice below.",
  AGENT_NOT_FOUND: "Voice agent isn't active — falling back to browser voice.",
  AGENT_NOT_ACTIVE: "Voice agent isn't active — falling back to browser voice.",
  TOKEN_FETCH_FAILED: "Couldn't start voice (token request failed).",
  CONNECTION_FAILED: "Couldn't connect to the voice agent.",
};

const allBoxes = (a: Verdict | null): GroundBox[] => (a ? a.citations.flatMap((c) => c.boxes) : []);

// --- waveform: the connection lifecycle IS the visual script (CONCEPT §6b) ---
function Waveform({ mode }: { mode: "idle" | "breath" | "alive" }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 3, height: 22 }}>
      {[0, 1, 2, 3, 4].map((i) => (
        <span
          key={i}
          className={mode === "alive" ? "fp-alive" : mode === "breath" ? "fp-breath" : ""}
          style={{
            width: 3,
            height: mode === "idle" ? 6 : 18,
            background: mode === "idle" ? BRAND.grey : BRAND.lime,
            borderRadius: 2,
            transformOrigin: "center",
            animationDelay: `${i * 90}ms`,
          }}
        />
      ))}
    </div>
  );
}

function RailShell({
  title,
  status,
  wave,
  children,
  footer,
}: {
  title: string;
  status: string;
  wave: "idle" | "breath" | "alive";
  children: React.ReactNode;
  footer: React.ReactNode;
}) {
  return (
    <div style={{ background: BRAND.dark, color: BRAND.light, borderRadius: 2, overflow: "hidden" }}>
      <div style={{ padding: "14px 16px", borderBottom: `1px solid ${BRAND.grey}`, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <Eyebrow color={BRAND.lime}>{title}</Eyebrow>
          <div style={{ fontFamily: fontStack.body, fontSize: 11.5, color: BRAND.midGreen, marginTop: 3 }}>{status}</div>
        </div>
        <Waveform mode={wave} />
      </div>
      <div style={{ padding: "14px 16px" }}>{children}</div>
      <div style={{ padding: "10px 16px 14px", borderTop: `1px solid ${BRAND.grey}` }}>{footer}</div>
    </div>
  );
}

// Manual AI-agent delegation that HOLDS the retrieved answer until the caller has replied
// to the voice agent's follow-up. The fetch runs in parallel with the agent's filler, so a
// fast answer (no follow-up) is delivered with no added latency; a slow answer waits for a
// clean turn instead of cutting the caller off. Decision logic: lib/voice/hold-decision.ts.
type HeldTurn = {
  turnId: string;
  baselineUser: number;
  baselineAgent: number;
  fetchDone: boolean;
  graceElapsed: boolean;
  released: boolean;
  reply: string;
  assessment: Verdict | null;
  graceTimer: ReturnType<typeof setTimeout> | null;
  maxTimer: ReturnType<typeof setTimeout> | null;
};

function useHeldDelegation({
  policy,
  onVerdict,
  onHighlight,
}: {
  policy: LoadedPolicy;
  onVerdict: (v: Verdict) => void;
  onHighlight: (boxes: GroundBox[]) => void;
}) {
  const { pendingQuery, respond } = useAIAgent();
  const { transcript } = useTranscript();
  const transcriptRef = useRef(transcript);
  useEffect(() => {
    transcriptRef.current = transcript;
  }, [transcript]);

  const turnRef = useRef<HeldTurn | null>(null);

  const roleCounts = () => {
    let user = 0;
    let agent = 0;
    for (const x of transcriptRef.current) {
      if (x.role === "user") user++;
      else if (x.role === "agent") agent++;
    }
    return { user, agent };
  };

  const releaseNow = useCallback(() => {
    const turn = turnRef.current;
    if (!turn || turn.released) return;
    turn.released = true;
    if (turn.graceTimer) clearTimeout(turn.graceTimer);
    if (turn.maxTimer) clearTimeout(turn.maxTimer);
    // Reveal the grounded verdict + document highlight in lockstep with the SPOKEN answer,
    // not when the fetch resolved — otherwise the page answers before the voice does.
    if (turn.assessment) {
      onVerdict(turn.assessment);
      onHighlight(allBoxes(turn.assessment));
    }
    respond(turn.turnId, turn.reply);
  }, [onVerdict, onHighlight, respond]);

  const evaluate = useCallback(() => {
    const turn = turnRef.current;
    if (!turn || turn.released) return;
    const c = roleCounts();
    if (
      shouldRelease({
        fetchDone: turn.fetchDone,
        newAgentTurns: c.agent - turn.baselineAgent,
        newUserTurns: c.user - turn.baselineUser,
        graceElapsed: turn.graceElapsed,
        maxHoldElapsed: false, // the safety cap fires via maxTimer → releaseNow
      })
    ) {
      releaseNow();
    }
  }, [releaseNow]);

  // Re-check the release decision whenever the transcript moves (follow-up spoken, caller replies).
  useEffect(() => {
    evaluate();
  }, [transcript, evaluate]);

  // Drive each delegated query through the hold state machine.
  useEffect(() => {
    const q = pendingQuery;
    if (!q) return;
    if (turnRef.current && turnRef.current.turnId === q.turnId) return;
    // A new delegation arrived while a prior one was still held — flush it so it can't orphan.
    if (turnRef.current && !turnRef.current.released) releaseNow();

    const c = roleCounts();
    const turn: HeldTurn = {
      turnId: q.turnId,
      baselineUser: c.user,
      baselineAgent: c.agent,
      fetchDone: false,
      graceElapsed: false,
      released: false,
      reply: "Let me pull that up again — could you say that once more?",
      assessment: null,
      graceTimer: null,
      maxTimer: null,
    };
    turnRef.current = turn;
    turn.maxTimer = setTimeout(releaseNow, MAX_HOLD_MS);

    const history = [
      ...transcriptRef.current.map((t) => ({ role: t.role, content: t.text })),
      { role: "user", content: q.query },
    ];
    (async () => {
      try {
        const res = await fetch("/api/hotline/turn", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ policyId: policy.policyId, messages: history }),
        });
        const data = await res.json();
        if (data.reply) turn.reply = data.reply;
        turn.assessment = data.assessment ?? null;
      } catch {
        /* keep the fallback reply */
      }
      if (turn.released) return; // flushed by a newer turn or the safety cap
      turn.fetchDone = true;
      // Grace: if no follow-up has registered yet, wait a beat before delivering so a
      // just-starting follow-up isn't cut off (the original bug).
      turn.graceTimer = setTimeout(() => {
        turn.graceElapsed = true;
        evaluate();
      }, GRACE_MS);
      evaluate();
    })();
  }, [pendingQuery, policy.policyId, releaseNow, evaluate]);

  // Clear timers on unmount.
  useEffect(
    () => () => {
      const turn = turnRef.current;
      if (turn?.graceTimer) clearTimeout(turn.graceTimer);
      if (turn?.maxTimer) clearTimeout(turn.maxTimer);
    },
    []
  );
}

// ---------------- Live VocalBridge ----------------
function LiveInner({
  policy,
  onHighlight,
  onVerdict,
  onSwitch,
}: {
  policy: LoadedPolicy;
  onHighlight: (boxes: GroundBox[]) => void;
  onVerdict: (v: Verdict) => void;
  onSwitch: () => void;
}) {
  const { state, connect, disconnect, isMicrophoneEnabled, toggleMicrophone, error } = useVocalBridge();
  const { transcript } = useTranscript();

  // Delegate policy questions to the hotline brain, holding the answer until the caller has
  // replied to any follow-up the voice agent asks while we fetch (see useHeldDelegation).
  useHeldDelegation({ policy, onVerdict, onHighlight });

  const connected = state === ConnectionState.Connected || state === ConnectionState.WaitingForAgent;
  const wave = state === ConnectionState.Connected ? "alive" : state === ConnectionState.Connecting || state === ConnectionState.WaitingForAgent ? "breath" : "idle";

  return (
    <>
      <RailShell
        title="Talk to your policy · live"
        status={`VocalBridge · ${state}`}
        wave={wave}
        footer={
          <>
            {error && <div style={{ fontFamily: fontStack.body, fontSize: 12, color: "#e8a090", marginBottom: 8 }}>{ERROR_COPY[error.code] ?? error.message}</div>}
            {!connected && state !== ConnectionState.Connecting ? (
              <button onClick={() => connect()} style={{ width: "100%", fontFamily: fontStack.display, fontWeight: 700, fontSize: 15, padding: "12px 0", background: BRAND.lime, color: BRAND.dark, border: "none", cursor: "pointer" }}>
                🎙 Start talking
              </button>
            ) : (
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8 }}>
                <button onClick={() => toggleMicrophone()} style={{ fontFamily: fontStack.display, fontWeight: 700, fontSize: 13, padding: "10px 14px", background: isMicrophoneEnabled ? BRAND.blue : "transparent", color: isMicrophoneEnabled ? BRAND.dark : BRAND.light, border: `1px solid ${BRAND.midGreen}`, cursor: "pointer" }}>
                  {isMicrophoneEnabled ? "Mute" : "Unmute"}
                </button>
                <span style={{ fontFamily: fontStack.body, fontSize: 12, color: BRAND.midGreen }}>{state === ConnectionState.Connecting ? "Connecting…" : "Listening"}</span>
                <button onClick={() => disconnect()} style={{ fontFamily: fontStack.display, fontWeight: 700, fontSize: 12, padding: "8px 14px", background: "transparent", color: "#e8a090", border: "1px solid #e8a090", cursor: "pointer" }}>
                  End
                </button>
              </div>
            )}
          </>
        }
      >
        {transcript.length === 0 ? (
          <div style={{ textAlign: "center", padding: "18px 6px", fontFamily: fontStack.accent, fontStyle: "italic", fontSize: 17, color: BRAND.light, lineHeight: 1.4 }}>
            &ldquo;My flight&apos;s delayed eight hours — what am I covered for?&rdquo;
          </div>
        ) : (
          <div style={{ maxHeight: 150, overflowY: "auto", display: "flex", flexDirection: "column", gap: 8 }}>
            {transcript.map((m, i) => (
              <div key={i} style={{ alignSelf: m.role === "user" ? "flex-end" : "flex-start", maxWidth: "85%", padding: "8px 11px", fontFamily: fontStack.body, fontSize: 13, lineHeight: 1.5, background: m.role === "user" ? BRAND.blue : BRAND.light, color: BRAND.dark, borderRadius: m.role === "user" ? "12px 12px 3px 12px" : "12px 12px 12px 3px" }}>
                {m.text}
              </div>
            ))}
          </div>
        )}
      </RailShell>
      <button onClick={onSwitch} style={{ display: "block", margin: "10px auto 0", background: "none", border: "none", color: BRAND.blue, textDecoration: "underline", fontFamily: fontStack.body, fontSize: 12, cursor: "pointer" }}>
        or type in the browser instead
      </button>
    </>
  );
}

// ---------------- Browser fallback ----------------
function BrowserRail({
  policy,
  voiceAvailable,
  onHighlight,
  onVerdict,
  onUseVoice,
}: {
  policy: LoadedPolicy;
  voiceAvailable: boolean;
  onHighlight: (boxes: GroundBox[]) => void;
  onVerdict: (v: Verdict) => void;
  onUseVoice: () => void;
}) {
  const [transcript, setTranscript] = useState<{ role: "user" | "agent"; content: string }[]>([]);
  const [thinking, setThinking] = useState(false);
  const [listening, setListening] = useState(false);
  const [interim, setInterim] = useState("");
  const [typed, setTyped] = useState("");
  const [speaking, setSpeaking] = useState(false);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const recogRef = useRef<any>(null);
  const transcriptRef = useRef(transcript);
  useEffect(() => {
    transcriptRef.current = transcript;
  }, [transcript]);
  const [srSupported] = useState(
    typeof window !== "undefined" &&
      !!((window as unknown as { SpeechRecognition?: unknown }).SpeechRecognition || (window as unknown as { webkitSpeechRecognition?: unknown }).webkitSpeechRecognition)
  );

  useEffect(() => () => window.speechSynthesis?.cancel(), []);

  const speak = useCallback((text: string) => {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.rate = 1.02;
    u.onstart = () => setSpeaking(true);
    u.onend = () => setSpeaking(false);
    u.onerror = () => setSpeaking(false);
    window.speechSynthesis.speak(u);
  }, []);

  const sendTurn = useCallback(
    async (text: string) => {
      const t = text.trim();
      if (!t) return;
      const next = [...transcriptRef.current, { role: "user" as const, content: t }];
      setTranscript(next);
      setThinking(true);
      try {
        const res = await fetch("/api/hotline/turn", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ policyId: policy.policyId, messages: next }),
        });
        const data = await res.json();
        const reply = data.reply ?? "Let me pull that up again — could you say that once more?";
        setTranscript((prev) => [...prev, { role: "agent", content: reply }]);
        if (data.assessment) {
          onVerdict(data.assessment);
          onHighlight(allBoxes(data.assessment));
        }
        speak(reply);
      } catch {
        setTranscript((prev) => [...prev, { role: "agent", content: "Let me pull that up again — could you say that once more?" }]);
      } finally {
        setThinking(false);
      }
    },
    [policy.policyId, onHighlight, onVerdict, speak]
  );

  const toggleMic = () => {
    if (!srSupported) return;
    if (listening) {
      try {
        recogRef.current?.stop();
      } catch {}
      setListening(false);
      return;
    }
    window.speechSynthesis?.cancel();
    const w = window as unknown as { SpeechRecognition?: new () => unknown; webkitSpeechRecognition?: new () => unknown };
    const SR = w.SpeechRecognition || w.webkitSpeechRecognition;
    if (!SR) return;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const r: any = new SR();
    recogRef.current = r;
    r.lang = "en-US";
    r.interimResults = true;
    r.continuous = false;
    let finalText = "";
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    r.onresult = (ev: any) => {
      let it = "";
      for (let i = ev.resultIndex; i < ev.results.length; i++) {
        const res = ev.results[i];
        if (res.isFinal) finalText += res[0].transcript;
        else it += res[0].transcript;
      }
      setInterim(it || finalText);
    };
    r.onend = () => {
      setListening(false);
      setInterim("");
      if (finalText.trim()) sendTurn(finalText);
    };
    r.onerror = () => {
      setListening(false);
      setInterim("");
    };
    setListening(true);
    r.start();
  };

  const wave = speaking ? "alive" : listening ? "breath" : "idle";
  return (
    <>
      <RailShell
        title="Talk to your policy · browser"
        status={srSupported ? "Browser voice · push to talk or type" : "Browser voice · type your question"}
        wave={wave}
        footer={
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <button onClick={toggleMic} disabled={!srSupported || thinking} title={srSupported ? "Push to talk" : "Mic unavailable — type below"} className={listening ? "fp-pulse" : ""} style={{ width: 44, height: 44, borderRadius: "50%", border: `2px solid ${listening ? BRAND.lime : BRAND.midGreen}`, background: listening ? BRAND.lime : "transparent", color: listening ? BRAND.dark : BRAND.light, fontSize: 18, cursor: srSupported ? "pointer" : "not-allowed", flexShrink: 0 }}>
              🎙
            </button>
            <input value={typed} onChange={(e) => setTyped(e.target.value)} onKeyDown={(e) => e.key === "Enter" && (sendTurn(typed), setTyped(""))} placeholder="Ask about your policy…" style={{ flex: 1, fontFamily: fontStack.body, fontSize: 13, padding: "10px 12px", border: `1px solid ${BRAND.grey}`, background: "#2a2f3a", color: BRAND.light, outline: "none" }} />
            <button onClick={() => (sendTurn(typed), setTyped(""))} disabled={thinking || !typed.trim()} style={{ fontFamily: fontStack.display, fontWeight: 700, fontSize: 13, padding: "10px 14px", background: BRAND.blue, color: BRAND.dark, border: "none", cursor: thinking || !typed.trim() ? "default" : "pointer", opacity: thinking || !typed.trim() ? 0.5 : 1 }}>
              Ask
            </button>
          </div>
        }
      >
        {transcript.length === 0 ? (
          <div style={{ textAlign: "center", padding: "18px 6px", fontFamily: fontStack.accent, fontStyle: "italic", fontSize: 17, color: BRAND.light, lineHeight: 1.4 }}>
            &ldquo;My flight&apos;s delayed eight hours — what am I covered for?&rdquo;
          </div>
        ) : (
          <div style={{ maxHeight: 150, overflowY: "auto", display: "flex", flexDirection: "column", gap: 8 }}>
            {transcript.map((m, i) => (
              <div key={i} style={{ alignSelf: m.role === "user" ? "flex-end" : "flex-start", maxWidth: "85%", padding: "8px 11px", fontFamily: fontStack.body, fontSize: 13, lineHeight: 1.5, background: m.role === "user" ? BRAND.blue : BRAND.light, color: BRAND.dark, borderRadius: m.role === "user" ? "12px 12px 3px 12px" : "12px 12px 12px 3px" }}>
                {m.content}
              </div>
            ))}
            {interim && <div style={{ alignSelf: "flex-end", fontFamily: fontStack.body, fontSize: 13, fontStyle: "italic", color: BRAND.midGreen }}>{interim}…</div>}
            {thinking && <div className="fp-pulse" style={{ fontFamily: fontStack.body, fontSize: 12, color: BRAND.lime }}>Checking your policy…</div>}
          </div>
        )}
      </RailShell>
      {voiceAvailable && (
        <button onClick={onUseVoice} style={{ display: "block", margin: "10px auto 0", background: "none", border: "none", color: BRAND.blue, textDecoration: "underline", fontFamily: fontStack.body, fontSize: 12, cursor: "pointer" }}>
          switch to live VocalBridge voice
        </button>
      )}
      <div style={{ fontFamily: fontStack.body, fontSize: 10.5, color: BRAND.grey, marginTop: 10, textAlign: "center", lineHeight: 1.5 }}>{DISCLAIMER}</div>
    </>
  );
}

export function VoiceRail({
  policy,
  onHighlight,
  onVerdict,
}: {
  policy: LoadedPolicy;
  onHighlight: (boxes: GroundBox[]) => void;
  onVerdict: (v: Verdict) => void;
}) {
  const [voiceEnabled, setVoiceEnabled] = useState<boolean | null>(null);
  const [mode, setMode] = useState<"voice" | "browser">("browser");

  useEffect(() => {
    (async () => {
      try {
        const { enabled } = await (await fetch("/api/voice-enabled")).json();
        setVoiceEnabled(!!enabled);
        setMode(enabled ? "voice" : "browser");
      } catch {
        setVoiceEnabled(false);
        setMode("browser");
      }
    })();
  }, []);

  if (voiceEnabled === null) {
    return <div className="fp-pulse" style={{ fontFamily: fontStack.body, color: BRAND.grey, textAlign: "center", padding: 20 }}>Connecting the voice line…</div>;
  }
  if (voiceEnabled && mode === "voice") {
    return (
      <VocalBridgeProvider options={{ auth: { tokenUrl: "/api/voice-token" } }}>
        <LiveInner policy={policy} onHighlight={onHighlight} onVerdict={onVerdict} onSwitch={() => setMode("browser")} />
      </VocalBridgeProvider>
    );
  }
  return <BrowserRail policy={policy} voiceAvailable={voiceEnabled} onHighlight={onHighlight} onVerdict={onVerdict} onUseVoice={() => setMode("voice")} />;
}
