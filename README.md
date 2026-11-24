# PFC2

PFC2 is C11 with contracts. A file is ordinary C plus a few words (`requires`, `ensures`, `invariant`,
`decreases`, `assert`, `where`, `separated`, `law`) that an ordinary C compiler erases through `pfc.h`. The
checker proves every contract and law with Z3 and then either certifies the whole file and emits C without the
proved checks, or refuses it and emits nothing. `pfc2_eval` is the evaluation harness.

"Proved" means Z3 answered `unsat` for the obligation; no proof object is produced. The console runtime
(`pfc2/runtime/pfc_rt.c`), external declarations and the C `main` are unverified and listed as such in every
proof file.

## Requirements

- [uv](https://docs.astral.sh/uv/) and Python 3.11 or 3.12
- `clang-19` (`PFC2_CLANG` selects another) for `build`, `run` and the harness
- optional: `cvc5` (cross-check), Docker (Frama-C/WP), `OPENAI_API_KEY` in the environment (`--prove`, `sources --live`)

## Install and try

```bash
make sync
uv run --locked pfc2 check examples/05_binary_search/binary_search.c     # prove; write nothing
uv run --locked pfc2 build examples/02_fill/fill.c --output build/fill   # certified C and a proof file
uv run --locked pfc2 run examples/09_calculator/calculator.c --stdin examples/09_calculator/stdin.txt
uv run --locked pfc2 replay build/fill/fill.proof.json                   # recompute the proof file offline
uv run --locked pfc2 check examples/wrong/off_by_one.c                   # a refusal, with the failing obligation
```

Levels: `--level full` (default; every obligation proved) and `--level memory` (overflow traps kept and listed).
`examples/examples.json` holds the hand-written expectation of every example.

## Layout

| Path | Content |
| --- | --- |
| `pfc2/` | the compiler: surface passes, `core/` (verification conditions, Z3 adapter, admission, emitter), `include/pfc.h`, console runtime, language server |
| `pfc2_eval/` | the evaluation harness |
| `examples/`, `showcase/` | example programs, including ones that must be refused; the five programs the site opens with |
| `docs/`, `site/` | the user documentation and the site built from it |
| `corpus/` | ported third-party programs and their provenance (see its README) |
| `tests/` | unit and integration tests |
| `validation/freeze/` | SHA-256 inventories of the frozen candidate |

## Evaluation harness

```bash
uv run --locked python -m pfc2_eval SUBCOMMAND --help
```

Every experiment writes a new directory (`--output`), refuses an existing one, and supports `--dry-run`.

| Subcommand | What it does |
| --- | --- |
| `selfcheck` | the reference interpreter against the source compiled as plain C |
| `differential` | certified, checked and plain C against the interpreter on generated programs; expected traps; proof replay |
| `breakit` | each `requires` conjunct removed alone; what depended on it must be lost |
| `inject` | damaged loop invariants; none may be admitted |
| `robustness` | renaming, reordering, operand swap and re-layout must not change the verdict |
| `crosscheck` | every query answered again by cvc5 |
| `surfaces` | the editor and browser entry points against the command line |
| `verifier` | Frama-C/WP on hand-written ACSL beside PFC2's verdicts (Docker) |
| `sources` | invariant sources on a sealed loop set: none, inference, Houdini, dynamic inference, a language model |
| `runtime` | run time of the plain, checked and certified builds |
| `mutate` | every mutant of the engine against the tests and a differential run |
| `corpus` | upstream tests and code mutants against ported units, tests versus proofs |
| `generate`, `interpret`, `heldout`, `candidate` | utilities |

## Site

`site/` is a static site (Astro) with a playground that runs the checker in the browser, the documentation of
`docs/`, a lock whose single combination is proved (`showcase/lock`) and a game that cannot be won.
`.github/workflows/site.yml` builds it and deploys it to GitHub Pages on every push to `main`: enable Pages in the
repository settings with "GitHub Actions" as the source. The address is `https://<owner>.github.io/pfc2/`; if the
owner or the repository name differ, change `site` and `base` in `site/astro.config.mjs`.

```bash
make site-build     # needs Node 24 and pnpm; writes site/dist
make site-test      # browser tests
```

## Records

`records/` holds the registered design, the amendment log and, for every run behind a reported result, its
configuration, summary and manifest. The raw runs are not published (see `records/README.md`).

## Tests

```bash
make check          # pytest, ruff, black --check, mypy
make freeze-check   # the tree is the frozen candidate
```

## Notes

- `pfc2/`, `pyproject.toml`, `uv.lock` and `.python-version` are the frozen candidate `pfc2-v3`
  (`validation/freeze/protected.sha256`); they are unchanged here. Comments that cite decision, amendment or
  design-section numbers refer to development records that are not part of this repository.
- Not supported: `old()` in `ensures`, quantifiers in contracts, recursion, structs, general pointers, global
  arrays, variables other than `long` and `_Bool`, `switch`, `do`, `goto`, `?:` and bitwise operators.
  Unsupported input is refused with a rule and a position, never guessed.
- Third-party material keeps its licence (`corpus/README.md`); the Zilu-derived programs are GPL-2.0.
  No licence has been chosen yet for the rest of the repository.
