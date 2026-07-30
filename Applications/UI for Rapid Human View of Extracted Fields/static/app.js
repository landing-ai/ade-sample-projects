/* ADE human-in-the-loop review UI.
 *
 * State model: overrides live per document stem in an in-memory map that
 * survives navigation between documents, so a reviewer can move around the
 * batch without losing work before pressing Submit.
 *
 * A field counts as overridden only once the reviewer types into it. The ADE
 * value sits in the input's placeholder, never its value, which is what makes
 * "never touched" distinguishable from "deliberately emptied".
 */

const $ = (id) => document.getElementById(id);

const state = {
  folder: null,
  schema: null,
  files: [],
  fileIndex: 0,
  doc: null,
  page: 1,
  selected: 0,
  overridesByStem: new Map(), // stem -> Map(path -> value)
  openedStems: new Set(),
  theme: localStorage.getItem("hl-theme") || "theme-volt",
  polling: null,
};

/* --------------------------------------------------------------- utilities */

async function api(path, opts) {
  const res = await fetch(path, opts);
  const text = await res.text();
  let body = null;
  try {
    body = text ? JSON.parse(text) : null;
  } catch {
    body = { error: text };
  }
  if (!res.ok) throw new Error((body && body.error) || `HTTP ${res.status}`);
  return body;
}

function setStatus(msg, isError = false) {
  const el = $("status");
  el.textContent = msg || "";
  el.classList.toggle("error", Boolean(isError));
}

function overridesFor(stem) {
  if (!state.overridesByStem.has(stem)) state.overridesByStem.set(stem, new Map());
  return state.overridesByStem.get(stem);
}

function currentStem() {
  const f = state.files[state.fileIndex];
  return f ? f.stem : null;
}

function displayValue(v) {
  if (v === null || v === undefined || v === "") return "";
  if (typeof v === "object") return JSON.stringify(v);
  return String(v);
}

/* ------------------------------------------------------------ bootstrapping */

async function init() {
  applyTheme(state.theme);

  try {
    const [folders, schemas] = await Promise.all([
      api("/api/folders"),
      api("/api/schemas"),
    ]);
    fillSelect($("folder"), folders.folders);
    fillSelect($("schema"), schemas.schemas);
    state.folder = $("folder").value || null;
    state.schema = $("schema").value || null;
    if (state.folder) await loadFiles();
  } catch (err) {
    setStatus(err.message, true);
  }

  $("folder").addEventListener("change", async () => {
    $("folder-path").value = "";
    state.folder = $("folder").value;
    state.fileIndex = 0;
    await loadFiles();
  });
  // A typed absolute path wins over the dropdown, since the dropdown can only
  // ever show folders that live under input_folders/.
  $("folder-path").addEventListener("change", async () => {
    const typed = $("folder-path").value.trim();
    state.folder = typed || $("folder").value;
    state.fileIndex = 0;
    state.overridesByStem.clear();
    state.openedStems.clear();
    await loadFiles();
  });
  $("schema").addEventListener("change", async () => {
    state.schema = $("schema").value;
    if (currentStem()) await loadDoc();
  });

  $("run").addEventListener("click", runBatch);
  $("submit-file").addEventListener("click", submitFile);
  $("submit-batch").addEventListener("click", submitBatch);
  $("doc-prev").addEventListener("click", () => moveDoc(-1));
  $("doc-next").addEventListener("click", () => moveDoc(1));
  $("page-prev").addEventListener("click", () => movePage(-1));
  $("page-next").addEventListener("click", () => movePage(1));

  $("theme-picker").addEventListener("click", (e) => {
    const btn = e.target.closest(".swatch");
    if (btn) applyTheme(btn.dataset.theme);
  });

  $("font-up").addEventListener("click", () => bumpFont(1));
  $("font-down").addEventListener("click", () => bumpFont(-1));
  $("reset").addEventListener("click", onResetClick);
  initSplitter();
  applyFont(Number(localStorage.getItem("fields-fs")) || 15);

  document.addEventListener("keydown", onKeyDown);
  pollProgress();
}

/* ------------------------------------------------- pane width + text size */

