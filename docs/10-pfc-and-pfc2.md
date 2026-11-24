# 10. PFC and PFC2

PFC2 grew out of **PFC**, the proof-guided compiler built for a thesis. This page says what each one is, what
changed, and what did not carry over.

## In one paragraph

PFC is a research artifact. It answers one question, on six numeric kernels: can a compiler remove a runtime
check only where a machine-checked proof says it may, with every removal traceable, even when the loop
invariants come from an untrusted source? It was frozen and then evaluated at length. PFC2 takes the same
principle and turns it into a language you can write small programs in. It has its own copy of the compiler,
changed where a usable language needed it, and it has not been evaluated the way PFC was.

## Side by side

| | PFC | PFC2 |
| --- | --- | --- |
| Purpose | show auditable check removal, and measure it | write, prove and run small programs |
| Status | frozen (freeze-v5); the subject of the published evaluation | research prototype; own tests only |
| Contracts | `REQUIRES(p);` `ENSURES(q);` `INVARIANT(i);` as the first statements of a body | `requires(p)` `ensures(q)` on the signature, `invariant(i)` on the loop |
| Result | `RESULT` | `result` |
| Arrays | `long a[], long a_len`, the length by naming convention | `long a[n]`; `0 <= n` is a checked precondition; local arrays; `char` and `int` elements |
| Statements | explicit assignments only (`i = i + 1`); no `break` | also `i++`, `+=`, `break`, `continue` |
| Operators | `+ - * /`; one operator of a kind per expression can be proved | also `%`; `a + b + c` is checked operator by operator |
| Calls | only as a whole initializer, assigned value or return value | anywhere in an expression, or as a statement |
| State | parameters and locals | also file-scope globals |
| Outside world | none: kernels only, driven by separate host C | declared functions under contracts; strings; console I/O; `main` |
| Properties | contracts | contracts, `where` types, and `law`s proved for every input |
| Loop proofs | written by hand, or proposed by a language model | written, inferred for counters, supplied as data, or proposed by a model |
| Termination | not addressed | `decreases(e)`, optional |
| Reading the source | external `cpp`; positions are those of its output | built-in preprocessor; positions are those of the file |
| What is produced | plain, checked or verified C; optional `restrict`/`assume` facts | certified C or nothing; a separate proof file |
| When a proof is missing | verified C is still printed, with the check kept | the file is refused; at `memory` an overflow trap may stay, listed |
| Removing a bounds check | needs the arithmetic that feeds it proved too | relies on the overflow trap that stays at unproved arithmetic |
| Tools | `pfc` commands, directory workflows, benchmark and proposer experiments | `pfc2 check/build/run/replay`, language server, playground |

## What changed in the compiler

PFC2's core (`pfc2/core/`) began as a copy of sixteen PFC modules.

**Removed.** The plain mode; the `restrict` and `assume` compiler facts and their authorization; the external
preprocessor boundary; reports, benchmark, differential and experiment code; the convention that an array's
length is the parameter named `<array>_len` (still accepted, no longer required).

**Added to the core.** `%`; `break` and `continue`; local arrays with their initial values; `char` and `int`
elements with a required proof for every narrowing store; distinct positions for chained operators; array types
with a length parameter; `++`, `--`, compound assignment and calls inside
expressions, spelled out before validation; globals with per-function write sets; declared-only functions and a
consistency check of their contracts; decimal literals up to 64 bits with a target check.

**Added around the core.** The surface passes for the new words; elaboration of `where`, `law` and `decreases`;
inference of counter bounds; the strict gate with two levels; the proof file and `replay`; the console runtime;
the language server; the browser entry point.

**One rule changed on purpose.** PFC keeps a bounds or division check whenever arithmetic that can influence
it is not proved free of overflow. PFC2 removes the check once its own obligation is proved, because every
arithmetic operation without an overflow proof keeps a runtime trap in the emitted C: an execution either stops
at that trap or has computed exactly the values the proof reasoned about. [Proofs](03-proofs.md#two-levels) gives
the argument; `tests/test_soundness.py` gives ten constructed programs, a sanitizer-backed comparison with fully
checked C, and a check that the comparison notices a dropped trap.

## What stays the same

- Only `unsat` of the negated obligation is a proof. Failures, timeouts, `unknown` and errors keep the check.
- A proof removes a check only if it is the proof of that operation, in that program, for that target.
- Every removed check is cited in the emitted C.
- Whatever proposes an invariant (a person, inference, a file, a model) is untrusted; the checker decides.
- A contract no input can satisfy is refused, so nothing is certified vacuously.

`tests/test_v5_agreement.py` holds PFC2 to this on PFC's own ground: for the 48 programs of PFC's subset it
compares PFC2's obligations, statuses, decisions and emitted code with a recording of what PFC produced. 44 are
identical; four differ on purpose (PFC2 accepts `++`, `break` and `continue`, and names the refusal of an
uninitialised local array differently).

## What PFC has that PFC2 does not

The evidence. PFC was tested with a thousand generated inputs per kernel against an independent interpreter,
break-it experiments on every precondition, injection of false invariants, mutation testing of the compiler and
of the harness, a second solver, an independent proof tool, and a study on an externally selected set of
programs. None of that was run on PFC2, and none of its results describe PFC2. PFC also has what a study needs
and a language does not: three build modes with identical flags, fact ablations, benchmark drivers and sealed
experiment records.

## What PFC2 has that PFC does not

A syntax meant to be read; proofs about whole small programs, not only kernels; inference; termination; laws;
a proof file that is separate from the code and replayable; an editor integration and a playground; and
declared functions, with a check that their contracts are possible.

## Which one to cite or use

- For a claim about measured soundness or the experiments: PFC, and its paper.
- For writing and checking a program: PFC2, with [Limits](09-limits.md) in mind.
