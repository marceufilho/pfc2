# Pre-registered design of the PFC2 evaluation

Registered on 2026-11-18, before any experiment below was run on the engine. Object of the evaluation: the
frozen candidate `pfc2-v1`, identified by the SHA-256 of `validation/freeze/protected.sha256`
(`b65f0bc9810bc10ac0301e107f2d38337f3ba37b2f9f273664ccc1e3a58ea719`).

This document fixes the questions, the units, the procedures, the criteria and the analysis. A change after
this date is an entry in [AMENDMENTS.md](AMENDMENTS.md), dated, with its reason and with a statement of
whether any outcome it concerns had already been seen. Results that this document does not cover are
exploratory and are labelled so wherever they appear.

## 0. What this registration is worth

- It was written by the same author, with the same AI assistant, that wrote the tool. No third party holds a
  copy with an independent timestamp unless the author publishes the bundle of
  `docs/evaluation/preregistration/` (a commit and a tag on a public remote are the intended means). Until then
  its date rests on the author's word and on file hashes.
- The thresholds below were chosen before outcomes, not derived from a power analysis. Where a threshold is
  inherited from the evaluation of the thesis compiler this is said.

### What had already been seen when this was written

These are development data. None of them may be reported as a confirmatory result.

| Seen | What it showed |
| --- | --- |
| The 32 example programs and the tests of `tests/` | written together with the tool; all pass |
| The 48 programs recorded from the thesis compiler | 44 identical, 4 intended differences |
| Review of the engine (decision 0063) | six defects, fixed before the freeze |
| Review of the language growth (decision 0065) | about 230 ad hoc generated programs, no difference between certified and plain C; one assumption and six defects, handled before the freeze |
| Harness self-check, generator seeds 0–299 | interpreter and plain C agree on 13,547 cases; no engine decision involved |
| A live smoke test of `--prove` on five programs | four certified at the first reply, a false claim refused |
| Lists of candidate corpora (`CORPORA.md`) | names, licences and estimated portability; no program was opened or ported |

Generator seeds 0–999 are development seeds. Confirmatory experiments use seeds from 100000 upward.

## 1. Questions

- **RQ1 (soundness).** Does `pfc2-v1` certify only programs whose released C behaves as the source's C
  semantics say, and does it remove a runtime check only where the removal cannot be observed?
- **RQ2 (independent agreement and capability).** Do a second solver and an independent verifier agree with
  its verdicts, and how much does it prove within its solver budget?
- **RQ3 (where loop invariants come from).** On programs it has not seen, how do the built-in inference, two
  classical baselines and a language model compare as sources of the invariants that certification needs?
- **RQ4 (tests versus proofs).** On small modules that ship their own tests: how many can be ported and
  certified, how many of the upstream test assertions follow from the proved contracts alone, and how do tests
  and proofs compare at detecting injected faults?
- **RQ5 (cost, descriptive).** What do kept and removed checks cost at run time?

RQ1 and RQ2 concern the engine and are answered by experiments E1–E9 and E12. RQ3 is E10. RQ4 is the corpus
study S1–S5. RQ5 is E11.

## 2. Corpora

| Name | What | Role |
| --- | --- | --- |
| `generated` | programs of `pfc2-eval-generator-v1`, seeds 100000–100999 (1,000 programs) | confirmatory for E1, E5, E6, E8, E9 |
| `examples` | `examples/` without `wrong/` | development; reported apart |
| `thesis-derived` | the six kernels and the ported strata of the thesis repository, re-spelled for `pfc.h` by a mechanical rule | regression only: the engine's ancestor was developed on them |
| `heldout-loops` | every task of SV-COMP `c/array-fpi` and `c/loop-invgen` at commit `d36a1c91fd9d21b0b6c89809dee4808828beb74b` whose expected verdict for `unreach-call` is true, ported by rule (below) | confirmatory for E10; sealed before E10 runs |
| `modules` | units selected by rule from the sources of section 6 | confirmatory for S1–S5; sealed in two steps (section 6) |

`heldout-loops` porting rules, applied mechanically and in this order: (H1) integer types become `long`;
(H2) array sizes and loop bounds given by nondeterministic values or macros become parameters with `requires`
stating the upstream assumptions; (H3) fixed-size and global arrays become array parameters with a length
parameter; (H4) nondeterministic scalar values become parameters; (H5) the final assertion becomes `assert` if
it is quantifier-free over scalars, and is dropped otherwise, the task then being about bounds and arithmetic
only (recorded per task); (H6) loops keep their shape; `for` stays `for`; (H7) no invariant is written.
A task is excluded only if a rule cannot be applied (pointer arithmetic, structs, floating point, recursion,
`goto`) or the front end refuses the port; each exclusion is recorded with its rule. A port is never reshaped
to pass. The set is external and public: it is **not blinded**, and the model of E10 may have seen the
upstream files.