function initSplitter() {
  const saved = Number(localStorage.getItem("right-w"));
  if (saved) setRightWidth(saved);

  const splitter = $("splitter");
  let dragging = false;

  const onMove = (e) => {
    if (!dragging) return;
    // Width measured from the right edge of the window.
    setRightWidth(window.innerWidth - e.clientX);
    e.preventDefault();
  };
  const stop = () => {
    if (!dragging) return;
    dragging = false;
    splitter.classList.remove("dragging");
    document.body.classList.remove("resizing");
    localStorage.setItem("right-w", String(currentRightWidth()));
    // A resize changes the rendered page size, so re-place the highlights.
    drawHighlights();
  };

  splitter.addEventListener("mousedown", (e) => {
    dragging = true;
    splitter.classList.add("dragging");
    document.body.classList.add("resizing");
    e.preventDefault();
  });
  window.addEventListener("mousemove", onMove);
  window.addEventListener("mouseup", stop);
}

function currentRightWidth() {
  return parseInt(
    getComputedStyle(document.documentElement).getPropertyValue("--right-w"),
    10
  );
}

function setRightWidth(px) {
  // Keep both panes usable however far the splitter is dragged.
  const min = 320;
  const max = Math.max(min, window.innerWidth - 360);
  const clamped = Math.min(max, Math.max(min, Math.round(px)));
  document.documentElement.style.setProperty("--right-w", `${clamped}px`);
}

function bumpFont(delta) {
  const current = Number(localStorage.getItem("fields-fs")) || 15;
  applyFont(current + delta);
}

function applyFont(size) {
  const clamped = Math.min(22, Math.max(12, size));
  document.documentElement.style.setProperty("--fields-fs", `${clamped}px`);
  localStorage.setItem("fields-fs", String(clamped));
}

/* --------------------------------------------------------------- reset */

async function onResetClick() {
  const btn = $("reset");
  // Two-step confirm rather than a blocking browser dialog.
  if (!btn.classList.contains("confirming")) {
    btn.classList.add("confirming");
    btn.textContent = "Click again to confirm";
    setStatus(
      "Reset will delete parse, extract, region, page-image and HIL results for " +
        "this folder. Source documents are kept.",
      true
    );
    clearTimeout(state.resetTimer);
    state.resetTimer = setTimeout(cancelReset, 6000);
    return;
  }
  clearTimeout(state.resetTimer);
  cancelReset();

  try {
    const res = await api("/api/reset", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ folder: state.folder }),
    });
    state.overridesByStem.clear();
    state.openedStems.clear();
    state.doc = null;
    state.lastFinished = null;
    $("doc-title").textContent = "Document";
    $("doc-body").innerHTML =
      '<div class="empty-state">Reset complete. Press <strong>Parse+Extract</strong> to start over.</div>';
    $("fields-body").innerHTML =
      '<div class="empty-state">No extraction results yet.</div>';
    $("override-summary").textContent = "";
    setBar("parse", 0, 0);
    setBar("extract", 0, 0);
    await refreshFileList();
    setStatus(
      res.removed.length
        ? `Reset: removed ${res.removed.join(", ")}. ${res.documents_kept} source document(s) kept.`
        : `Nothing to remove. ${res.documents_kept} source document(s) kept.`
    );
  } catch (err) {
    setStatus(err.message, true);
  }
}

function cancelReset() {
  const btn = $("reset");
  btn.classList.remove("confirming");
  btn.textContent = "Clear & reset";
}

function fillSelect(select, values) {
  select.innerHTML = "";
  for (const v of values) {
    const opt = document.createElement("option");
    opt.value = v;
    opt.textContent = v;
    select.appendChild(opt);
  }
}

function applyTheme(theme) {
  state.theme = theme;
  localStorage.setItem("hl-theme", theme);
  const body = $("doc-body");
  body.classList.remove("theme-volt", "theme-ice", "theme-outline");
  body.classList.add(theme);
  for (const sw of document.querySelectorAll(".swatch")) {
    sw.classList.toggle("active", sw.dataset.theme === theme);
  }
}

