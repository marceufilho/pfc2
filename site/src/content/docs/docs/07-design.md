---
title: "7. Design"
sidebar:
  order: 7
source: docs/07-design.md
source_sha256: 2ca1fc727d01524b2862ac51ad5c43cf803e290ffd023ef40d64bd043dc2b6ea
---

## Goal

A language in which a small real program can be written, proved and run, with three properties:

1. **It is C.** The source compiles with any C11 compiler, so it can be read, debugged and benchmarked with
   ordinary tools, and the proof-led build can be compared with the plain one.
2. **Nothing is assumed.** Every word PFC2 adds becomes an obligation. A proof may remove a runtime check; a
   failed, timed-out or missing proof never does.
3. **The proof is separate and recomputable.** The released C carries citations; the proof file can be replayed
   offline, and it grants nothing by itself.

## Decisions

| Decision | Reason | Cost |
| --- | --- | --- |
| Stay valid C11; a header erases the added words | one source for both builds; no new parser to trust | the syntax is limited to what a C preprocessor can erase |
| Clauses after the declarator and on the loop | a contract reads as part of the signature; the invariant sits next to the condition it explains | the surface pass must find them in token text |
| `long a[n]` for arrays | C already has this spelling; the length stops being a convention | `n` must be a parameter; no local arrays yet |
| Calls anywhere, lifted left to right before other operands | everyday code; an order C permits | calls under `&&`, `\|\|` and in loop conditions are refused, not reordered |
| Infer counter bounds, prove them | the most common invariant should not be written by hand | one extra solver pass per file |
| `decreases` optional | most small loops are obviously finite; the claim should be explicit when made | a certified program may still not terminate unless every loop has one |
| Globals with computed write sets | callers keep facts about globals a callee cannot touch, with no annotation | no `old()`: an increment cannot be stated in `ensures` |
| Declared functions as the boundary | I/O has to live somewhere; a contract is the honest interface | external contracts are trusted, after a check that they are possible |
| Strings opaque | enough for a console program; no memory model for characters | nothing can be proved about text |
| Trap unless proved, for overflow | lets a bounds proof stand next to unproved arithmetic (see [Proofs](../03-proofs/#two-levels)) | `memory` programs can stop at a trap |
| Two levels, `full` by default | the default promises the most; the weaker promise must be asked for | accumulators over unbounded data need `--level memory` |

## What must be trusted

A certificate from PFC2 is as good as these parts:

| Part | Role | Size |
| --- | --- | --- |
| `pfc2/core/` | parsing, typing, obligation generation, solver encoding, admission, emission | about 3 540 lines |
| `pfc2/preprocess.py`, `clauses.py`, `surface.py`, `text.py`, `elaborate.py` | read the source; turn the added words into contracts | about 1 210 lines |
| `pfc2/gate.py`, `check.py`, `release.py` | decide the verdict; append the boundary lines | about 220 lines |
| Z3 5.3.3 | decides each formula | external |
| clang | compiles the released C; defines the integer layout | external |
| `pfc2/runtime/pfc_rt.c`, external contracts | the world outside the proof | 55 lines plus what you declare |

Two properties limit the damage of a mistake in the surface passes: they only ever *add* obligations, and the
released program is checked a second time without the laws by the same core that emits it. A mistake there can
make a proof fail or state a different contract than you meant; it cannot mark an unproved formula as proved.
A mistake in `core/wp.py`, `core/smt.py` or `core/emit.py` can.

Not in the trusted base: `infer.py`, `bundle.py`, `prove.py`, `llm.py`, the language server and the language model. They produce candidate
invariants, which are text until the checker proves them.

## Relation to PFC

PFC2 grew out of PFC, the compiler of a thesis, and keeps a recording of that compiler's results as a regression
anchor. What changed, what stayed and what did not carry over is in [PFC and PFC2](../10-pfc-and-pfc2/).

## What would come next

In the order that seems to pay most:

1. `old(x)` in `ensures`, so that state changes can be stated.
2. A reference interpreter and a generated-input differential campaign, as the thesis compiler had.
3. Recursion with contracts: the call rule already reasons from the callee's contract alone.
4. Local arrays, then `int` variables.
5. A second solver agreeing on every obligation before a certificate is issued.
6. Structs and pointers: these need a memory model that the current one (typed arrays with lengths) does not have.