## 3. Engine experiments

For all of them: solver budget 10 s per obligation (the package default), clang 19, the flags of
`pfc2.core.config.C_FLAGS`, sanitizers on every binary unless stated, level `memory` unless stated (so that
programs with unprovable arithmetic are certified with kept traps and remain in the experiment), every outcome
recorded in a sealed evidence directory, the candidate's identity in its configuration. A run on a tree that is
not the frozen candidate is not a confirmatory run.

**Failure is never agreement.** A build failure, a timeout of a binary, a missing or malformed output line, a
sanitizer report or a signal other than the trap is a failure of the case and is counted against the criterion.

| # | Experiment | Unit | Procedure | Criterion |
| --- | --- | --- | --- | --- |
| E1 | Differential | case = (certified program, input) | For each program of `generated` that is certified at `memory`: 100 inputs. On inputs the interpreter accepts, compare the interpreter with the certified C, the checked C and the source as plain C: result, final arrays, final globals. Also at `full` for programs certified there. | 0 differing cases; at least 300 programs certified, or the experiment is reported as underpowered |
| E8 | Expected traps | case as E1, on inputs the interpreter rejects | Overflow, out-of-bounds, division and conversion rejections: the checked C must trap. The certified C must trap for overflow at a kept trap site and for a violated scalar `requires` conjunct that the emitter rendered; plain C is not run. Cases in which the first violated conjunct was not rendered are counted and listed, not hidden. | 100% of the cases that must trap do; 0 traps on accepted inputs (that is E1) |
| E2 | Break-it | (program, clause) | In `examples`, `thesis-derived` and the first 200 certified programs of `generated`: remove each top-level conjunct of each `requires`, alone. A small-domain witness search with the interpreter decides whether some input now makes a guarded operation fail. | sensitivity: every removal with a witness loses the certificate (100%); specificity: every removal without a witness in the domain keeps verdict and code — reported, with the finite domain stated; threshold 100%, inherited |
| E3 | False invariants | (loop, candidate) | For each loop of the certified programs of `examples`, `thesis-derived` and the first 200 of `generated`: up to 20 candidates from fixed operators (literal false, off by one, reversed comparison, dropped conjunct, wrong variable), each admitted through `adapter.admit`. A candidate is false if the interpreter reaches a loop head that violates it. | 0 false candidates certified |
| E4 | Mutation of the engine | mutant | Every mutant of `pfc2/core/{vc,wp,smt,authorization,emit,desugar,lower}.py`, `gate.py`, `infer.py`, `elaborate.py`, `clauses.py`, `preprocess.py` under the operators relational, arithmetic, boolean, constant, statement deletion, return replacement; killed by the test suite, then by E1 on 50 programs. | score at least 0.90 excluding mutants classified equivalent; survivors classified one by one; the classifier and the review status are stated |
| E5 | Metamorphic robustness | (program, variant) | For the certified programs of `generated` (first 300): consistent renaming, reordering of independent adjacent locals, operand swap of one commutative operator, and re-layout (clauses and `{` joined on one line; one statement per line). | identical verdict, per-site decisions and, for renaming and layout, identical code up to names and positions: 100% |
| E6 | Second solver | query | Every obligation and entry query of `generated` (first 300 certified or not) and `examples`, exported to SMT-LIB and given to cvc5 1.4.2 with the same budget. | 0 disagreements (one says unsat, the other sat); inconclusive answers counted apart |
| E7 | Independent verifier | property | The units of `examples` and `thesis-derived` that can be stated in ACSL, by hand, run with Frama-C/WP in the image pinned by the thesis repository. | 0 unclassified disagreements; goals WP leaves open are inconclusive, not counterexamples |
| E9 | Replay | proof file | Build every certified program of `generated` and `examples`; replay each proof file in a fresh process. | 0 differences |
| E12 | Surfaces | program | The language server analysis and the browser entry point against the command-line path, on `examples` and 100 programs of `generated`. | identical verdict and blockers: 100% |

Order: E1 and E8 first. If either fails, the defect is recorded, the candidate is superseded (section 7), and
the experiments already run are rerun on the new candidate; their earlier results are reported as obtained on
the superseded one.

### E10 — sources of invariants

