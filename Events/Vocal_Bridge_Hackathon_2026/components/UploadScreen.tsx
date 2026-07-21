"use client";

import { useEffect, useState } from "react";
import { BRAND, fontStack, type LoadedPolicy } from "@/lib/brand";
import { Eyebrow } from "@/components/atoms";
import { EXTRACT_PASSES } from "@/lib/ade/schemas";

type PolicySummary = {
  policyId: string;
  planName: string | null;
  fieldCount: number;
  docNames: string[];
  pageCount: number;
  savedAt: string;
};

export function UploadScreen({
  onReady,
  onCancel,
  onPick,
  currentPolicyId,
}: {
  onReady: (policy: LoadedPolicy) => void;
  /** When present, a policy is already loaded — offer a way back without uploading. */
  onCancel?: () => void;
  /** Reopen a previously-read policy by id (parse artifacts persist on disk). */
  onPick?: (policyId: string) => void;
  /** The policy currently on the stage, if any — marked "current" in the library. */
  currentPolicyId?: string | null;
}) {
  const [files, setFiles] = useState<File[]>([]);
  const [passStatus, setPassStatus] = useState<Record<string, string>>({});
  const [extracting, setExtracting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<PolicySummary[]>([]);

  useEffect(() => {
    let live = true;
    fetch("/api/policies")
      .then((r) => r.json())
      .then((list) => {
        if (live && Array.isArray(list)) setHistory(list);
      })
      .catch(() => {
        /* library is optional — the dropzone still works */
      });
    return () => {
      live = false;
    };
  }, []);

  const addFiles = (fileList: FileList) => {
    setError(null);
    const accepted: File[] = [];
    for (const file of Array.from(fileList)) {
      const ok = file.type === "application/pdf" || ["image/png", "image/jpeg", "image/webp"].includes(file.type);
      if (!ok) {
        setError(`"${file.name}" skipped — PDFs and images only.`);
        continue;
      }
      if (file.size > 8 * 1024 * 1024) {
        setError(`"${file.name}" skipped — keep files under 8 MB.`);
        continue;
      }
      accepted.push(file);
    }
    setFiles((prev) => [...prev, ...accepted]);
  };

  const extract = async () => {
    if (!files.length || extracting) return;
    setExtracting(true);
    setError(null);
    const form = new FormData();
    files.forEach((f) => form.append("files", f));
    let policyId: string;
    try {
      const res = await fetch("/api/documents", { method: "POST", body: form });
      if (!res.ok) {
        setError((await res.json()).error ?? "Upload failed.");
        setExtracting(false);
        return;
      }
      ({ policyId } = await res.json());
    } catch {
      setError("Upload failed — is the dev server reachable?");
      setExtracting(false);
      return;
    }
    let fails = 0;
    const poll = setInterval(async () => {
      try {
        const s = await (await fetch(`/api/documents/${policyId}/status`)).json();
        fails = 0;
        setPassStatus(s.passStatus);
        if (s.done) {
          clearInterval(poll);
          setExtracting(false);
          if (!s.extracted || Object.values(s.passStatus).every((v) => v === "failed")) {
            setError("Extraction failed. Check the files are readable policy documents and try again.");
            return;
          }
          // Load the full grounded policy (with docs) so the stage can render pages.
          const full = await (await fetch("/api/policy")).json();
          if (full?.extracted) onReady(full as LoadedPolicy);
        }
      } catch {
        if (++fails >= 3) {
          clearInterval(poll);
          setExtracting(false);
          setError("Lost contact with the extraction job. Reload to check its status.");
        }
      }
    }, 2500);
  };

  const glyph: Record<string, string> = { running: "…", done: "✓", failed: "✕" };
  const color: Record<string, string> = { running: BRAND.grey, done: "#3d5c34", failed: "#a33" };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto" }}>
      {onCancel && (
        <button
          onClick={onCancel}
          disabled={extracting}
          style={{ border: "none", background: "transparent", color: BRAND.grey, cursor: extracting ? "default" : "pointer", fontFamily: fontStack.body, fontSize: 13, padding: 0, marginBottom: 12, opacity: extracting ? 0.5 : 1 }}
        >
          ← Keep my current policy
        </button>
      )}
      <Eyebrow>{onCancel ? "Replace · Your policy" : "Step 1 · Your policy"}</Eyebrow>
      <h2 style={{ fontFamily: fontStack.display, fontWeight: 800, fontSize: 30, color: BRAND.dark, margin: "6px 0 8px", letterSpacing: "-0.01em" }}>
        {onCancel ? "Swap in a new policy." : "Drop it in. Watch it read."}
      </h2>
      <p style={{ fontFamily: fontStack.body, fontSize: 14, color: BRAND.grey, lineHeight: 1.6, margin: "0 0 20px" }}>
        {onCancel
          ? "Upload a different policy to read instead. Your current one stays loaded until the new one finishes — back out any time to keep using it."
          : "Your travel protection plan — the policy PDF, plus any state endorsement. FinePrint reads every page with DPT-3, then you talk to it and watch the exact line light up. Files stay on this machine."}
      </p>

      {/* Native <label htmlFor> opens the file chooser in every browser — no programmatic
          input.click(), which bubbles back to the container and re-fires as a non-user-gesture
          click that WebKit/Safari suppress (dropzone appears dead). */}
      <label
        htmlFor="fp-policy-input"
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          addFiles(e.dataTransfer.files);
        }}
        style={{ display: "block", border: `2px dashed ${BRAND.dark}`, background: "#fffef8", padding: "40px 24px", textAlign: "center", cursor: "pointer", borderRadius: 2 }}
      >
        <div style={{ fontFamily: fontStack.accent, fontStyle: "italic", fontSize: 22, color: BRAND.dark }}>Drop your policy here</div>
        <div style={{ fontFamily: fontStack.body, fontSize: 13, color: BRAND.grey, marginTop: 6 }}>or click to browse · PDF or images · up to 8 MB each</div>
      </label>
      <input id="fp-policy-input" type="file" accept="application/pdf,image/png,image/jpeg,image/webp" multiple style={{ display: "none" }} onChange={(e) => { if (e.target.files) addFiles(e.target.files); e.target.value = ""; }} />

      {files.length > 0 && (
        <div style={{ marginTop: 14 }}>
          {files.map((f, i) => (
            <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: BRAND.lavender, border: `1px solid ${BRAND.blue}`, padding: "8px 12px", marginBottom: 6, fontFamily: fontStack.body, fontSize: 13, color: BRAND.dark }}>
              <span style={{ overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>📄 {f.name}</span>
              {!extracting && (
                <button onClick={() => setFiles((prev) => prev.filter((_, j) => j !== i))} style={{ border: "none", background: "transparent", color: BRAND.grey, cursor: "pointer", fontSize: 14 }} aria-label={`Remove ${f.name}`}>
                  ✕
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {error && <div style={{ marginTop: 12, background: "#f8e8e2", border: "1px solid #c77", padding: "10px 14px", fontFamily: fontStack.body, fontSize: 13, color: "#7a2e1d" }}>{error}</div>}

      <button onClick={extract} disabled={!files.length || extracting} style={{ marginTop: 16, width: "100%", fontFamily: fontStack.display, fontWeight: 700, fontSize: 16, padding: "14px 0", background: !files.length || extracting ? BRAND.midGreen : BRAND.dark, color: !files.length || extracting ? BRAND.dark : BRAND.lime, border: "none", cursor: !files.length || extracting ? "default" : "pointer", borderRadius: 2 }}>
        {extracting ? "Reading every page…" : "Read my policy"}
      </button>

      {Object.keys(passStatus).length > 0 && (
        <div style={{ marginTop: 16, border: `1px solid ${BRAND.midGreen}`, background: "#fffef8", padding: "12px 16px" }}>
          <Eyebrow>DPT-3 pipeline</Eyebrow>
          {EXTRACT_PASSES.map((p) => (
            <div key={p.id} style={{ display: "flex", justifyContent: "space-between", fontFamily: fontStack.body, fontSize: 13, color: BRAND.dark, padding: "5px 0" }}>
              <span>{p.label}</span>
              <span className={passStatus[p.id] === "running" ? "fp-pulse" : ""} style={{ fontWeight: 600, color: color[passStatus[p.id]] || BRAND.grey }}>
                {glyph[passStatus[p.id]] || ""}
                {passStatus[p.id] === "failed" ? " failed" : ""}
              </span>
            </div>
          ))}
        </div>
      )}

      {onPick && history.length > 0 && (
        <div style={{ marginTop: 28 }}>
          <Eyebrow>Recently read · pick up where you left off</Eyebrow>
          <div style={{ marginTop: 8, display: "flex", flexDirection: "column", gap: 8 }}>
            {history.map((h) => {
              const isCurrent = h.policyId === currentPolicyId;
              return (
                <button
                  key={h.policyId}
                  onClick={() => !isCurrent && !extracting && onPick(h.policyId)}
                  disabled={isCurrent || extracting}
                  style={{
                    textAlign: "left",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    gap: 12,
                    background: isCurrent ? BRAND.midGreen : "#fffef8",
                    border: `1px solid ${isCurrent ? BRAND.dark : BRAND.midGreen}`,
                    padding: "10px 14px",
                    borderRadius: 2,
                    cursor: isCurrent || extracting ? "default" : "pointer",
                    fontFamily: fontStack.body,
                    opacity: extracting && !isCurrent ? 0.55 : 1,
                  }}
                >
                  <span style={{ overflow: "hidden" }}>
                    <span style={{ display: "block", fontWeight: 700, fontSize: 14, color: BRAND.dark, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {h.planName || h.docNames[0] || "Untitled policy"}
                    </span>
                    <span style={{ display: "block", fontSize: 12, color: BRAND.grey, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {h.docNames.join(", ") || "—"} · {h.pageCount} page{h.pageCount === 1 ? "" : "s"} · {h.fieldCount} field{h.fieldCount === 1 ? "" : "s"}
                    </span>
                  </span>
                  <span style={{ flexShrink: 0, fontFamily: fontStack.display, fontWeight: 700, fontSize: 12, color: isCurrent ? BRAND.dark : BRAND.grey }}>
                    {isCurrent ? "Current" : "Open →"}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      )}

      <div style={{ marginTop: 18, fontFamily: fontStack.body, fontSize: 11.5, color: BRAND.grey, lineHeight: 1.6 }}>
        Personal use only — upload your own documents, not anyone else&apos;s and not customer data.
        Runs LandingAI DPT-3 Agentic Document Extraction; every extracted clause is grounded to a
        line-level box in your document.
      </div>
    </div>
  );
}
