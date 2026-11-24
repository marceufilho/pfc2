// Playground: an editor, the PFC2 checker running in the page, and panels for its verdict.
import { basicSetup, EditorView } from "codemirror";
import { cpp } from "@codemirror/lang-cpp";
import { HighlightStyle, syntaxHighlighting } from "@codemirror/language";
import { type Diagnostic, setDiagnostics } from "@codemirror/lint";
import { tags } from "@lezer/highlight";
import { analyze, cancel, onProgress } from "./engine";
import { dataUrl, pageUrl } from "./paths";

// Editor colours come from the site's theme variables, so light and dark mode both stay legible.
const editorTheme = EditorView.theme({
  "&": { backgroundColor: "transparent", color: "var(--sl-color-text)" },
  ".cm-gutters": { backgroundColor: "var(--sl-color-gray-6)", color: "var(--sl-color-gray-3)", border: "none" },
  ".cm-activeLine, .cm-activeLineGutter": { backgroundColor: "color-mix(in srgb, var(--pfc-sky) 14%, transparent)" },
  ".cm-cursor": { borderLeftColor: "var(--sl-color-text)" },
  "&.cm-focused .cm-selectionBackground, .cm-selectionBackground, ::selection": {
    backgroundColor: "color-mix(in srgb, var(--pfc-blue) 30%, transparent)",
  },
});
const editorHighlight = HighlightStyle.define([
  { tag: [tags.keyword, tags.typeName, tags.modifier], color: "var(--pfc-code-keyword)" },
  { tag: [tags.number, tags.bool], color: "var(--pfc-code-number)" },
  { tag: [tags.string, tags.processingInstruction], color: "var(--pfc-code-string)" },
  { tag: tags.comment, color: "var(--sl-color-gray-3)", fontStyle: "italic" },
  { tag: tags.function(tags.variableName), color: "var(--pfc-code-function)" },
]);

export const escapeHtml = (text: unknown): string =>
  String(text).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]!);

function codeLines(text: string): string {
  return text
    .split("\n")
    .map((line) => {
      const kind = line.includes("// proved: obligation")
        ? "proved"
        : line.includes("__builtin_trap")
          ? "trap"
          : line.includes("// entry check") || line.includes("pfc_entry_")
            ? "entry"
            : "";
      return `<span class="${kind}">${escapeHtml(line) || " "}</span>`;
    })
    .join("");
}

