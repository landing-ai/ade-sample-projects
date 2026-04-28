"""
Instant Feedback Demo — Landing AI
Split-screen document verification: W-2 + Paystub
"""

import json
import os
import re
from datetime import date, datetime
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv

# ── Config ───────────────────────────────────────────────────────────────────
load_dotenv(Path(__file__).parent / ".env")

API_KEY     = os.getenv("VISION_AGENT_API_KEY", "")
PARSE_URL   = "https://api.va.landing.ai/v1/ade/parse"
EXTRACT_URL = "https://api.va.landing.ai/v1/ade/extract"

W2_SCHEMA = {
    "type": "object",
    "properties": {
        "w2_employee_name": {
            "type": "string",
            "description": "Employee's full legal name as printed on the W-2 form",
        },
        "w2_employee_ssn": {
            "type": "string",
            "description": "Employee's Social Security Number on the W-2 form",
        },
        "w2_tax_year": {
            "type": "string",
            "description": "The tax year of the W-2 form (4-digit year, e.g. 2023)",
        },
    },
}

PAYSTUB_SCHEMA = {
    "type": "object",
    "properties": {
        "paystub_employee_name": {
            "type": "string",
            "description": "Employee's full name as printed on the paystub",
        },
        "paystub_employee_ssn": {
            "type": "string",
            "description": "Employee's Social Security Number on the paystub",
        },
        "paystub_paydate": {
            "type": "string",
            "description": "Pay date on the paystub (return in YYYY-MM-DD format if possible)",
        },
    },
}

# ── Page setup ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Instant Feedback | Landing AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