/* -------------------------------------------------------------- run + poll */

async function runBatch() {
  if (!state.folder || !state.schema) {
    setStatus("Pick a folder and a schema first.", true);
    return;
  }
  try {
    await api("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        folder: state.folder,
        schema_name: state.schema,
        force: $("force").checked,
      }),
    });
    setStatus("Run started.");
    $("run").disabled = true;
  } catch (err) {
    setStatus(err.message, true);
  }
}

async function pollProgress() {
  try {
    const p = await api("/api/progress");
    const total = p.total || 0;
    setBar("parse", p.parsed, total);
    setBar("extract", p.extracted, total);
    $("run").disabled = p.running;

    if (p.running) {
      setStatus(
        `Running… parsed ${p.parsed}/${total}, extracted ${p.extracted}/${total}` +
          (p.skipped ? ` (${p.skipped} reused)` : "")
      );
    } else if (p.finished_at && !state.lastFinished) {
      state.lastFinished = p.finished_at;
      const notes = [];
      if (p.skipped) notes.push(`${p.skipped} reused from cache`);
      if (p.failures.length) notes.push(`${p.failures.length} failed`);
      if (p.message) notes.push(p.message);
      setStatus(`Run complete. ${notes.join(", ")}`, p.failures.length > 0);
      await loadFiles();
    } else if (p.message && !p.running) {
      setStatus(p.message, true);
    }

    renderFailures(p.failures);
  } catch {
    /* backend not reachable yet; keep polling quietly */
  }
  state.polling = setTimeout(pollProgress, 1000);
}

function setBar(prefix, done, total) {
  $(`${prefix}-count`).textContent = `${done}/${total}`;
  const pct = total ? Math.round((done / total) * 100) : 0;
  $(`${prefix}-bar`).style.width = `${pct}%`;
}

function renderFailures(failures) {
  const existing = document.querySelector(".notice.run-failures");
  if (existing) existing.remove();
  if (!failures || !failures.length) return;
  const div = document.createElement("div");
  div.className = "notice error run-failures";
  div.innerHTML =
    `<strong>${failures.length} document(s) failed.</strong> ` +
    failures.map((f) => `${f.document} (${f.stage}): ${f.error}`).join("<br>");
  $("doc-body").prepend(div);
}

/* ------------------------------------------------------------- file loading */

async function loadFiles() {
  if (!state.folder) return;
  try {
    const data = await api(`/api/files?folder=${encodeURIComponent(state.folder)}`);
    state.files = data.files;
    if (state.fileIndex >= state.files.length) state.fileIndex = 0;
    updateDocPos();
    if (state.files.length && state.files.some((f) => f.has_extract)) {
      await loadDoc();
    } else {
      $("fields-body").innerHTML =
        '<div class="empty-state">No extraction results yet. Press Parse+Extract.</div>';
    }
  } catch (err) {
    setStatus(err.message, true);
  }
}

async function refreshFileList() {
  // Refresh submitted/override badges without reloading the open document --
  // reloading would reset the selection and yank the reviewer back to field 0.
  if (!state.folder) return;
  try {
    const data = await api(`/api/files?folder=${encodeURIComponent(state.folder)}`);
    state.files = data.files;
    updateDocPos();
  } catch {
    /* non-fatal: the badges just stay stale until the next load */
  }
}

function updateDocPos() {
  const n = state.files.length;
  $("doc-pos").textContent = n
    ? `Document ${state.fileIndex + 1} of ${n}`
    : "No documents";
}

async function loadDoc() {
  const stem = currentStem();
  if (!stem || !state.schema) return;
  const file = state.files[state.fileIndex];
  if (!file.has_extract) {
    $("fields-body").innerHTML =
      '<div class="empty-state">This document has no extraction results yet.</div>';
    $("doc-body").innerHTML = '<div class="empty-state">Nothing to show.</div>';
    return;
  }

  try {
    const doc = await api(
      `/api/doc?folder=${encodeURIComponent(state.folder)}&stem=${encodeURIComponent(
        stem
      )}&schema_name=${encodeURIComponent(state.schema)}`
    );
    state.doc = doc;
    state.selected = 0;
    state.page = 1;
    state.openedStems.add(stem);

    // Seed in-memory overrides from anything previously submitted, once.
    const map = overridesFor(stem);
    if (map.size === 0 && doc.saved_overrides) {
      for (const [path, value] of Object.entries(doc.saved_overrides)) {
        map.set(path, value);
      }
    }

    $("doc-title").textContent = doc.document;
    renderFields();
    renderPage();
    updateDocPos();
    setStatus("");
  } catch (err) {
    setStatus(err.message, true);
  }
}

