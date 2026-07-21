"use client";

import { useEffect, useRef, useState } from "react";
import { BRAND, fontStack, type LoadedPolicy } from "@/lib/brand";
import type { GroundBox } from "@/lib/policy/grounded";
import type { Verdict } from "@/lib/policy/schema";
import { UploadScreen } from "@/components/UploadScreen";
import { DocumentStage, type StageHighlight } from "@/components/DocumentStage";
import { CoverageMap, type MapTab } from "@/components/CoverageMap";
import { VoiceRail } from "@/components/VoiceRail";

export default function Home() {
  const [policy, setPolicy] = useState<LoadedPolicy | null>(null);
  const [replacing, setReplacing] = useState(false);
  const [boot, setBoot] = useState(true);
  const [reading, setReading] = useState(false);
  const [mapTab, setMapTab] = useState<MapTab>("benefits");
  const [verdict, setVerdict] = useState<Verdict | null>(null);
  const [highlight, setHighlight] = useState<StageHighlight>(null);
  const [spotlight, setSpotlight] = useState<GroundBox[] | null>(null);
  const anatomy = mapTab === "anatomy";
  const hlToken = useRef(0);
  const readTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const saved = await (await fetch("/api/policy")).json();
        if (saved?.extracted) {
          setPolicy(saved);
          playRead();
        }
      } catch {
        /* no saved policy */
      } finally {
        setBoot(false);
      }
    })();
    return () => {
      if (readTimer.current) clearTimeout(readTimer.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const playRead = () => {
    setReading(true);
    if (readTimer.current) clearTimeout(readTimer.current);
    readTimer.current = setTimeout(() => setReading(false), 1600);
  };

  // Loads a policy into the stage — used both for a fresh upload and for
  // reopening one from history. Never discards the previous one; everything
  // read stays in the library.
  const loadPolicy = (p: LoadedPolicy) => {
    setPolicy(p);
    setReplacing(false);
    setHighlight(null);
    setSpotlight(null);
    setVerdict(null);
    setMapTab("benefits");
    playRead();
  };

  // A grounded answer arrived from the voice/browser rail — surface it in its own
  // tab (leaving the voice widget exactly where it is) and switch to it.
  const onVerdict = (v: Verdict) => {
    setVerdict(v);
    setMapTab("verdict");
  };

  const onReady = loadPolicy;

  const pickPolicy = async (id: string) => {
    try {
      const p = await (await fetch(`/api/policy?id=${encodeURIComponent(id)}`)).json();
      if (p?.extracted) loadPolicy(p as LoadedPolicy);
    } catch {
      /* leave the current view in place if the reopen fails */
    }
  };

  const lightUp = (boxes: GroundBox[]) => {
    if (!boxes.length) return;
    hlToken.current += 1;
    setHighlight({ boxes, token: hlToken.current });
  };

  // Non-destructive: show the upload screen but keep the current policy loaded,
  // so the user can back out and keep using the same document.
  const beginReplace = () => setReplacing(true);

  return (
    <div style={{ minHeight: "100vh", background: BRAND.light, display: "flex", flexDirection: "column" }}>
      <header style={{ background: BRAND.dark, color: BRAND.light, padding: "16px 24px" }}>
        <div style={{ maxWidth: 1320, margin: "0 auto", display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12, flexWrap: "wrap" }}>
          <div style={{ display: "flex", alignItems: "baseline", gap: 14, flexWrap: "wrap" }}>
            <div style={{ fontFamily: fontStack.display, fontWeight: 800, fontSize: 26, letterSpacing: "-0.02em" }}>
              Fine<span style={{ color: BRAND.lime }}>Print</span>
            </div>
            <div style={{ fontFamily: fontStack.accent, fontStyle: "italic", fontSize: 15, color: BRAND.midGreen }}>
              Talk to your policy. Watch it answer.
            </div>
          </div>
          {policy && !replacing && (
            <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
              <button onClick={beginReplace} style={{ fontFamily: fontStack.body, fontSize: 12, padding: "8px 12px", background: "transparent", color: BRAND.midGreen, border: `1px solid ${BRAND.grey}`, cursor: "pointer" }}>
                Replace policy
              </button>
            </div>
          )}
        </div>
      </header>

      <main style={{ maxWidth: 1320, margin: "0 auto", padding: "18px 24px 32px", width: "100%", boxSizing: "border-box", flex: 1 }}>
        {boot ? (
          <div className="fp-pulse" style={{ textAlign: "center", paddingTop: 80, fontFamily: fontStack.display, fontWeight: 700, color: BRAND.grey }}>
            Looking for your policy…
          </div>
        ) : !policy || replacing ? (
          <UploadScreen
            onReady={onReady}
            onCancel={policy ? () => setReplacing(false) : undefined}
            onPick={pickPolicy}
            currentPolicyId={policy?.policyId ?? null}
          />
        ) : (
          <div className="fp-stage-grid" style={{ display: "grid", gridTemplateColumns: "1fr 380px", gap: 20, alignItems: "start" }}>
            <DocumentStage docs={policy.docs} reading={reading} anatomy={anatomy} highlight={highlight} spotlight={spotlight} />
            <div className="fp-rail" style={{ position: "sticky", top: 18, display: "flex", flexDirection: "column", gap: 16, maxHeight: "calc(100vh - 40px)" }}>
              <VoiceRail policy={policy} onHighlight={lightUp} onVerdict={onVerdict} />
              <CoverageMap
                fields={policy.extracted.fields}
                tab={mapTab}
                onTab={setMapTab}
                verdict={verdict}
                onHover={setSpotlight}
                onSelect={lightUp}
              />
            </div>
          </div>
        )}
      </main>

      <footer style={{ borderTop: `1px solid ${BRAND.midGreen}`, padding: "14px 24px 22px" }}>
        <div style={{ maxWidth: 1320, margin: "0 auto", fontFamily: fontStack.body, fontSize: 11, color: BRAND.grey, lineHeight: 1.6 }}>
          DPT-3 reads every page into line-level grounding; Extract v2 builds the typed benefits
          spine; Claude reasons and speaks. Every spoken answer resolves to a real line on the page —
          the voice can&apos;t claim what the page doesn&apos;t show. Personal documents only — not
          customer data.
        </div>
      </footer>
    </div>
  );
}
