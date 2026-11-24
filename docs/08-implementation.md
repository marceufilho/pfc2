# 8. Implementation

## Pipeline

```text
source.c
   │  frontend.py      read (bounded, UTF-8)
   │  preprocess.py    comments → spaces; pfc.h / pfc_rt.h / stdbool.h; #ifdef; #define NAME value
   ▼
preprocessed text
   │  clauses.py       requires / ensures / invariant / decreases / assert / separated → markers
   │                   string literals → pfc2_str_K(); int main → pfc2_main; declarations without a body
   │  surface.py       where(...) → markers; law → function; supplied invariants
   ▼
C the core can parse   (every rewrite stays on its line, so positions remain those of the source)
   │  core/parse.py    pycparser, then core/desugar.py: ++, +=, calls lifted into locals
   │  core/subset.py   reject anything outside the subset, by rule and position
   │  core/lower.py    names, types, array lengths, globals → typed structured IR (core/ir.py)
   ▼
IR program
   │  elaborate.py     where types → assertions and invariants; laws; decreases → ghost measure;
   │                   `a[n]` → requires(0 <= n); the released program (no laws, no ghosts)
   │  infer.py         candidate counter bounds, kept only if proved
   ▼
Unit  (program to prove, program to release)
   │  core/vc.py, core/wp.py    obligations per path; loops by induction; calls by contract;
   │                            possibility of each declared function's contract
   │  core/smt.py               Z3 query per obligation; statuses; counterexamples
   │  core/authorization.py     which obligations are admitted with their dependencies
   │  core/emit.py              C with each check removed only where its proof is admitted
   │  gate.py                   level verdict; a refusal carries no C
   │  release.py                append string constants and the C entry point
   ▼
Certification  →  cli.py (report, files, run)  ·  proof.py (proof file, replay)
```

`check.check(unit, target, level, timeout_ms)` is the single function that goes from a `Unit` to a verdict. The
CLI, the prover loop, `replay`, the playground and the language server all call it, so they cannot disagree.

## Modules

| Module | Responsibility |
| --- | --- |
| `text.py` | positions in preprocessed text; literal and parenthesis scanning |
| `clauses.py` | the clause words, strings, `main`, declared-only functions |
| `surface.py` | `where`, `law`, supplied invariants |
| `elaborate.py` | IR-level meaning of the added words; `Unit` |
| `infer.py` | counter-bound candidates and their selection |
| `gate.py` | `certify`: verdict per level, blockers |
| `check.py` | infer, certify, release |
| `release.py` | boundary lines |
| `proof.py` | proof file and `replay` |
| `bundle.py`, `prove.py` | invariants as data; the bounded model loop |
| `frontend.py`, `preprocess.py` | reading the file; PFC2's own preprocessing |
| `cli.py`, `report.py` | commands, `run`; the text report |
| `web.py` | the same path as one pure function, for the playground |
| `llm.py` | the single adapter to the model service used by `--prove` |
| `lsp/analysis.py`, `lsp/server.py` | editor facts from source text; the protocol around them |
| `core/desugar.py` | everyday C spelled out on the parsed tree |
| `core/parse.py`, `subset.py` | normalised syntax tree; subset rules |
| `core/ir.py`, `lower.py` | IR and typed lowering |
| `core/vc.py`, `wp.py` | terms, obligations, path semantics |
| `core/smt.py`, `target.py` | encoding, solving, cache, target layout |
| `core/authorization.py`, `emit.py` | admission and emission |
| `include/pfc.h`, `pfc_rt.h`, `runtime/pfc_rt.c` | the header pair and the console runtime |

## Rules the code keeps

- **Fail closed.** Only `unsat` of the negated obligation is a proof. Every other solver outcome keeps the check.
- **Exact matching.** A proof removes a check only if it is the proof of that operation, at that position, in
  that program, for that target and solver configuration.
- **Positions survive.** Surface passes blank text in place and insert markers on the same line. A diagnostic
  therefore points into the file you wrote. (Columns after an insertion on the same line can shift.)
- **Pure core.** `core/` does no I/O except `environment.py` and `target.py`, which ask clang for its integer layout. The surface
  passes, elaboration, inference, the gate and the proof file are pure functions of their inputs.
- **Boundaries.** Only `core/environment.py`, `core/target.py`, `llm.py`, `cli.py` and `lsp/server.py` may start a
  process or open a connection; the core never imports the language layer. `tests/test_import_independence.py`
  enforces both.

## Adding a language feature

Most features fit one of three places. Pick the lowest one that works.

1. **Spelling only** (the feature is another way to write something the IR already has): `clauses.py` or
   `core/desugar.py`. Example: `i++`. Test by comparing the lowered program with the explicit spelling written by
   hand (`tests/test_everyday_c.py`).
2. **Meaning expressible with existing contracts**: `elaborate.py`. Example: `decreases` becomes a ghost local
   and two assertions. Test with programs that must certify and programs that must be refused
   (`tests/test_proof_help.py`).
3. **New meaning**: `core/ir.py`, `lower.py`, `wp.py`, `emit.py`. Example: globals. This changes the trusted
   core; it needs hand-derived expectations, a program that must be refused for each new way to be wrong, and a
   run of the agreement test to show the old subset is untouched (`tests/test_programs.py`).

Then add an example and a `wrong/` example, the line in `examples.json`, and the paragraph in
[Language](02-language.md).

## Tests

| File | What it pins down |
| --- | --- |
| `test_v5_agreement.py` | the core equals a recording of the thesis compiler on that compiler's subset |
| `test_preprocess.py` | the built-in preprocessor; real `cpp` as an oracle on every example |
| `test_clauses.py`, `test_surface.py` | the surface rewrites, their positions and their refusals |
| `test_everyday_c.py` | `++`, `+=`, lifted calls, array lengths, literals |
| `test_elaborate.py` | contracts produced from `where` and laws |
| `test_proof_help.py` | inferred bounds, `decreases`, `0 <= n` for arrays |
| `test_programs.py` | globals, external functions, strings, `main`, `run` (real clang) |
| `test_traps.py`, `test_soundness.py` | a kept overflow trap stops the run before a removed check matters: ten programs, sanitizers, a dropped-trap check |
| `test_externals.py` | impossible contracts on declared functions are refused, eleven hand-classified contracts about array contents included |
| `test_language_v1.py` | chained operators, `%`, `break`/`continue`, local arrays, `char`/`int` elements: a certifying program, a refused neighbour and a sanitizer-backed run for each |
| `test_review_v1.py` | the findings of the review of the language growth: termination counting, trigraphs, prefix operators in chains, long write chains |
| `test_audit_defects.py` | the defects of the 2026-11-18 review, and a guard for each class: generated names, layout independence, calls evaluated once |
| `test_semantics.py` | globals, external writes, nested termination, inference: one certifying program and one refused neighbour each |
| `test_lsp_analysis.py`, `test_lsp_server.py` | editor diagnostics, hover and symbols; one conversation over the real protocol |
| `test_gate.py`, `test_proof.py`, `test_prove.py`, `test_cli.py` | levels, proof files, replay, bundles, commands |
| `test_web.py` | the playground entry point equals the command-line path on every example |
| `test_integration.py` | every example: verdict, replay, certified versus plain C |
| `test_docs.py` | the programs printed in this documentation get the verdict the page states |
| `test_import_independence.py` | package boundaries |

Expectations are written by hand from the program text. They are never regenerated from the tool's output.