/* ---------------------------------------------------------------- rendering */

function renderFields() {
  const doc = state.doc;
  const body = $("fields-body");
  body.innerHTML = "";

  // ADE's own extraction warnings (schema_violation_error / warnings) are
  // intentionally not surfaced. The two notices below are integrity problems
  // with the local data, not ADE commentary, so they stay.
  const notices = [];
  if (!doc.paired) {
    notices.push(
      `<div class="notice warn"><strong>Extraction is not linked to this parse.</strong>
       The stored extraction's doc_id does not match the parse job, so highlight
       positions may be wrong. Re-run with Force re-run to fix.</div>`
    );
  }
  if (doc.failed_pages && doc.failed_pages.length) {
    notices.push(
      `<div class="notice warn">Parse failed on page(s) ${doc.failed_pages.join(", ")};
       those pages render without highlights.</div>`
    );
  }
  if (notices.length) body.innerHTML = notices.join("");

  const list = document.createElement("div");
  list.className = "fields";
  const map = overridesFor(doc.stem);
  const groupSizes = arrayGroupSizes(doc.fields);
  let lastGroup = null;

  doc.fields.forEach((f, i) => {
    // Insert a heading whenever we enter a new array element, so six
    // "Container number" rows read as Container 1..6 rather than a wall of
    // identical labels.
    const g = arrayGroupOf(f.path);
    if (g && g.key !== lastGroup) {
      const head = document.createElement("div");
      head.className = "array-group";
      const title = document.createElement("span");
      title.className = "array-group-title";
      title.textContent = `${humanizeSegment(g.name)} ${g.index + 1}`;
      const count = document.createElement("span");
      count.className = "array-group-count";
      count.textContent = `of ${groupSizes.get(g.name) || g.index + 1}`;
      head.append(title, count);
      list.appendChild(head);
    }
    lastGroup = g ? g.key : null;

    const row = document.createElement("div");
    row.className = "field-row" + (g ? " in-array" : "");
    row.dataset.index = String(i);
    if (i === state.selected) row.classList.add("selected");

    const value = displayValue(f.ade_value);

    const top = document.createElement("div");
    top.className = "field-top";
    const label = document.createElement("span");
    label.className = "field-label";
    label.textContent = f.label;
    if (f.description) label.title = f.description;
    const path = document.createElement("span");
    path.className = "field-path";
    path.textContent = f.path;
    path.title = f.path;
    top.append(label, path);

    const val = document.createElement("div");
    val.className = "field-value" + (value ? "" : " empty");
    val.textContent = value || "— no value extracted —";

    const input = document.createElement("input");
    input.className = "override";
    input.type = "text";
    input.placeholder = value || "type a value";
    input.value = map.has(f.path) ? displayValue(map.get(f.path)) : "";

    const paint = () => {
      // "Changed" means genuinely different from what ADE extracted. Retyping
      // the same value is touched-but-unchanged and stays neutral.
      const touched = map.has(f.path);
      const changed = touched && displayValue(map.get(f.path)) !== value;
      row.classList.toggle("is-override", touched);
      row.classList.toggle("is-changed", changed);
      input.classList.toggle("changed", changed);
    };
    paint();

    input.addEventListener("input", () => {
      map.set(f.path, input.value);
      paint();
      updateOverrideSummary();
    });
    input.addEventListener("focus", () => selectField(i, false));

    row.append(top, val, input);
    row.addEventListener("click", (e) => {
      if (e.target !== input) selectField(i, true);
    });
    list.appendChild(row);
  });

  body.appendChild(list);
  updateOverrideSummary();
}