const encodeSource = (text: string): string =>
  btoa(String.fromCharCode(...new TextEncoder().encode(text))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
function decodeSource(text: string): string | null {
  try {
    const binary = atob(text.replace(/-/g, "+").replace(/_/g, "/"));
    return new TextDecoder().decode(Uint8Array.from(binary, (c) => c.charCodeAt(0)));
  } catch {
    return null;
  }
}

interface Program {
  id: string;
  group: string;
  name: string;
  level: "full" | "memory";
  source: string;
}

const GROUPS: Record<string, string> = {
  showcase: "Start here",
  functions: "Functions",
  programs: "Programs",
  wrong: "Programs that must be refused",
};
const STAGES: Record<string, string> = {
  runtime: "loading Python (WebAssembly)…",
  solver: "loading Z3 5.3.3…",
  compiler: "loading the checker…",
  ready: "checking…",
};
const TABS = [
  ["report", "Report"],
  ["c", "Certified C"],
  ["elaborated", "What the checker reads"],
  ["record", "Proof file"],
] as const;
type Tab = (typeof TABS)[number][0];
const EXPERIMENTS: [string, string][] = [
  ["requires", "Remove every requires(...)"],
  ["ensures", "Remove every ensures(...)"],
  ["invariant", "Remove every invariant(...)"],
  ["decreases", "Remove every decreases(...)"],
];

let catalog: Promise<{ programs: Program[] }> | null = null;
const loadCatalog = () =>
  (catalog ??= Promise.all(["programs.json", "showcase.json"].map((name) => fetch(dataUrl(name)).then((r) => r.json()))).then(
    ([examples, showcase]) => ({ programs: [...showcase.programs, ...examples.programs] }),
  ));

/** Remove every `word(...)` clause, matching parentheses; text inside strings is not a concern for clauses. */
export function removeClauses(source: string, word: string): string {
  const pattern = new RegExp(`\\b${word}\\s*\\(`, "g");
  let result = "";
  let position = 0;
  for (let match = pattern.exec(source); match; match = pattern.exec(source)) {
    let depth = 0;
    let end = match.index + match[0].length - 1;
    for (; end < source.length; end++) {
      if (source[end] === "(") depth++;
      else if (source[end] === ")" && --depth === 0) break;
    }
    if (end >= source.length) break;
    // Drop the clause and, when it stood alone on its line, the line itself.
    const lineStart = source.lastIndexOf("\n", match.index) + 1;
    const lineEnd = source.indexOf("\n", end);
    const alone = source.slice(lineStart, match.index).trim() === "" && source.slice(end + 1, lineEnd).trim() === "";
    result += source.slice(position, alone ? lineStart : match.index).replace(/[ \t]+$/, alone ? "" : " ");
    position = alone && lineEnd >= 0 ? lineEnd + 1 : end + 1;
    pattern.lastIndex = position;
  }
  return result + source.slice(position);
}

function place(line: number | null, column: number | null): string {
  if (line == null) return "";
  return `<button class="loc" data-line="${line}" data-column="${column ?? 1}">${line}:${column ?? 1}</button>`;
}

function renderReport(result: any): string {
  const record = result.record;
  const proved = record.obligations.filter((o: any) => o.status === "proved").length;
  const guards = record.guards.filter((g: any) => g.removed).length;
  const traps = record.overflow.filter((g: any) => g.removed).length;
  const state = result.accepted ? "ok" : "bad";
  let html = `<div class="chips">
    <span class="chip ${state}">${result.accepted ? "certified" : "not certified"} (${escapeHtml(result.level)})</span>
    <span class="chip ${proved === record.obligations.length ? "ok" : "bad"}">obligations proved: ${proved}/${record.obligations.length}</span>
    <span class="chip">bounds/division checks removed: ${guards}/${record.guards.length}</span>
    <span class="chip">overflow checks removed: ${traps}/${record.overflow.length}</span>
    <span class="chip">loops proved to terminate: ${record.termination.proved.length}/${record.termination.loops}</span>
  </div>`;
  if (!result.accepted) html += `<p><strong>${escapeHtml(result.reason)}</strong></p>`;
  const primary = result.blockers.filter((b: any) => !String(b.status).startsWith("depends"));
  if (primary.length) {
    html += `<table><thead><tr><th>Where</th><th>What</th><th>Cannot prove</th></tr></thead><tbody>`;
    for (const blocker of primary) {
      html += `<tr><td>${place(blocker.line, blocker.column)}</td>
        <td>${escapeHtml(blocker.meaning)} <span class="status ${escapeHtml(blocker.status)}">${escapeHtml(blocker.status)}</span></td>
        <td><code>${escapeHtml(blocker.goal)}</code>${blocker.example ? `<div class="model">for example: ${escapeHtml(blocker.example)}</div>` : ""}</td></tr>`;
    }
    html += `</tbody></table>`;
    const dependent = result.blockers.length - primary.length;
    if (dependent) html += `<p class="muted">${dependent} more obligation(s) depend on the ones above.</p>`;
  }
  if (record.inferred.length) {
    html += `<h4>Inferred and proved</h4><ul>`;
    for (const item of record.inferred) {
      html += `<li>${escapeHtml(item.function)}, loop at ${place(item.line, 1)}: <code>${escapeHtml(item.invariant)}</code></li>`;
    }
    html += `</ul>`;
  }
  if (result.accepted && record.retained_traps.length) {
    html += `<h4>Overflow traps kept</h4><ul>`;
    for (const trap of record.retained_traps) html += `<li>${place(trap.line, trap.column)} <code>${escapeHtml(trap.condition)}</code></li>`;
    html += `</ul>`;
  }
  const unverified = record.unverified.functions;
  if (unverified.length) {
    html += `<h4>Not verified</h4><p>Declared functions, called under their contracts: <code>${escapeHtml(unverified.join(", "))}</code>.</p>`;
    const open = record.unverified.contracts.filter((c: any) => c.total !== "total");
    if (open.length) {
      html += `<p class="muted">Possible, but not shown to have a result for every input: <code>${escapeHtml(open.map((c: any) => c.function).join(", "))}</code>.</p>`;
    }
  }
  if (!result.accepted && result.level === "full" && result.memory_would_pass) {
    html += `<p class="muted">At level <strong>memory</strong> this program is certified: memory safety is proved and the unproved overflow traps are kept.</p>`;
  }
  return html + `<h4>Report</h4><pre>${escapeHtml(result.report)}</pre>`;
}

function renderTab(tab: Tab, result: any): string {
  if (tab === "report") return renderReport(result);
  if (tab === "c") {
    return result.c == null
      ? `<p class="muted">A refused program releases no C.</p>`
      : `<pre>${codeLines(result.c)}</pre>`;
  }
  if (tab === "elaborated") return `<pre>${escapeHtml(result.elaborated)}</pre>`;
  const { preprocessed, c, ...rest } = result.record;
  return `<p class="muted">The proof file without its two long text fields (the program and the emitted C).</p><pre>${escapeHtml(JSON.stringify(rest, null, 2))}</pre>`;
}

export async function mount(root: HTMLElement): Promise<void> {
  if (root.dataset.mounted) return;
  root.dataset.mounted = "1";
  root.innerHTML = `
    <div class="bar">
      <select class="program" aria-label="Example"></select>
      <select class="experiment" aria-label="Experiment"><option value="">Experiments…</option></select>
      <label>level <select class="level" aria-label="Level"><option value="full">full</option><option value="memory">memory</option></select></label>
      <button class="primary run">Check</button>
      <button class="stop" hidden>Cancel</button>
      <button class="share" title="Copy a link to this program">Share</button>
      <span class="state muted" role="status"></span>
    </div>
    <div class="panes">
      <div class="editor"></div>
      <div class="out">
        <div class="tabs" role="tablist"></div>
        <div class="body"><p class="muted">Edit the program and press <strong>Check</strong>. The checker (Python, Z3 and PFC2 as WebAssembly, about 20 MB) is loaded on first use.</p></div>
      </div>
    </div>
    <div class="foot">Live run in your browser. The same checker as the <code>pfc2</code> command, with one declared difference: the integer layout is fixed (32-bit int, 64-bit long) and no clang is queried. Programs are checked here, not run. PFC2 is a research prototype: read the <a href="${pageUrl("docs/09-limits/")}">limits</a>.<span class="prov"></span></div>`;
  const $ = <T extends HTMLElement>(selector: string) => root.querySelector<T>(selector)!;
  const programSelect = $<HTMLSelectElement>(".program");
  const experimentSelect = $<HTMLSelectElement>(".experiment");
  const levelSelect = $<HTMLSelectElement>(".level");
  const runButton = $<HTMLButtonElement>(".run");
  const stopButton = $<HTMLButtonElement>(".stop");
  const shareButton = $<HTMLButtonElement>(".share");
  const state = $(".state");
  const body = $(".body");
  const tabs = $(".tabs");
  let tab: Tab = "report";
  let last: any = null;
  let current: Program | null = null;

  const view = new EditorView({
    parent: $(".editor"),
    doc: "",
    extensions: [basicSetup, cpp(), editorTheme, syntaxHighlighting(editorHighlight), EditorView.lineWrapping],
  });
  const getSource = () => view.state.doc.toString();
  const setSource = (text: string) => view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: text } });

  tabs.innerHTML = TABS.map(([id, label]) => `<button role="tab" data-tab="${id}">${label}</button>`).join("");
  experimentSelect.innerHTML += EXPERIMENTS.map(([id, label]) => `<option value="${id}">${label}</option>`).join("");
  const paint = () => {
    tabs.querySelectorAll<HTMLButtonElement>("button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.tab === tab)));
    if (last?.ok) body.innerHTML = renderTab(tab, last);
  };
  tabs.addEventListener("click", (event) => {
    const button = (event.target as HTMLElement).closest<HTMLButtonElement>("button[data-tab]");
    if (button) (tab = button.dataset.tab as Tab), paint();
  });
  body.addEventListener("click", (event) => {
    const button = (event.target as HTMLElement).closest<HTMLButtonElement>("button.loc");
    if (!button) return;
    const line = Math.min(Number(button.dataset.line), view.state.doc.lines);
    const info = view.state.doc.line(Math.max(line, 1));
    const position = Math.min(info.from + Number(button.dataset.column) - 1, info.to);
    view.dispatch({ selection: { anchor: position, head: info.to }, scrollIntoView: true });
    view.focus();
  });
  paint();

  /** Underline what the checker could not prove, and the traps it kept, where they stand in the source. */
  function mark(result: any): void {
    const found: Diagnostic[] = [];
    const add = (line: number | null, column: number | null, severity: "error" | "warning", message: string) => {
      if (line == null || line < 1 || line > view.state.doc.lines) return;
      const info = view.state.doc.line(line);
      const from = Math.min(info.from + (column ?? 1) - 1, info.to);
      const word = /^[A-Za-z_][A-Za-z0-9_]*/.exec(view.state.doc.sliceString(from, info.to));
      found.push({ from, to: Math.min(from + (word ? word[0].length : 1), info.to), severity, message });
    };
    if (result?.ok) {
      for (const blocker of result.blockers) {
        if (String(blocker.status).startsWith("depends")) continue;
        const example = blocker.example ? ` For example: ${blocker.example}` : "";
        add(blocker.line, blocker.column, "error", `${blocker.meaning}. Cannot prove: ${blocker.goal}.${example}`);
      }
      for (const trap of result.accepted ? result.record.retained_traps : []) {
        add(trap.line, trap.column, "warning", "overflow is not proved here; the emitted C keeps a runtime trap");
      }
    } else if (result) {
      add(result.diagnostic.line, result.diagnostic.column, "error", `${result.diagnostic.rule}: ${result.diagnostic.message}`);
    }
    view.dispatch(setDiagnostics(view.state, found));
  }
  onProgress((stage) => {
    if (runButton.disabled) state.textContent = STAGES[stage] ?? stage;
  });

  async function run(): Promise<void> {
    runButton.disabled = true;
    stopButton.hidden = false;
    state.textContent = "starting…";
    const started = performance.now();
    try {
      const reply = await analyze({
        kind: "pfc2",
        source: getSource(),
        name: current?.name ?? "program.c",
        level: levelSelect.value as "full" | "memory",
      });
      last = reply.result;
      mark(last);
      root.dispatchEvent(new CustomEvent("pfc2-result", { detail: reply, bubbles: true }));
      const seconds = ((performance.now() - started) / 1000).toFixed(1);
      if (last.ok) {
        state.textContent = `${last.accepted ? "certified" : "not certified"} · ${seconds} s`;
        paint();
      } else {
        const d = last.diagnostic;
        state.textContent = `source refused · ${seconds} s`;
        body.innerHTML =
          `<div class="diag"><strong>${escapeHtml(d.rule)}</strong> ${d.line == null ? "" : "at " + place(d.line, d.column)}` +
          `<br>${escapeHtml(d.message)}</div><p class="muted">PFC2 refuses what is outside its language instead of guessing a meaning.</p>`;
      }
      const p = last.provenance;
      $(".prov").textContent = ` Engine: Z3 ${p.z3}, Python ${p.python} (${p.platform}).`;
    } catch (error) {
      state.textContent = "";
      body.innerHTML = `<div class="diag">${escapeHtml((error as Error).message)}</div>`;
    } finally {
      runButton.disabled = false;
      stopButton.hidden = true;
    }
  }
  runButton.addEventListener("click", run);
  stopButton.addEventListener("click", () => cancel());
  shareButton.addEventListener("click", async () => {
    history.replaceState(null, "", `#level=${levelSelect.value}&src=${encodeSource(getSource())}`);
    try {
      await navigator.clipboard.writeText(location.href);
      state.textContent = "link copied";
    } catch {
      state.textContent = "the link is in the address bar";
    }
  });

  const { programs } = await loadCatalog();
  for (const [group, label] of Object.entries(GROUPS)) {
    const options = programs.filter((program) => program.group === group);
    if (!options.length) continue;
    const element = document.createElement("optgroup");
    element.label = label;
    for (const program of options) element.append(new Option(program.id, program.id));
    programSelect.append(element);
  }
  const select = (id: string) => {
    current = programs.find((program) => program.id === id) ?? programs[0] ?? null;
    if (!current) return;
    programSelect.value = current.id;
    levelSelect.value = current.level;
    setSource(current.source);
    last = null;
    mark(null);
    body.innerHTML = `<p class="muted">Press <strong>Check</strong>.</p>`;
    state.textContent = "";
  };
  programSelect.addEventListener("change", () => select(programSelect.value));
  experimentSelect.addEventListener("change", () => {
    const word = experimentSelect.value;
    experimentSelect.value = "";
    if (!word) return;
    setSource(removeClauses(getSource(), word));
    void run();
  });
  // #example=ID opens an example; #src=... (with optional level=) opens a shared program.
  const hash = new URLSearchParams(location.hash.slice(1));
  const shared = hash.get("src") ? decodeSource(hash.get("src")!) : null;
  select(hash.get("example") ?? root.dataset.program ?? "01_count/count");
  if (shared != null) {
    current = { id: "shared", group: "", name: "program.c", level: "full", source: shared };
    programSelect.selectedIndex = -1;
    setSource(shared);
    if (hash.get("level") === "memory") levelSelect.value = "memory";
  }
}