Conditions, each judged by `adapter.admit` or `adapter.check` at level `memory`, success meaning a certificate:

| Condition | Source |
| --- | --- |
| N | nothing: inference off, no invariant |
| I | the built-in inference of counter bounds |
| B1 | Houdini over a fixed template family (bounds of each scalar against each constant and each other scalar in scope), inference off |
| B2 | Daikon-style: the same filtering over invariants observed at loop heads by the interpreter on 200 inputs, inference off |
| L1 | a language model with the checker's refusal fed back, at most 5 attempts, inference off |
| L2 | the same model, 5 independent single attempts, no feedback, inference off |

Model: `gpt-6-astra`, reasoning effort low, 2,048 output tokens, no SDK retries, one instruction text fixed
before the set is unsealed. R = 5 independent runs of L1 and L2. The set `heldout-loops` is sealed before any
condition runs on it and is used once.

Primary outcome: the proportion of programs certified. Pre-registered contrasts, paired by program, with a
cluster bootstrap over programs (10,000 resamples, seed 0) for the 95% interval and Holm's correction over the
family of three:

1. I − N: does the built-in inference matter? Supported if the interval excludes 0.
2. L1 − I: does the model add to the built-in inference? Supported if the difference is at least 0.20 and the
   interval excludes 0.
3. L1 − B2: does the model beat the strongest classical baseline? Same threshold.

Also reported, exploratory: L1 − L2, attempts used, programs solved by exactly one condition, and the round
budget of B1 and B2 as a sensitivity analysis (5, the registered value, and 50). If more than 90% of the set is
certified under I, the set has no power for contrasts 2 and 3; this is then the reported result.

### E11 — run time (descriptive)

Certified, checked and plain builds of the array programs of `examples` and `thesis-derived` with drivers of
2^24 elements where the contract allows, three warm-ups, three interleaved blocks of ten runs, medians and
ratios with a seeded bootstrap. Labelled controlled only on a machine with the `performance` governor and an
instruction counter; otherwise exploratory. No performance claim is made either way.

## 4. Statistics

- Proportions: Wilson interval and Clopper–Pearson interval, both reported.
- Zero failures in n: the exact one-sided 95% bound, computed on the independent unit (the program), and also
  on cases with the statement that cases within a program are not independent.
- Paired contrasts: cluster bootstrap over programs; exact sign test as a check; Holm within each registered
  family.
- No result is described as significant without its interval, and no contrast outside section 3 and section 6
  is described as confirmatory.

## 5. What counts as a finding against PFC2

Any of: a differing case in E1; a missing trap in E8; a false invariant certified in E3; a removal with a
witness that keeps its certificate in E2; a solver disagreement in E6 or an unclassified one in E7; a proof file
that does not replay. Each is reported with its program, in the paper's main text, whether or not a later
candidate fixes it.

## 6. Corpus study (RQ4)

### Sources, pinned before opening

| Source | Commit | Unit | Role of its tests |
| --- | --- | --- | --- |
| Exercism C track, `exercises/practice/*` | `1675b02c310198e9752e516ee1a2294b76a37f84` | one exercise: the reference solution `.meta/example.c` with its header | `test_<slug>.c`, one assertion per check |
| Exercism problem specifications | `4812c213a2647e2034ad5ac78155ce9265cdd171` | `canonical-data.json` of the same exercise | the language-neutral list of cases |
| Verina | `66b3ce5014edafb20cb26b87c681e7f31847249f` | one task, re-expressed in C by hand from its description | its positive and negative tests; its specification is written by others |

Juliet and library kernels, named in the plan, are **not** part of the registered study. They may be reported
as exploratory additions.

### Selection

Every Exercism practice exercise, in lexicographic order of slug, is a candidate. A unit enters the corpus if
its reference solution can be ported by the rules P1–P8 below. Exclusion is by rule only, recorded per unit:
(X1) needs floating point; (X2) needs dynamic allocation whose size is not bounded by an input length;
(X3) needs structures that cannot be flattened to scalars and parallel arrays by P5; (X4) needs function
pointers, recursion or `goto`; (X5) needs bitwise operators; (X6) the front end refuses the port for a reason
not listed, with the diagnostic recorded. The target of 150–200 units in the plan is not a criterion: the number
of units that port is a result. For Verina, every task in the order of its identifier, same rules.