/* Array paths look like `containers[2].container_number` or
 * `goods.itemized_list[0].gross_weight`. Group by everything up to and
 * including the last index. */
function arrayGroupOf(path) {
  const m = /^(.*)\[(\d+)\]/.exec(path);
  if (!m) return null;
  return { key: `${m[1]}[${m[2]}]`, name: m[1], index: Number(m[2]) };
}

function arrayGroupSizes(fields) {
  const sizes = new Map();
  for (const f of fields) {
    const g = arrayGroupOf(f.path);
    if (g) sizes.set(g.name, Math.max(sizes.get(g.name) || 0, g.index + 1));
  }
  return sizes;
}

function humanizeSegment(name) {
  const last = name.split(".").pop().replace(/\[\d+\]/g, "").replace(/_/g, " ");
  return last.charAt(0).toUpperCase() + last.slice(1);
}

function updateOverrideSummary() {
  const doc = state.doc;
  if (!doc) return;
  const map = overridesFor(doc.stem);
  // Count only real changes, matching what the backend will record.
  let n = 0;
  for (const f of doc.fields) {
    if (map.has(f.path) && displayValue(map.get(f.path)) !== displayValue(f.ade_value)) n++;
  }
  $("override-summary").textContent = n
    ? `${n} override${n === 1 ? "" : "s"} · ${doc.fields.length} fields`
    : `${doc.fields.length} fields`;
}

function selectField(index, jump) {
  if (!state.doc) return;
  const fields = state.doc.fields;
  if (!fields.length) return;
  state.selected = Math.max(0, Math.min(index, fields.length - 1));

  for (const row of document.querySelectorAll(".field-row")) {
    row.classList.toggle("selected", Number(row.dataset.index) === state.selected);
  }
  const selectedRow = document.querySelector(".field-row.selected");
  if (selectedRow) selectedRow.scrollIntoView({ block: "nearest" });

  const field = fields[state.selected];
  const regions = field.regions || [];
  if (jump && regions.length) {
    const target = regions[0].page;
    if (target !== state.page) {
      state.page = target;
      renderPage();
      return;
    }
  }
  drawHighlights();
}

function renderPage() {
  const doc = state.doc;
  const body = $("doc-body");
  if (!doc) return;

  const pageCount = doc.page_count || 1;
  state.page = Math.max(1, Math.min(state.page, pageCount));
  $("page-pos").textContent = `Page ${state.page} of ${pageCount}`;
  $("page-prev").disabled = state.page <= 1;
  $("page-next").disabled = state.page >= pageCount;

  body.innerHTML = "";
  body.classList.add(state.theme);

  const wrap = document.createElement("div");
  wrap.className = "page-wrap";
  wrap.id = "page-wrap";

  const img = document.createElement("img");
  img.alt = `${doc.document} page ${state.page}`;
  img.src = `/api/page-image?folder=${encodeURIComponent(
    state.folder
  )}&stem=${encodeURIComponent(doc.stem)}&page=${state.page}`;
  img.addEventListener("load", drawHighlights);
  img.addEventListener("error", () => {
    wrap.innerHTML = '<div class="empty-state">Could not render this page.</div>';
  });

  wrap.appendChild(img);
  body.appendChild(wrap);
}

