# 3. Proofs

## What is proved

The checker turns a program into *obligations*: formulas that must hold on every path, for every input the
contracts allow. Each one is sent to the Z3 solver. An obligation counts only when Z3 answers that its negation is
unsatisfiable; a failure, a timeout, `unknown` or a solver error never counts.

| Obligation | Where it comes from | Meaning |
| --- | --- | --- |
| `bounds` | every `a[i]`, read or written | `0 <= i` and `i <` the length of `a` |
| `division` | every `/` and `%` | the divisor is not zero, and the quotient exists (`LONG_MIN / -1` does not) |
| `overflow` | every `+`, `-`, `*`, unary `-` | the result fits its C type |
| `conversion` | every store of a wider value into a `char` or `int` element | the value fits the element; required at both levels |
| `call-precondition` | every call | the callee's `requires`, and the length of each array passed |
| `postcondition` | every `return` | the function's `ensures` |
| `entry`, `preservation` | every loop | the invariant holds before the loop and after one arbitrary iteration |
| `assert` | `assert`, `where`, `decreases`, laws | the stated fact holds there |

Two more questions are asked about every function that is declared and not defined, because its contract is
taken on trust: can the contract be met at all, and does every input it allows have a result? An impossible
contract refuses the file ([Programs](04-programs.md#functions-implemented-elsewhere)).

Arithmetic inside contracts is mathematical: `requires(a + b < n)` speaks about the true sum, with no overflow.

Besides the obligations, each function gets one *entry consistency* query: is there any input at all that
satisfies its `requires`? If not, the file is refused, because everything about that function would be proved
vacuously.

## Two levels

| Level | Certified when | What the emitted C still checks |
| --- | --- | --- |
| `full` (default) | every obligation is proved | scalar `requires` at entry, nothing else |
| `memory` | every obligation except `overflow` is proved | the same, plus a trap at each unproved `+ - *` |

At `memory`, the report lists every trap that stays:

```console
$ pfc2 check examples/03_sum/sum.c --level memory
sum.c: certified (memory)
  overflow checks removed: 1 of 2; 1 overflow trap kept
      kept at sum.c:10:9
```

Why a bounds check may be removed while an addition nearby is unproved: the proofs reason about mathematical
integers. In the emitted C, every arithmetic operation either was proved not to overflow or traps when it does.
So an execution either stops at a trap or has computed exactly the values the proofs talk about, and a bounds
check proved for those values is redundant on every execution that reaches it. `tests/test_traps.py`
runs a program built to exercise this: an overflowing input stops at the multiplication, before the index that
the wrapped value would have sent far outside the array.

A consequence to keep in mind at `memory`: laws and postconditions describe the executions that do not stop at a
kept trap.

## What stays in the emitted C

- **Entry checks.** Each top-level conjunct of a `requires` that mentions only scalar parameters and literals
  is tested when the function is entered, and traps if false. The proofs cover callers that PFC2 checked; this
  covers callers it did not. Conjuncts about array contents, globals or results of calls are not tested; the
  report lists them as "assumed, not checked at entry".
- **Kept overflow traps**, at `memory` only.
- **Citations.** Each removed check leaves `// proved: obligation <id>` where it stood.

Nothing else: `assert`, `ensures`, `invariant`, `decreases` and laws leave no code.

## Inferred loop bounds

A loop needs an invariant. For the common counting loop PFC2 proposes one:

| Loop | Candidates |
| --- | --- |
| `i` starts at `init`, grows by a positive constant, condition `i < e` / `i <= e` / `i != e` | `init <= i`; and `i <= e` when the step is 1 and the condition is `<` or `!=` |
| `i` starts at `init`, shrinks by a positive constant, condition `i > e` / `i >= e` / `i != e` | `i <= init`; and `e <= i` when the step is 1 and the condition is `>` or `!=` |

`e` and `init` must be values the loop does not change. The candidates are joined with any invariant you wrote
and checked like it. If the loop's invariant obligations fail, candidates are dropped (all, then each alone, then
none) until they hold; what survived is reported as `(inferred)` and recorded in the proof file. A candidate is a
guess that costs a solver call; it cannot make an unproved program pass.

Anything else, such as how an accumulator relates to the counter, has to be written.

## Termination

Without `decreases`, PFC2 proves what a loop computes *if* it ends. With it:

```c
while (left > 0) decreases(left) {
    left--;
}
```

two facts are proved: when the body starts the measure is not negative, and when the body ends (after the update
of a `for`) it is strictly smaller. A non-negative integer cannot decrease forever, provided each
iteration ends: so a loop is counted only if every loop nested in it has a proved measure too and every function
it calls ends on all its paths. Declared functions are assumed to return. The report counts the loops
that have a proved measure: `loops proved to terminate: 1 of 1`. Termination is never required for certification.

## Proof files

`build` writes `NAME.c` and, separately, `NAME.proof.json` (`pfc-proof-v3`): the preprocessed program, the
target layout, the solver version and budget, every law, every obligation with its status and query identity,
every decision about a check, the entry checks, the inferred invariants, the proved measures, the unverified
boundary, and the emitted C with its hash. It has no timestamp and no machine path, so two builds of the same
source on the same solver give the same file.

```console
$ pfc2 replay build/pfc2/fill/fill.proof.json
build/pfc2/fill/fill.proof.json: reproduced (certified, level full, 0 network requests)
```

`replay` recomputes everything from the embedded program and lists any field that differs. A proof file is
evidence to recompute, not an authority: editing a status in it changes nothing except making `replay` fail.

## Supplying or requesting invariants

- `--proof FILE` reads `{"invariants": ["...", ...]}`, one per loop in source order, or the proof file of an
  earlier build. The text is validated as a call-free expression and then proved like a written invariant. It
  cannot replace an invariant that is already written.
- `--prove` asks a language model for that JSON, at most five times, feeding back what the checker refused. It
  sends the source file to the service and reads `OPENAI_API_KEY` from the environment only. Whatever comes back
  is untrusted text that goes through the same checker; a wrong answer is refused like any wrong invariant.
  The tests use scripted replies. `PFC2_MODEL` selects the model.