Porting rules: (P1) integer types become `long`, except array elements that hold characters (`char`) or `int`
values in the upstream interface; (P2) a `const char *` string becomes a `const char` array with its length as a
parameter, the terminator not counted; (P3) an out-parameter becomes an array parameter of length 1 or the
return value; (P4) `size_t` lengths become `long` parameters with the array type `a[n]`; (P5) a struct of
scalars becomes that many parameters or parallel arrays; an enum becomes named `long` constants; (P6) `switch`
becomes `if` chains; `do` loops become `while` with the body duplicated once; `?:` becomes `if`; (P7) calls to
`strlen`, `isdigit`, `isalpha`, `toupper`, `tolower`, `abs` and `memset`/`memcpy` over arrays become small
functions written once in a shared prelude and certified with the unit; (P8) nothing else changes: the
algorithm, its order of operations and its loop structure are kept.

### Protocol

1. **Port** each selected unit (AI-drafted, by P1–P8), with a driver that runs the upstream tests against the
   port compiled as plain C. A port that fails an upstream test is fixed until it passes or the unit is excluded
   under X6 with the reason; the number of such fixes is reported.
2. **Seal** the ports and their tests (`heldout seal`).
3. **Specify**: write `requires`/`ensures`/invariants/laws for each unit (AI-drafted) from the exercise's
   prose description and the function's signature. The contract states what the function returns for every
   input; it does not enumerate the test cases. Then **freeze** the contracts (second seal) before step 5.
4. **Review**: the author reviews a random 20% of the units (seeded, seed 20261118, drawn after sealing) for
   whether the contract says what the prose says. Every disagreement is recorded; reviewed and unreviewed units
   are reported separately.
5. **Measure** (below). No contract is edited after the second seal; a unit whose contract turns out wrong is
   reported as a specification defect.

### Measures and criteria

| # | Measure | Definition | Reported as |
| --- | --- | --- | --- |
| S1 | Portability | units ported / candidate units; exclusions by rule | proportion with interval; table of reasons |
| S2 | Certification | units certified at `full`, at `memory`, refused; annotation lines per code line | proportions with intervals |
| S3 | Test subsumption | for each upstream test assertion of a certified unit: restated as a law with those fixed inputs and proved **from the contract alone** (the unit's body replaced by a declared function with the same contract) | proportion of assertions subsumed, per unit and overall, clustered by unit |
| S4 | Fault detection | mutants of each certified unit's body (relational, arithmetic, constant, statement deletion; all mutants, not a sample); for each: do the upstream tests fail (run on the mutant as plain C under sanitizers), and is the mutant refused by PFC2 with a counterexample | the 2×2 table per unit; tests-only, proof-only, both, neither; mutants that survive both are examined for equivalence |
| S5 | Defects | a behaviour of the *upstream* solution that contradicts its prose or is undefined C on an input its tests allow, reproduced on the upstream code with a concrete input | a list; port defects and specification defects listed separately and never counted as upstream defects |

Registered hypotheses:

- **H4a.** At least half of the upstream test assertions of certified units are subsumed. The point estimate
  and its 95% interval (cluster bootstrap over units) are reported; the claim "at least half" is made only if
  the lower end of the interval is at least 0.50.
- **H4b.** Among non-equivalent mutants, the proportion refused by the proof is at least the proportion killed
  by the upstream tests (paired by mutant; the difference and its cluster-bootstrap interval over units are
  reported; supported if the interval's lower end is at least 0).
- No hypothesis is registered about S5: finding no defect in well-tested code is the expected outcome and is
  reported as such.

A mutant "refused by the proof" counts only when the refusal carries a counterexample or a failed obligation;
a timeout, an unknown or a front-end refusal is counted as *not detected by the proof* and reported apart.

### Threats fixed in advance

- The contracts are drafted by an AI assistant that can read the tests. Steps 3 and 4 limit this and do not
  remove it: S3 is an upper bound on what an independent specifier would achieve.
- A port is not the upstream code. S5 requires reproduction upstream; S3 and S4 are statements about the ports.
- Exercism solutions are small and didactic. Nothing here supports a claim about large programs.
- The Verina stratum has specifications written by others in another language; restating them in C is itself a
  translation, reported per task.

## 7. When the candidate changes

A defect found during the evaluation is recorded (decision record, program, test), fixed, and frozen as
`pfc2-v2`. The amendment log states which experiments had run on which candidate. Experiments whose procedure
the defect could affect are rerun in full on the new candidate; none is patched or resumed. Results from two
candidates are never pooled.

## 8. Stopping

Each experiment runs once to completion on its registered units. An experiment interrupted by a machine
failure is rerun from the start into a new directory; the partial directory is kept and not counted. No
experiment is extended because its result is close to a threshold.