function drawHighlights() {
  const wrap = $("page-wrap");
  if (!wrap || !state.doc) return;
  for (const el of wrap.querySelectorAll(".hl")) el.remove();

  const field = state.doc.fields[state.selected];
  if (!field) return;

  // Normalized boxes map straight onto percentages, so highlights stay correct
  // at any rendered size without needing the image's pixel dimensions.
  const onPage = (field.regions || []).filter((r) => r.page === state.page);
  let firstEl = null;
  for (const r of onPage) {
    const div = document.createElement("div");
    div.className = "hl hl-pulse";
    div.style.left = `${r.xmin * 100}%`;
    div.style.top = `${r.ymin * 100}%`;
    div.style.width = `${(r.xmax - r.xmin) * 100}%`;
    div.style.height = `${(r.ymax - r.ymin) * 100}%`;
    wrap.appendChild(div);
    if (!firstEl) firstEl = div;
  }

  // Bring the highlight into view when it sits outside the visible strip of the
  // page. Only the pane scrolls -- the surrounding chrome stays put.
  if (firstEl) {
    const pane = $("doc-body");
    const paneRect = pane.getBoundingClientRect();
    const hlRect = firstEl.getBoundingClientRect();
    if (hlRect.top < paneRect.top + 8 || hlRect.bottom > paneRect.bottom - 8) {
      const offsetInPane = hlRect.top - paneRect.top + pane.scrollTop;
      pane.scrollTo({
        top: Math.max(0, offsetInPane - pane.clientHeight * 0.35),
        behavior: "smooth",
      });
    }
  }

  const all = field.regions || [];
  const otherPages = [...new Set(all.map((r) => r.page))].filter((p) => p !== state.page);
  if (!all.length) {
    setStatus(`"${field.label}" has no source location in the document.`);
  } else if (otherPages.length) {
    setStatus(`"${field.label}" also appears on page ${otherPages.join(", ")}.`);
  } else {
    setStatus("");
  }
}

/* -------------------------------------------------------------- navigation */

function movePage(delta) {
  if (!state.doc) return;
  state.page += delta;
  renderPage();
}

async function moveDoc(delta) {
  if (!state.files.length) return;
  const next = state.fileIndex + delta;
  if (next < 0 || next >= state.files.length) return;
  state.fileIndex = next;
  await loadDoc();
}

function onKeyDown(e) {
  const editing = document.activeElement && document.activeElement.classList.contains("override");

  if (e.key === "Escape" && editing) {
    document.activeElement.blur();
    e.preventDefault();
    return;
  }
  if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "s") {
    e.preventDefault();
    submitFile();
    return;
  }
  if (editing) return; // let the input own every other key

  if (e.key === "ArrowDown") {
    e.preventDefault();
    selectField(state.selected + 1, true);
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    selectField(state.selected - 1, true);
  } else if (e.key === "Enter") {
    e.preventDefault();
    const row = document.querySelector(".field-row.selected input.override");
    if (row) row.focus();
  } else if (e.key === "[") {
    moveDoc(-1);
  } else if (e.key === "]") {
    moveDoc(1);
  } else if (e.key === "PageUp") {
    e.preventDefault();
    movePage(-1);
  } else if (e.key === "PageDown") {
    e.preventDefault();
    movePage(1);
  }
}

/* ----------------------------------------------------------------- submit */

function overridesPayload(stem) {
  const out = {};
  for (const [path, value] of overridesFor(stem)) out[path] = value;
  return out;
}

async function submitFile() {
  const stem = currentStem();
  if (!stem || !state.doc) return;
  try {
    const res = await api("/api/submit-file", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        folder: state.folder,
        schema_name: state.schema,
        stem,
        overrides: overridesPayload(stem),
      }),
    });
    setStatus(
      `Saved ${stem}.hil.json — ${res.override_count} override${
        res.override_count === 1 ? "" : "s"
      }.`
    );
    await refreshFileList();
  } catch (err) {
    setStatus(err.message, true);
  }
}

async function submitBatch() {
  if (!state.folder || !state.schema) return;
  const overridesByStem = {};
  for (const stem of state.overridesByStem.keys()) {
    overridesByStem[stem] = overridesPayload(stem);
  }
  try {
    const res = await api("/api/submit-batch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        folder: state.folder,
        schema_name: state.schema,
        overrides_by_stem: overridesByStem,
        opened_stems: [...state.openedStems],
      }),
    });
    const s = res.summary;
    const skipped = res.skipped.length ? `, ${res.skipped.length} skipped (no extraction)` : "";
    setStatus(
      `Batch submitted: ${res.documents_written} file(s), ${s.total_overrides} override(s) ` +
        `across ${s.total_fields} fields (${s.documents_never_opened} never opened)${skipped}. ` +
        `Report written to HIL_results/.`
    );
    await refreshFileList();
  } catch (err) {
    setStatus(err.message, true);
  }
}

init();
