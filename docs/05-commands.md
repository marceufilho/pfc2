# 5. Commands

Run from the repository root. `pfc2` stands for `uv run pfc2` (or just `pfc2` once the package is installed).

| Command | Purpose | Writes |
| --- | --- | --- |
| `check FILE` | prove one file and report | nothing |
| `build FILE` | prove, then write the C and the proof file | `NAME.c`, `NAME.proof.json` |
| `run FILE` | prove a program, compile it with the console runtime, execute it | nothing kept |
| `replay FILE.proof.json` | recompute a proof file offline and compare every field | nothing |
| `elaborate FILE` | print the program with the contracts the checker reads | nothing |
| `lsp` | serve an editor over stdin/stdout ([Editor](11-editor.md)) | nothing |

## Options

| Option | Commands | Meaning |
| --- | --- | --- |
| `--level full\|memory` | check, build, run | `full` (default): every obligation proved. `memory`: unproved overflow traps are kept and listed |
| `--clang PATH` | check, build, run | clang that defines the target integer layout and compiles in `run` (default `clang-19`, or `PFC_CLANG`) |
| `--timeout-ms N` | check, build, run | Z3 budget per obligation, 1 to 60000 (default 10000) |
| `--json` | check, build | print the proof record as JSON instead of the report |
| `--proof FILE` | check, build, run | loop invariants as JSON, or the proof file of an earlier build |
| `--prove` | check, build, run | ask a language model for the invariants; sends the source; needs `OPENAI_API_KEY` in the environment; `PFC2_MODEL` selects the model |
| `--output DIR` | build | directory for the two files (default `build/pfc2/NAME`) |
| `--force` | build | replace the files of an earlier build |
| `--dry-run` | build | prove and report, write nothing |
| `--stdin FILE` | run | file given to the program as standard input |

`--proof` and `--prove` exclude each other. `build` refuses to overwrite existing files without `--force`.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | certified; replay reproduced |
| 1 | refused, a source or toolchain error, an existing output, a replay mismatch |
| 2 | wrong command line |

`run` is the exception: once the program is certified and compiled, `run` exits with the program's own exit code.

Reports go to standard output; diagnostics about the source or the tools go to standard error.

## Reading a refusal

```console
$ pfc2 check examples/wrong/broken_call.c
broken_call.c: not certified (full): 4 obligation(s) not proved
  obligations proved: 3 of 4 (Z3 5.3.3.0)
  broken_call.c:12:12: this call may break the callee's requires [failed]
      cannot prove: (0 <= (-4))
  (3 more obligation(s) depend on the ones above)
```

Each entry gives `file:line:column`, what kind of fact failed, the formula, and when Z3 found one, a state that
violates it. The status in brackets is `failed` (a counterexample exists), `timeout`, `unknown` or `error`; only
`failed` comes with an example. "N more obligation(s) depend on the ones above" counts facts that were proved
only on top of an unproved one.

Errors in the source itself use a rule name:

```console
$ pfc2 check bad.c
bad.c:5:18: [subset-call-order] the call would run conditionally or repeatedly here; assign it to a variable first
```

| Rule prefix | Stage |
| --- | --- |
| `clause-`, `where-`, `law-`, `proof-` | the words PFC2 adds |
| `subset-`, `contract-` | C outside the accepted subset |
| `ir-` | names and types |
| `vc-`, `target-`, `solver-` | proof generation and the target |
| `preprocess-`, `source-`, `parse-` | reading the file |

## Checks for contributors

```console
$ make check        # pytest, ruff, black --check, mypy
$ make site-data    # regenerate the site's bundle, example data and documentation pages
```
