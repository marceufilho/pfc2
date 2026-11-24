---
title: "9. Limits"
sidebar:
  order: 9
source: docs/09-limits.md
source_sha256: 8b056b72ce22c32f9d593226257100291d54fa0810cfa7fd5cecb5b82ada28d4
---

Read this page before relying on a PFC2 certificate.

## What a certificate means

For a file certified at `full`: for every input allowed by the contracts, every function defined in the file
performs no out-of-bounds array access, no division by zero, no signed overflow, calls every function within its
contract, returns values that satisfy its `ensures`, and every `assert` and law holds — **provided** the callers
PFC2 did not check respect the contracts, the declared external functions behave as their contracts say, the
arrays passed in are as long as declared, **arrays of different element types passed in do not overlap**, and the tools listed under
[what must be trusted](../07-design/#what-must-be-trusted) are correct.

At `memory` the same holds except that an execution may stop at a listed overflow trap.

The condition on element types matters only for code PFC2 did not check. Inside a PFC2 file a `char` array and a
`long` array are always different objects. A host C caller, however, can legally pass the same storage as
`long *` and as `char *`; a function certified by PFC2 is then outside its certificate, and can read out of
bounds. `separated(a, s)` says nothing when the element types differ. This is the typed memory model that
deductive verifiers for C commonly use; it is an assumption, not something PFC2 detects.

## What it does not mean

- **Termination**, unless every loop has a proved `decreases`. A certified program may loop forever. A loop is
  counted as proved to terminate only when every loop inside it and every function it calls is too; declared
  functions are assumed to return.
- **Anything about the outside world.** `pfc_rt.c`, the operating system, and every function you declare
  without a body are trusted as described by their contracts.
- **Anything about text.** Strings are opaque values.
- **That the contract is the one you wanted.** PFC2 proves what is written. A weak `ensures` proves little.
- **That PFC2 itself is right.** See the next section.

## How much evidence stands behind PFC2

- The compiler core began as a copy of PFC, the thesis compiler ([PFC and PFC2](../10-pfc-and-pfc2/)). On a
  recording of PFC's results for the 48 programs of its subset, PFC2 agrees on 44 and differs on four on purpose
  (it accepts `++`, `break` and `continue`, and refuses an uninitialised local array under a new rule). That agreement says nothing about the features PFC2 added.
- The added features rest on PFC2's own tests, including concrete runs of certified binaries against plain C
  builds and against inputs that must trap.
- A review of the engine on 2026-11-18 found six defects, one of which certified an out-of-bounds read. They are
  fixed and kept as tests (`tests/test_audit_defects.py`). A review that finds six defects is evidence that more exist.
- A second review, of the language growth of 2026-11-18, ran about 230 generated programs through certified and
  plain C without a difference and found one assumption that had to be stated (element types, above), one false
  termination report and five smaller defects, fixed and kept in `tests/test_review_v1.py`.
- The first shake-down of the evaluation harness found two more defects, neither about soundness: proof files
  differed from one process to the next (a set of names was iterated in arbitrary order), and the released C of
  odd but valid source (`g = g;`) did not build under the documented flags. Both are fixed in candidate `pfc2-v2`.
- The corpus study found a third, about time and not soundness: on a function with a long chain of proved
  obligations the check did not return, because the admission of dependencies was recomputed without being
  remembered. It is fixed in candidate `pfc2-v3`.
- PFC2 has **not** had the evaluation PFC had. Some of its experiments have run on candidate `pfc2-v3`
  (a differential campaign against an interpreter, false invariants, a second solver, removed preconditions,
  rewritings that keep the meaning; `records/runs/` holds the summary of each run, and one criterion was
  not met). Mutation testing of the engine ran and did **not** meet its criterion: the tests and the
  differential check noticed 0.806 of 3,768 changes to the engine against a required 0.90 (0.797 once 32 kills
  caused by a flaky harness test are taken out, a correction made after the campaign), and of the 732 changes that
  went unnoticed, read one by one by an AI assistant and not yet reviewed by the author, 84 change nothing and
  125 would make the engine certify something it should not. Tests that catch those 125 were added afterwards;
  the campaign was not run again. There is no external review. Say which experiments ran, never that PFC2 "was evaluated".
- One admission rule differs from PFC on purpose (unproved arithmetic no longer keeps bounds checks, because
  its overflow trap stays). It is argued in [Proofs](../03-proofs/#two-levels) and tested on ten constructed
  programs, with a sanitizer-backed comparison against fully checked C on seeded inputs and a check that the
  comparison notices a dropped trap. It is not mechanically proved, and ten programs are not a campaign.
- `--prove` was tried live on a handful of small programs: correct invariants were accepted and a false claim was
  refused in every attempt. That is a smoke test, not a study of any model.
- The VS Code extension compiles and the server is tested over the real protocol, but no test drives a running
  editor.

Treat PFC2 as a research prototype.

## Known gaps

| Gap | Effect | Workaround |
| --- | --- | --- |
| No `old(x)` | an `ensures` cannot relate a global to its value on entry | return the new value and state it about `result` |
| External contracts are checked for possibility, not truth | a declared function that does not behave as its contract says makes a certified caller wrong | keep external contracts to simple ranges |
| External functions are assumed not to call back into the file | a callback that writes a global would invalidate what the caller knows | do not pass control back from host code |
| An external `ensures` where one written cell selects another (`a[a[0]]`) | refused as undecided | state the property about one cell |
| A call that writes a global, in an expression that also reads it | C leaves the order unspecified; PFC2 evaluates the call first, so a plain C build may differ | read the global into a variable first |
| No recursion | recursive functions are refused | write a loop |
| No global arrays; local arrays need a literal length and an initial value | a buffer whose size depends on the input must be a parameter | take the array from the caller |
| A local array longer than 64 elements | only its listed initial values are known to the prover, not the zeros after them | write the elements you rely on |
| Variables are `long` or `_Bool` | `int` and `char` exist only as array elements; no unsigned types | read an element into a `long` |
| Characters are 7-bit | no character above 127, no octal or hexadecimal escapes | use the number |
| A string is a value only as the initial value of a `char` array | a literal cannot be passed where a `char` array is expected | declare the array first |
| No `switch`, `do`, `goto`, `?:`, bitwise operators | refused with a rule name | restructure with `if` |
| `long a[n]` with `n == 0` | the proof and the certified C are fine; the source compiled as plain C declares an array bound of zero, which C does not define | call it with `n >= 1` from plain C |
| `decreases(n - i)` at `full` | the subtraction of the measure needs an overflow proof although it is not in the emitted C | bound `n` and `i`, or use `memory` |
| Trigraphs (`??/` and the like) | refused: a C11 compiler would replace them | — |
| A computed index in the update of a `for` (`a[i + 1]++`) | refused (`subset-for-update`) | write it as the last statement of the body |
| `decreases` on a loop that contains `continue` | refused (`decreases-continue`) | restructure with `if`/`else` |
| Two prefix operators in a row (`- -x`) | the two operations share a position, so the check stays and the file is refused at `full` | write `x` |
| Calls under `&&`/`\|\|` and in loop conditions | refused (`subset-call-order`) | assign the call to a variable |
| One file per program | no modules; only PFC2's headers can be included | declare what you call as external functions |
| No macros with parameters, no `#if` | refused (`preprocess-unsupported`) | write a function; use `#define NAME value` for constants |
| Strings need `long` and pointers of equal size | LP64 targets only for programs with text | — |
| Decimal literals assume a 32-bit `int` and a 64-bit `long` | other targets are refused (`target-literal`) | — |
| `read_line` never frees | memory grows with the number of lines read | acceptable for short runs |
| Entry checks cover scalar conditions only | a `requires` about array contents or globals is not tested for unverified callers | call such functions only from checked code |
| Positions after a clause or macro on the same line | a reported column may be off; the line is right, and what is proved does not depend on layout | put `{` at the end of the line |
| The read of `a[i] += e` | reported one column after the write, to tell the two apart | — |
| A function whose invariants are long sums (26 array elements, say) | checking it, and above all a variant of it that is wrong, can take more than ten minutes; the cause is not established | shorter invariants; split the function |
| An array element passed directly as a call argument (`f(a[i])`) | the callee's `requires` about the element's range is not proved | read the element into a local first |
| A length parameter named after its array (`long a_len, long a[a_len]`) | it is read as the older `a[], a_len` spelling: `0 <= a_len` is **not** assumed, although `long a[n]` with any other name states `0 <= n` (found while porting the Verina tasks, 2026-11-19) | write `requires(a_len >= 0)`, or name the length differently |
| An `ensures` that names a parameter the body assigns | it reads the parameter's final value, not the value passed | copy the parameter into a local and leave the parameter alone |
| Inference covers counters only | relations between variables must be written | `invariant(...)`, `--proof`, `--prove` |
| The proof file names a file by its base name | two `x.c` in different directories look alike | use distinct names |

## Not a claim

PFC2 makes no performance claim: nothing here was measured.
