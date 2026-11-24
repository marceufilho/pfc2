# Corpora

Programs the harness reads. Sealed directories carry `HELDOUT.sha256` and are checked before every run
(`python -m pfc2_eval heldout verify DIR`); `SELECTION.json` or `PROVENANCE.json` records the upstream commit, the
selection rule and every exclusion.

| Directory | Content | Origin | Licence |
| --- | --- | --- | --- |
| `exercism/`, `exercism-ports/` | practice exercises ported to PFC2, with contracts | [exercism/c](https://github.com/exercism/c) at `1675b02c` | MIT |
| `verina/`, `verina-ports/` | Verina tasks ported to PFC2, with contracts | [sunblaze-ucb/verina](https://github.com/sunblaze-ucb/verina) at `66b3ce50` | Apache-2.0 |
| `upstream/verina-c/` | the Verina tests as C test files (generated from the Verina task data) | same | Apache-2.0 |
| `upstream/unity/` | the Unity test framework used by those tests | ThrowTheSwitch/Unity | MIT |
| `heldout-loops/` | loops ported from SV-COMP `array-fpi` and `loop-invgen` | sv-benchmarks at `d36a1c91` | Apache-2.0 |
| `thesis-heldout/` | 43 array programs ported from SV-COMP | sv-benchmarks | Apache-2.0 |
| `thesis-derived/kernels`, `acsl` | six kernels; eight functions of *ACSL by Example* | Fraunhofer FOKUS (acsl) | MIT (acsl) |
| `thesis-derived/zilu*` | Zilu loops and variants | SV-COMP `c/loop-zilu` | GPL-2.0 |
| `independent-verifier/` | hand-written ACSL transcriptions for Frama-C/WP | this project | as the repository |

Licence texts are in `licenses/`.

## Upstream checkouts (not stored)

The corpus study runs the upstream Exercism tests, which are fetched, not committed:

```bash
git clone https://github.com/exercism/c corpus/upstream/exercism-c
git -C corpus/upstream/exercism-c checkout 1675b02c310198e9752e516ee1a2294b76a37f84
```

```bash
uv run --locked python -m pfc2_eval corpus corpus/exercism \
    --upstream corpus/upstream/exercism-c/exercises/practice --output out/corpus-exercism
uv run --locked python -m pfc2_eval corpus corpus/verina --upstream corpus/upstream/verina-c --output out/corpus-verina
```