/* ── Base ── */
.stApp { background-color: #F6F6EF !important; font-family: 'Inter', sans-serif; }
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: #03221D !important; }
[data-testid="stDecoration"] { display: none; }

/* ── App header bar ── */
.lai-header {
  background: #03221D;
  padding: 14px 32px;
  display: flex; align-items: center; gap: 16px;
  margin: -4rem -4rem 2rem -4rem;
}
.lai-logo { font-family: 'Urbanist', sans-serif; font-size: 18px; font-weight: 800;
             letter-spacing: -0.02em; color: #fff; }
.lai-sep  { width: 1px; height: 20px; background: rgba(255,255,255,0.2); flex-shrink: 0; }
.lai-title { font-family: 'Urbanist', sans-serif; font-size: 12px; font-weight: 600;
              letter-spacing: 0.08em; text-transform: uppercase; color: rgba(255,255,255,0.55); }
.lai-badge {
  margin-left: auto;
  background: rgba(219,255,155,0.12); color: #DBFF9B;
  font-family: 'Urbanist', sans-serif; font-size: 10px; font-weight: 700;
  letter-spacing: 0.07em; text-transform: uppercase;
  padding: 3px 10px; border-radius: 20px; border: 1px solid rgba(219,255,155,0.22);
}

/* ── Typography helpers ── */
.eyebrow {
  font-family: 'Urbanist', sans-serif; font-size: 10px; font-weight: 700;
  letter-spacing: 0.13em; text-transform: uppercase; color: #43574C; margin-bottom: 4px;
}
.sec-title {
  font-family: 'Urbanist', sans-serif; font-size: 22px; font-weight: 700;
  color: #03221D; margin-bottom: 4px; line-height: 1.2;
}
.sec-sub { font-size: 13px; color: #4A5450; margin-bottom: 16px; line-height: 1.6; }
.divider  { height: 1px; background: #E0E2DA; margin: 14px 0 18px; }

/* ── Step badge ── */
.step-badge {
  display: inline-block; background: #03221D; color: #DBFF9B;
  font-family: 'Urbanist', sans-serif; font-size: 11px; font-weight: 700;
  padding: 3px 10px; border-radius: 4px; letter-spacing: 0.05em; margin-bottom: 10px;
}
.pass-badge {
  display: inline-block;
  background: #d4f5e2; color: #1a7340;
  font-family: 'Urbanist', sans-serif; font-size: 11px; font-weight: 700;
  padding: 3px 10px; border-radius: 4px; letter-spacing: 0.04em; margin-bottom: 10px;
}

/* ── Processing log entries ── */
.log-wrap { display: flex; flex-direction: column; gap: 8px; }
.log-entry {
  background: #fff; border: 1px solid #E0E2DA; border-left: 3px solid #E0E2DA;
  border-radius: 0 8px 8px 0; padding: 10px 14px; font-size: 13px;
}
.log-entry.upload  { border-left-color: #ABC2EB; }
.log-entry.parse   { border-left-color: #C7DCCD; }
.log-entry.extract { border-left-color: #DBFF9B; }
.log-entry.pass    { border-left-color: #52c47a; }
.log-entry.fail    { border-left-color: #e05050; }
.log-ts { font-family: 'SF Mono','Fira Code',monospace; font-size: 10px; color: #7A8680; margin-bottom: 3px; }
.log-title { font-weight: 600; color: #0A0A08; margin-bottom: 3px; }
.log-detail { font-size: 12px; color: #4A5450; }
.log-kv { font-size: 12px; color: #4A5450; padding: 1px 0; }
.log-kv strong { color: #0A0A08; }
.log-check { font-size: 12px; padding: 2px 0; }
.log-empty { font-size: 13px; color: #7A8680; padding: 20px 0; }

/* ── Success screen ── */
.success-header {
  background: #03221D; border-radius: 10px;
  padding: 28px 24px; text-align: center; margin-bottom: 18px;
}
.success-header h2 {
  font-family: 'Urbanist', sans-serif; font-size: 24px; font-weight: 800;
  color: #DBFF9B; margin: 0 0 4px;
}
.success-header p { font-size: 13px; color: rgba(255,255,255,0.65); margin: 0; }

/* ── Metrics card ── */
.metrics-card {
  background: #fff; border: 1px solid #E0E2DA; border-radius: 10px;
  padding: 16px 20px; margin-bottom: 14px;
}
.metric-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 6px 0; border-bottom: 1px solid #E0E2DA; font-size: 13px;
}
.metric-row:last-child { border-bottom: none; }
.metric-label { color: #4A5450; }
.metric-val { font-family: 'Urbanist', sans-serif; font-weight: 700; color: #03221D; }
.metric-total .metric-val { font-size: 16px; }
.metric-section {
  font-family: 'Urbanist', sans-serif; font-size: 9px; font-weight: 700;
  letter-spacing: 0.12em; text-transform: uppercase; color: #43574C;
  padding: 8px 0 4px; border-bottom: 1px solid #E0E2DA;
}

/* ── Streamlit widget overrides ── */
div.stButton > button {
  background: #03221D !important; color: #DBFF9B !important;
  border: none !important; border-radius: 6px !important;
  font-family: 'Urbanist', sans-serif !important; font-weight: 700 !important;
  font-size: 14px !important; padding: 10px 0 !important; width: 100%;
  letter-spacing: 0.02em;
}
div.stButton > button:hover { background: #43574C !important; }
div.stButton > button[disabled] { opacity: 0.4 !important; }
[data-testid="stFileUploader"] { border: 1.5px dashed #C7DCCD; border-radius: 8px; padding: 6px; }
label { font-family: 'Urbanist', sans-serif !important; font-weight: 600 !important;
        font-size: 13px !important; color: #03221D !important; }
</style>
""",
    unsafe_allow_html=True,
)


# ── Session state ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "step": 0,
        "borrower_name": "",
        "borrower_ssn": "",
        "loan_application_date": None,
        "log": [],
        "manual_review": [],
        "w2_fields": {},
        "w2_passed": False,
        "w2_metrics": {},
        "w2_processed": False,
        "paystub_fields": {},
        "paystub_passed": False,
        "paystub_metrics": {},
        "paystub_processed": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()


# ── API calls ─────────────────────────────────────────────────────────────────
def api_parse(file_bytes: bytes, filename: str) -> dict:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    resp = requests.post(
        PARSE_URL,
        headers=headers,
        files={"document": (filename, file_bytes, "application/pdf")},
        data={"model": "dpt-2-latest"},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


def api_extract(markdown: str, schema: dict) -> dict:
    headers = {"Authorization": f"Bearer {API_KEY}"}
    resp = requests.post(
        EXTRACT_URL,
        headers=headers,
        files={"markdown": ("document.md", markdown.encode("utf-8"), "text/plain")},
        data={"schema": json.dumps(schema), "model": "extract-latest"},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


# ── Business logic ────────────────────────────────────────────────────────────
def normalize_ssn(ssn: str) -> str:
    return re.sub(r"\D", "", ssn or "")


def normalize_name(name: str) -> str:
    return (name or "").strip().lower()


def check_w2(fields: dict) -> tuple[bool, list[dict], list[str]]:
    """Returns (passed, checks, null_fields). Null fields are skipped; all definitive checks must pass."""
    borrower_name = st.session_state.borrower_name
    borrower_ssn  = st.session_state.borrower_ssn
    today         = date.today()
    checks, null_fields = [], []

    # A — name
    extracted_name = fields.get("w2_employee_name") or ""
    if not extracted_name.strip():
        null_fields.append("w2_employee_name")
        checks.append({"label": "Name match", "result": None, "detail": "Could not extract employee name"})
    else:
        ok = normalize_name(extracted_name) == normalize_name(borrower_name)
        checks.append({
            "label": "Name match", "result": ok,
            "detail": f'"{extracted_name}" vs "{borrower_name}"',
        })

    # B — SSN
    extracted_ssn = fields.get("w2_employee_ssn") or ""
    if not extracted_ssn.strip():
        null_fields.append("w2_employee_ssn")
        checks.append({"label": "SSN match", "result": None, "detail": "Could not extract SSN"})
    else:
        ok = normalize_ssn(extracted_ssn) == normalize_ssn(borrower_ssn)
        checks.append({
            "label": "SSN match", "result": ok,
            "detail": f"Normalized: {normalize_ssn(extracted_ssn)} vs {normalize_ssn(borrower_ssn)}",
        })

    # C — tax year (previous 2 years, regardless of month — per spec Jan is same rule)
    extracted_year = fields.get("w2_tax_year") or ""
    if not extracted_year.strip():
        null_fields.append("w2_tax_year")
        checks.append({"label": "Tax year valid", "result": None, "detail": "Could not extract tax year"})
    else:
        m = re.search(r"\d{4}", extracted_year)
        if not m:
            null_fields.append("w2_tax_year")
            checks.append({"label": "Tax year valid", "result": None, "detail": f'Cannot parse year from "{extracted_year}"'})
        else:
            year = int(m.group())
            valid_years = {today.year - 1, today.year - 2}
            ok = year in valid_years
            checks.append({
                "label": "Tax year valid", "result": ok,
                "detail": f"W-2 year {year} — acceptable: {sorted(valid_years)}",
            })

    definitive = [c for c in checks if c["result"] is not None]
    passed = all(c["result"] for c in definitive)
    return passed, checks, null_fields


def check_paystub(fields: dict) -> tuple[bool, list[dict], list[str]]:
    borrower_name = st.session_state.borrower_name
    borrower_ssn  = st.session_state.borrower_ssn
    loan_date     = st.session_state.loan_application_date
    checks, null_fields = [], []

    # A — name
    extracted_name = fields.get("paystub_employee_name") or ""
    if not extracted_name.strip():
        null_fields.append("paystub_employee_name")
        checks.append({"label": "Name match", "result": None, "detail": "Could not extract employee name"})
    else:
        ok = normalize_name(extracted_name) == normalize_name(borrower_name)
        checks.append({
            "label": "Name match", "result": ok,
            "detail": f'"{extracted_name}" vs "{borrower_name}"',
        })

    # B — SSN
    extracted_ssn = fields.get("paystub_employee_ssn") or ""
    if not extracted_ssn.strip():
        null_fields.append("paystub_employee_ssn")
        checks.append({"label": "SSN match", "result": None, "detail": "Could not extract SSN"})
    else:
        ok = normalize_ssn(extracted_ssn) == normalize_ssn(borrower_ssn)
        checks.append({
            "label": "SSN match", "result": ok,
            "detail": f"Normalized: {normalize_ssn(extracted_ssn)} vs {normalize_ssn(borrower_ssn)}",
        })

    # C — paydate within 30 days of loan application date
    extracted_date = fields.get("paystub_paydate") or ""
    if not extracted_date.strip() or loan_date is None:
        null_fields.append("paystub_paydate")
        checks.append({"label": "Paydate within 30 days", "result": None, "detail": "Could not extract pay date"})
    else:
        pay_date = None
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y", "%B %d, %Y", "%b %d, %Y", "%d %B %Y"):
            try:
                pay_date = datetime.strptime(extracted_date.strip(), fmt).date()
                break
            except ValueError:
                continue
        if pay_date is None:
            null_fields.append("paystub_paydate")
            checks.append({"label": "Paydate within 30 days", "result": None, "detail": f'Cannot parse date from "{extracted_date}"'})
        else:
            diff = abs((pay_date - loan_date).days)
            ok = diff <= 30
            checks.append({
                "label": "Paydate within 30 days", "result": ok,
                "detail": f"Pay date {pay_date}, loan date {loan_date} — {diff} days apart",
            })

    definitive = [c for c in checks if c["result"] is not None]
    passed = all(c["result"] for c in definitive)
    return passed, checks, null_fields


# ── Log renderer ──────────────────────────────────────────────────────────────
def render_log(placeholder, entries: list[dict]) -> None:
    if not entries:
        placeholder.markdown(
            '<div class="log-empty">No activity yet — complete the form on the left to begin.</div>',
            unsafe_allow_html=True,
        )
        return

    parts = []
    for e in entries:
        ts  = e.get("time", "")
        ts_str = ts.strftime("%H:%M:%S.%f")[:-3] if isinstance(ts, datetime) else str(ts)
        doc = e.get("doc", "")
        et  = e.get("type", "")

        if et == "upload":
            parts.append(f"""
<div class="log-entry upload">
  <div class="log-ts">{ts_str}</div>
  <div class="log-title">📤 {doc} — Upload received</div>
</div>""")

        elif et == "parse":
            dur = e.get("duration", 0)
            parts.append(f"""
<div class="log-entry parse">
  <div class="log-ts">{ts_str}</div>
  <div class="log-title">📄 {doc} — Parse complete</div>
  <div class="log-detail">Duration: {dur:.2f}s</div>
</div>""")

        elif et == "extract":
            dur    = e.get("duration", 0)
            fields = e.get("fields", {})
            kv_html = "".join(
                f'<div class="log-kv"><span style="color:#7A8680">{k}:</span> '
                f'{"<strong>" + str(v) + "</strong>" if v else "<em style=color:#e05050>null</em>"}</div>'
                for k, v in fields.items()
            )
            parts.append(f"""
<div class="log-entry extract">
  <div class="log-ts">{ts_str}</div>
  <div class="log-title">🔍 {doc} — Extract complete</div>
  <div class="log-detail" style="margin-bottom:4px">Duration: {dur:.2f}s</div>
  {kv_html}
</div>""")

        elif et == "rules":
            checks    = e.get("checks", [])
            passed    = e.get("passed", False)
            null_flds = e.get("null_fields", [])

            checks_html = ""
            for c in checks:
                r = c.get("result")
                icon = "✅" if r is True else ("❌" if r is False else "⚠️")
                checks_html += f'<div class="log-check">{icon} <strong>{c["label"]}</strong>: <span style="color:#7A8680">{c["detail"]}</span></div>'

            verdict_style = "color:#1a7340;background:#d4f5e2" if passed else "color:#912f2f;background:#fde8e8"
            verdict_label = "PASS" if passed else "FAIL"
            manual_note = ""
            if null_flds:
                manual_note = f'<div style="font-size:11px;color:#7a5800;margin-top:6px">⚠️ Manual review flagged: {", ".join(null_flds)}</div>'

            entry_class = "pass" if passed else "fail"
            parts.append(f"""
<div class="log-entry {entry_class}">
  <div class="log-ts">{ts_str}</div>
  <div class="log-title">📋 {doc} — Business rules</div>
  {checks_html}
  <div style="margin-top:8px">
    <span style="display:inline-block;padding:2px 10px;border-radius:20px;font-weight:700;font-size:12px;{verdict_style}">{verdict_label}</span>
  </div>
  {manual_note}
</div>""")

    placeholder.markdown(
        f'<div class="log-wrap">{"".join(parts)}</div>',
        unsafe_allow_html=True,
    )


# ── App header ────────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="lai-header">
  <span class="lai-logo">Landing AI</span>
  <div class="lai-sep"></div>
  <span class="lai-title">Instant Feedback Demo</span>
  <span class="lai-badge">Landing AI Demo</span>
</div>
""",
    unsafe_allow_html=True,
)

if not API_KEY:
    st.error("VISION_AGENT_API_KEY is not set. Add it to a .env file in the project directory.")
    st.stop()

# ── Layout ────────────────────────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")

# Right column — always rendered from session state
with right_col:
    st.markdown('<div class="eyebrow">Processing View</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Real-time Log</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    log_placeholder = st.empty()
    render_log(log_placeholder, st.session_state.log)

# Left column — step-based UX
with left_col:

    # ── Step 0: Borrower info form ────────────────────────────────
    if st.session_state.step == 0:
        st.markdown('<div class="eyebrow">Step 1 of 3</div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-title">Borrower Information</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="sec-sub">Enter borrower details to begin the verification workflow.</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        with st.form("borrower_form"):
            name      = st.text_input("Borrower Name", placeholder="e.g. John McCay")
            ssn       = st.text_input("Borrower SSN",  placeholder="e.g. 123-45-6789")
            loan_date = st.date_input("Loan Application Date", value=date.today())
            submitted = st.form_submit_button("Start Verification →")

        if submitted:
            if not name.strip() or not ssn.strip():
                st.error("Borrower name and SSN are required.")
            else:
                st.session_state.borrower_name        = name.strip()
                st.session_state.borrower_ssn         = ssn.strip()
                st.session_state.loan_application_date = loan_date
                st.session_state.step = 1
                st.rerun()

    # ── Step 1: W-2 upload ───────────────────────────────────────
    elif st.session_state.step == 1:
        st.markdown('<span class="step-badge">Step 2 of 3</span>', unsafe_allow_html=True)
        st.markdown('<div class="sec-title">Upload W-2 Form</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="sec-sub">Verifying for <strong>{st.session_state.borrower_name}</strong>. '
            "The system will check name, SSN, and tax year.</div>",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        uploaded_w2 = st.file_uploader("Choose W-2 PDF", type=["pdf"], key="w2_file")

        if uploaded_w2:
            if st.button("Process W-2"):
                file_bytes = uploaded_w2.read()
                t_upload   = datetime.now()
                log        = st.session_state.log

                log.append({"time": t_upload, "type": "upload", "doc": "W-2"})
                render_log(log_placeholder, log)

                try:
                    t0         = datetime.now()
                    parse_resp = api_parse(file_bytes, uploaded_w2.name)
                    t1         = datetime.now()
                    log.append({"time": t1, "type": "parse", "doc": "W-2", "duration": (t1 - t0).total_seconds()})
                    render_log(log_placeholder, log)

                    markdown     = parse_resp.get("markdown", "")
                    t2           = datetime.now()
                    extract_resp = api_extract(markdown, W2_SCHEMA)
                    t3           = datetime.now()
                    fields       = extract_resp.get("extraction", {})
                    log.append({"time": t3, "type": "extract", "doc": "W-2",
                                "duration": (t3 - t2).total_seconds(), "fields": fields})
                    render_log(log_placeholder, log)

                    passed, checks, null_fields = check_w2(fields)
                    log.append({"time": datetime.now(), "type": "rules", "doc": "W-2",
                                "passed": passed, "checks": checks, "null_fields": null_fields})
                    render_log(log_placeholder, log)

                    st.session_state.w2_fields    = fields
                    st.session_state.w2_passed    = passed
                    st.session_state.w2_processed = True
                    st.session_state.w2_metrics   = {
                        "parse_s":   (t1 - t0).total_seconds(),
                        "extract_s": (t3 - t2).total_seconds(),
                        "total_s":   (t3 - t_upload).total_seconds(),
                    }
                    st.session_state.manual_review.extend([f"W-2 › {f}" for f in null_fields])
                    st.session_state.log = log

                    if passed:
                        st.session_state.step = 2
                        st.rerun()

                except Exception as exc:
                    st.session_state.log = log
                    st.error(f"API error: {exc}")

        if st.session_state.w2_processed and not st.session_state.w2_passed:
            st.error("W-2 verification failed — one or more checks did not pass. Please review the log and try again.")
            if st.button("Clear & Try Again", key="w2_retry"):
                st.session_state.w2_processed = False
                st.session_state.w2_fields    = {}
                st.rerun()

    # ── Step 2: Paystub upload ───────────────────────────────────
    elif st.session_state.step == 2:
        st.markdown('<span class="pass-badge">✓ W-2 Verified</span>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<span class="step-badge">Step 3 of 3</span>', unsafe_allow_html=True)
        st.markdown('<div class="sec-title">Upload Paystub</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="sec-sub">Verifying for <strong>{st.session_state.borrower_name}</strong>. '
            "The system will check name, SSN, and that the pay date is within 30 days of the loan application date.</div>",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        uploaded_ps = st.file_uploader("Choose Paystub PDF", type=["pdf"], key="ps_file")

        if uploaded_ps:
            if st.button("Process Paystub"):
                file_bytes = uploaded_ps.read()
                t_upload   = datetime.now()
                log        = st.session_state.log

                log.append({"time": t_upload, "type": "upload", "doc": "Paystub"})
                render_log(log_placeholder, log)

                try:
                    t0         = datetime.now()
                    parse_resp = api_parse(file_bytes, uploaded_ps.name)
                    t1         = datetime.now()
                    log.append({"time": t1, "type": "parse", "doc": "Paystub", "duration": (t1 - t0).total_seconds()})
                    render_log(log_placeholder, log)

                    markdown     = parse_resp.get("markdown", "")
                    t2           = datetime.now()
                    extract_resp = api_extract(markdown, PAYSTUB_SCHEMA)
                    t3           = datetime.now()
                    fields       = extract_resp.get("extraction", {})
                    log.append({"time": t3, "type": "extract", "doc": "Paystub",
                                "duration": (t3 - t2).total_seconds(), "fields": fields})
                    render_log(log_placeholder, log)

                    passed, checks, null_fields = check_paystub(fields)
                    log.append({"time": datetime.now(), "type": "rules", "doc": "Paystub",
                                "passed": passed, "checks": checks, "null_fields": null_fields})
                    render_log(log_placeholder, log)

                    st.session_state.paystub_fields    = fields
                    st.session_state.paystub_passed    = passed
                    st.session_state.paystub_processed = True
                    st.session_state.paystub_metrics   = {
                        "parse_s":   (t1 - t0).total_seconds(),
                        "extract_s": (t3 - t2).total_seconds(),
                        "total_s":   (t3 - t_upload).total_seconds(),
                    }
                    st.session_state.manual_review.extend([f"Paystub › {f}" for f in null_fields])
                    st.session_state.log = log

                    if passed:
                        st.session_state.step = 3
                        st.rerun()

                except Exception as exc:
                    st.session_state.log = log
                    st.error(f"API error: {exc}")

        if st.session_state.paystub_processed and not st.session_state.paystub_passed:
            st.error("Paystub verification failed — one or more checks did not pass. Please review the log and try again.")
            col_retry, col_summary = st.columns(2)
            with col_retry:
                if st.button("Clear & Try Again", key="ps_retry"):
                    st.session_state.paystub_processed = False
                    st.session_state.paystub_fields    = {}
                    st.rerun()
            with col_summary:
                if st.button("See Summary Metrics →", key="ps_summary"):
                    st.session_state.step = 3
                    st.rerun()

        if st.session_state.paystub_processed and st.session_state.paystub_passed:
            if st.button("See Summary Metrics →", key="ps_summary_pass"):
                st.session_state.step = 3
                st.rerun()

    # ── Step 3: Success screen ───────────────────────────────────
    elif st.session_state.step == 3:
        manual          = st.session_state.manual_review
        paystub_failed  = st.session_state.paystub_processed and not st.session_state.paystub_passed

        if paystub_failed:
            header_html = """
<div class="success-header">
  <h2>❌ Paystub Not Verified</h2>
  <p>W-2 passed — paystub did not meet one or more business rules</p>
</div>"""
        elif manual:
            header_html = """
<div class="success-header">
  <h2>⚠️ Verification Complete</h2>
  <p>All documents accepted — some fields flagged for manual review</p>
</div>"""
        else:
            header_html = """
<div class="success-header">
  <h2>✓ Verification Complete</h2>
  <p>All documents verified successfully</p>
</div>"""
        st.markdown(header_html, unsafe_allow_html=True)

        # ── Processing time metrics ──
        w2m   = st.session_state.w2_metrics
        psm   = st.session_state.paystub_metrics
        total = w2m.get("total_s", 0) + psm.get("total_s", 0)

        st.markdown(
            """
<div class="metrics-card">
  <div class="metric-section">Processing Times</div>
  <div class="metric-row">
    <span class="metric-label">W-2 Parse</span>
    <span class="metric-val">{w2p:.2f}s</span>
  </div>
  <div class="metric-row">
    <span class="metric-label">W-2 Extract</span>
    <span class="metric-val">{w2e:.2f}s</span>
  </div>
  <div class="metric-row">
    <span class="metric-label">W-2 Total</span>
    <span class="metric-val">{w2t:.2f}s</span>
  </div>
  <div class="metric-section">Paystub</div>
  <div class="metric-row">
    <span class="metric-label">Paystub Parse</span>
    <span class="metric-val">{psp:.2f}s</span>
  </div>
  <div class="metric-row">
    <span class="metric-label">Paystub Extract</span>
    <span class="metric-val">{pse:.2f}s</span>
  </div>
  <div class="metric-row">
    <span class="metric-label">Paystub Total</span>
    <span class="metric-val">{pst:.2f}s</span>
  </div>
  <div class="metric-row metric-total" style="padding-top:10px">
    <span class="metric-label"><strong>Total Processing Time</strong></span>
    <span class="metric-val" style="font-size:18px">{tot:.2f}s</span>
  </div>
</div>""".format(
                w2p=w2m.get("parse_s", 0),
                w2e=w2m.get("extract_s", 0),
                w2t=w2m.get("total_s", 0),
                psp=psm.get("parse_s", 0),
                pse=psm.get("extract_s", 0),
                pst=psm.get("total_s", 0),
                tot=total,
            ),
            unsafe_allow_html=True,
        )

        # ── Extracted fields ──
        w2f = st.session_state.w2_fields
        psf = st.session_state.paystub_fields

        def frow(label: str, value) -> str:
            val = (
                f"<strong>{value}</strong>"
                if value
                else "<em style='color:#e05050'>null — manual review</em>"
            )
            return f'<div class="metric-row"><span class="metric-label">{label}</span><span style="font-size:13px">{val}</span></div>'

        st.markdown(
            f"""
<div class="metrics-card">
  <div class="metric-section">Extracted Fields — W-2</div>
  {frow("Employee Name",  w2f.get("w2_employee_name"))}
  {frow("Employee SSN",   w2f.get("w2_employee_ssn"))}
  {frow("Tax Year",       w2f.get("w2_tax_year"))}
  <div class="metric-section">Extracted Fields — Paystub</div>
  {frow("Employee Name",  psf.get("paystub_employee_name"))}
  {frow("Employee SSN",   psf.get("paystub_employee_ssn"))}
  {frow("Pay Date",       psf.get("paystub_paydate"))}
</div>""",
            unsafe_allow_html=True,
        )

        # ── Manual review list ──
        if manual:
            items_html = "".join(
                f'<div style="font-size:13px;padding:5px 0;border-bottom:1px solid #E0E2DA">⚠️ {item}</div>'
                for item in manual
            )
            st.markdown(
                f'<div class="metrics-card"><div class="metric-section">Manual Review Required</div>{items_html}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Start New Verification"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            init_state()
            st.rerun()
