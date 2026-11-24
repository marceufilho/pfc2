# Amendments to the pre-registered design

Every change to [DESIGN.md](DESIGN.md) after 2026-11-18 is an entry here: date, what changes, why, and whether an
outcome it concerns had already been seen. An entry never rewrites an earlier one. Candidates are listed with
the experiments run on each.

## Candidates

| Candidate | Protected inventory SHA-256 | Frozen | Experiments run on it |
| --- | --- | --- | --- |
| `pfc2-v1` | `b65f0bc9810bc10ac0301e107f2d38337f3ba37b2f9f273664ccc1e3a58ea719` | 2026-11-18 | harness self-check (no engine decision); superseded by amendment 2 |
| `pfc2-v2` | `1151be09d4b4e104d60f0c6c7b521106163acfb838afab1809c071825f2b832a` | 2026-11-18 | E1, E8, E9, E3, E6, E12 (`bench/eval/*-20261118`); corpus pilot and Exercism stratum (`corpus-pilot-20261118`, `corpus-exercism-20261118`, `corpus-exercism-laws-defined-20261119`); superseded by amendment 11 |
| `pfc2-v3` | `115f5ad6dbdb0c48c71bbf72678c84b2eb89fba0220c026039f7db6cc835b6ee` | 2026-11-19 | the reruns of amendment 11 (`bench/eval/*-v3-20261119`) and everything later |

## Entries

### 1 — 2026-11-18: a time budget per program in E1/E8/E9

**Change.** In the differential campaign, the two verdicts of one program (`memory` and `full`, with inference)
get 600 s of wall-clock time in total. A program that exceeds it is recorded as "not judged within the time
budget", counts as not certified, and its number is reported. The per-obligation solver budget stays 10 s.

**Why.** A shake-down run on development seeds 300–359 did not finish: development seed 339 has 176 obligations
and one solver pass over them takes about two minutes, with no single obligation timing out. The registered
design bounded each obligation but not a program.

**Outcomes already seen.** None on confirmatory seeds. From the shake-down, only that it was slow; its partial
directory was deleted without being read for verdicts or case outcomes.

**Effect on the criteria.** None on what counts as a failure. The certified set shrinks by the programs not
judged; the threshold of 300 certified programs for E1 to be called powered is unchanged.

### 2 — 2026-11-18: candidate pfc2-v2 replaces pfc2-v1 before any confirmatory run

**Change.** The object of the evaluation is `pfc2-v2`: `pfc2-v1` with two fixes (decision 0067): a set iterated
in arbitrary order that made identities differ between processes, and two warning flags without which the
released C of odd but valid source did not build.

**Why.** Both were found by the shake-down of the differential campaign on development seeds 300–359.

**Outcomes already seen.** None on confirmatory seeds and none of the registered experiments had run on
`pfc2-v1`. On development seeds, from the shake-down with a 90 s budget: 51 of 60 programs certified at
`memory`, 1,875 cases agreeing, 125 required traps observed, no differing case, no missing trap; 200 cases
failed because 4 programs did not build; 3 proof files did not replay. These numbers are development data.

**Effect on the criteria.** None. Section 7 of the design is applied: nothing is pooled across candidates.

### 3 — 2026-11-18: a pilot on the first twelve corpus candidates; rules to be revised before the study

**Change.** The first twelve Exercism candidates in the order of their directory names (`acronym`, `allergies`,
`all-your-base`, `anagram`, `armstrong-numbers`, `atbash-cipher`, `beer-song`, `binary`, `binary-search`,
`binary-search-tree`, `bob`, `circular-buffer`) are a pilot. They are used to try the protocol and its tooling,
are reported as a pilot, and are excluded from the confirmatory corpus. In the pilot four porting rules were
added that the registered list lacks: (P9) `pow` on integer arguments becomes an integer loop; (P10) `<< 1` and
`| 1` on a non-negative accumulator become `* 2` and `+ 1`; (P11) a pointer walked over an array becomes an
index; (P12) a function that returns one of a fixed set of string literals returns its number, and the host
glue maps it back.

**Why.** Reading the first candidates showed that the registered rules exclude most of them for reasons that
have nothing to do with what PFC2 can prove, and that the contract language cannot state what most of these
functions compute (it has no quantifier and no specification function). Both needed measuring on real units
before 150 of them are ported.

**Outcomes already seen.** Only the reading of the twelve solutions. No unit outside the pilot was opened.

**Open, for the author to decide before the confirmatory study.** Whether P9–P12 become registered rules;
whether hypothesis H4a (at least half of the upstream assertions follow from the contract) stays as registered
given the pilot's result on it; and whether the contract language is extended first. Until then the corpus
study has not started.

### 4 — 2026-11-18: narrower scope of E3 as implemented

**Change.** E3 (false invariants) runs on the certified programs of `generated` only. The registered design
also names `examples` and `thesis-derived`.

**Why.** The falsity of a candidate is decided by running the interpreter on inputs, and inputs exist for
generated programs only; the thesis-derived corpus has not been built.

**Outcomes already seen.** On development seeds 0–11 only (no false candidate admitted). None on confirmatory
seeds.

### 5 — 2026-11-18: the same time budget in E12

**Change.** In E12 the three verdicts of one program get 600 s of wall-clock time; a program that exceeds it is
a row `not-judged`, compares nothing and is reported by count.

**Why.** The first run of E12 compared 72 programs in three minutes and then spent five hours on confirmatory
seed 100072, one of the 15 programs the differential campaign had recorded as not judged within 600 s. E12 had
been written without the budget of amendment 1.

**Outcomes already seen.** The 72 rows of the interrupted run: all three paths agreed on each. Its directory is
kept as `bench/eval/surfaces-20261118-partial`; it is not sealed and is not evidence.


### 6 — 2026-11-18: the corpus study after the pilot (author's decisions)

Written before any unit outside the pilot was opened. The author decided the three questions amendment 3 left
open, and a fourth about an engine defect. `DESIGN.md` is not rewritten; where this entry and section 6 of the
design differ, this entry holds.

**Change 1: porting rules.** Rules P9 to P12 of amendment 3 are registered, with one more:
(P13) an array element used as a call argument is first read into a local variable. Each port records the rules
it used. Portability (S1) is reported twice: for units that port under P1–P8 alone, and for all ported units.

**Change 2: the question.** The registered hypotheses H4a and H4b are kept exactly as written, are computed with
their registered intervals and are reported whatever they give. The pilot predicts both fail, and this entry
says so before the study runs. The primary reading of RQ4 becomes descriptive, "what does each catch": the 2×2
table of mutants (tests kill / proof refuses) by unit and by mutation operator, test subsumption by unit, and
upstream defects. No new hypothesis or threshold is registered for the descriptive reading.

**Change 3: the engine.** The completeness defect found in the pilot (an array element passed directly as a
call argument loses the range of its type) is not fixed. The candidate stays `pfc2-v2`; P13 works around it.

**Change 4: procedure.**
- The pilot's twelve units are excluded from every confirmatory count. Candidates are the other 73 Exercism
  practice exercises in lexicographic order of slug.
- The design's two seals are two directories, because a sealed directory cannot be sealed again:
  `corpus/exercism-ports` holds the ports as they passed the upstream tests; `corpus/exercism` holds the same
  ports with contracts and the transcribed test cases. The harness checks that each pair has the same code once
  the clauses are erased.
- A port may carry the `requires` clauses without which the front end refuses it; nothing else is written before
  the first seal.
- S3: each upstream assertion is transcribed by hand into a fixed-input law (`tests.json` of the unit), sealed
  with the contracts. An assertion that cannot be restated that way (for example, it compares text the port
  leaves to the host glue) is counted as not subsumed and reported apart as "not expressible".
- S4: mutants that survive both the tests and the proof are examined for equivalence by the AI assistant; the
  classification is labelled as such until the author reviews it.
- The author's review of a 20% sample (seed 20261118) happens after the measurements. The sample is drawn right
  after the second seal; reviewed and unreviewed units are reported separately once the review exists.
- The time budget of amendment 1 does not apply; each verdict of a unit or mutant keeps the registered 10 s per
  obligation.

**Why.** Amendment 3 and `reports/PHASE-4.md`: under P1–P8 one pilot unit of twelve ports, and the contract
language cannot state what most of these functions compute.

**Outcomes already seen.** The pilot (twelve units, sealed in `bench/eval/corpus-pilot-20261118`) and a script's
count of lines, tests and constructs for candidates 13 to 85. No reference solution outside the pilot had been
read. The Verina stratum had not been opened.

**What this entry is worth.** The repository has no commit and no tag, so this entry has no external date. It
was written after the pilot's outcomes and because of them; the descriptive reading is therefore not a
prediction made blind, and the text of the paper must say so.

### 7 — 2026-11-18: how the porting rules are read, and one more rule

Written after the 73 reference solutions were read for classification and before any port was written, any
upstream test was run against a port, or any proof was attempted on a confirmatory unit.

**Change 1: P14.** Where the front end refuses a construct that has an exact local spelling it accepts, that
spelling is used: a `void` function returns `0`; a call, an update (`++`, `--`, an assignment) or a read through
a moving pointer that C evaluates inside a larger expression or a loop condition becomes a statement of its own
in the same order; a file-scope constant table becomes a local constant array of the function that reads it; a
macro with parameters is expanded where it is used. The pilot did the second of these without naming it
(`acronym`). Portability is reported in three tiers: P1–P8, with P9–P13, with P14.

**Change 2: the lists in the rules are closed.** P7 names `strlen`, `isdigit`, `isalpha`, `toupper`, `tolower`,
`abs`, `memset` and `memcpy`. A solution that calls any other library function in the code that remains after
P2 and P3 (`strcpy`, `strcat`, `strchr`, `strcmp`, `memcmp`, `isupper`, `isalnum`, `qsort`, `sscanf`,
`snprintf`, the `<time.h>` and `<math.h>` functions other than `pow` on integers) is excluded under X6 with the
function named, or under X1 when the function is a floating-point one. P10 covers `<< 1` and `| 1` only; every
other bitwise use is X5. An allocation whose size comes from an input *value* (not from the length of an input)
is X2. An interface that hands out an array of pointers (`char **`, `int **`), a table of strings, or a struct
holding an array of text is X3. Allocation of a result bounded by an input length moves to the host glue with
its failure handling (P3), as in the pilot.

**Why.** The registered rules name no way to spell what PFC2's front end demands (P14), and they do not say
whether their lists are examples. Reading them as closed keeps the selection mechanical; it also excludes units
that a longer prelude would admit (`sublist`, `rotational-cipher`, `rail-fence-cipher`, `phone-number`,
`pig-latin`), which is reported as such and is a decision for a later amendment, not for this run.

**Outcomes already seen.** The text of the 73 solutions and their headers. Classification made from them: 21
candidates to port, 52 excluded by rule. No port existed and no tool had run on any of them.

### 8 — 2026-11-18: a time budget per verdict in the corpus study, and proofs in their own process

Corrects the last point of change 4 of amendment 6, before any measurement of the corpus study ran.

**Change.** Each verdict of the corpus study (a unit at one level, a mutant at its unit's level, one
subsumption law) runs in a process of its own and gets 600 s of wall-clock time, the budget of amendments 1 and
5. The per-obligation solver budget stays 10 s. A unit not judged within the budget at either level is reported
as "not judged within the time budget" and counts as not certified; a mutant or a law not judged counts as not
detected by the proof and not subsumed, and is reported apart. Mutants and laws of one unit are judged by
several workers at once (the number is recorded in the configuration).

**Why.** While the contracts were being written, `pfc2 check` on two units (`two-bucket`, `yacht`) did not
return in ten minutes with any solver budget, including 100 ms. A stack dump shows the time is spent in
`pfc2/core/smt.py`, in the function that decides whether the dependencies of an obligation are admitted: it
recomputes the same sub-results recursively without remembering them, which is exponential in the depth of the
dependency chain when every obligation is proved. This is a performance defect of `pfc2-v2`, not a soundness
one. It is recorded here and in `reports/PHASE-4.md` and is not fixed: the candidate is unchanged.

**Outcomes already seen.** The verdicts obtained while writing the contracts of the 21 units (which units
certify, at which level, and which do not), and the two timings above. No mutant had been generated and no
subsumption law had been checked.

### 9 — 2026-11-19: an exploratory second reading of S3, added after its outcome

**Change.** Besides the registered S3 (each law beside declarations whose bodies are removed), a second
measurement is reported and labelled exploratory: the same laws, each written beside the unit's definitions
(`python -m pfc2_eval corpus ... --laws-beside-definitions`, assertions only, its own sealed directory). The
registered S3 and hypothesis H4a are reported from the registered measurement only.

**Why.** In the sealed registered run, laws of several units were refused with no failed obligation. The reason
PFC2 gives is "the contract of F was not shown possible for every input (unknown)": for a function without a
body PFC2 must show that some result satisfies the contract for every input, and it leaves that undecided for
contracts with products of variables or remainders (`difference-of-squares`, `nth-prime`). The refusal says
nothing about whether the contract implies the test. Beside the definitions that check does not arise, and a
law is still proved through the contracts of the functions it calls, never through their bodies (a test of the
harness checks this with a body that returns more than its contract says).

**Outcomes already seen.** All of the registered run (`bench/eval/corpus-exercism-20261118`): 58 of 198
assertions subsumed. This entry is post hoc; the second reading can only be read as a description.

### 10 — 2026-11-19: a flaw of the exploratory reading, fixed in the harness after its run

**Change.** `pfc2_eval/corpus.py` now judges a law beside definitions at the level its unit certifies at; before,
it used `full` always. A test of the harness covers it. The sealed exploratory directory
(`bench/eval/corpus-exercism-laws-defined-20261119`) was produced before the fix and is not rerun or edited.

**Why.** In that run every law of the three units certified at `memory` was refused, because the file that
holds the unit is not certified at `full`: 9 laws that the registered reading proves were lost for that reason.

**Outcomes already seen.** Both readings. The report gives each and the number of laws proved under at least
one (67 of 198), and says the second reading is post hoc.

### 11 — 2026-11-19: candidate pfc2-v3 replaces pfc2-v2; what is rerun on it

**Change.** The defect of amendment 8 (decision 0068) is fixed and the tree is frozen as `pfc2-v3` (decision
0069): the admission of dependencies is decided once per obligation, in `pfc2/core/smt.py`,
`pfc2/core/authorization.py` and `pfc2/infer.py`. By section 7 of the design, the experiments already run are
rerun in full on `pfc2-v3`, each once, into a new directory, with the commands, seeds and settings of the
first run:

| Experiment | On `pfc2-v2` (stays sealed) | On `pfc2-v3` |
| --- | --- | --- |
| E1, E8, E9 | `bench/eval/differential-20261118` | `bench/eval/differential-v3-20261119` |
| E3 | `bench/eval/inject-20261118` | `bench/eval/inject-v3-20261119` |
| E6 | `bench/eval/crosscheck-20261118` | `bench/eval/crosscheck-v3-20261119` |
| E12 | `bench/eval/surfaces-20261118` | `bench/eval/surfaces-v3-20261119` |
| Corpus study, S2 to S4 | `bench/eval/corpus-exercism-20261118` | `bench/eval/corpus-exercism-v3-20261119` |

The sealed corpora (`corpus/exercism-ports`, `corpus/exercism`) are used as they are: no port, contract or
transcribed test changes, the selection (S1) and the upstream findings (S5) are not redone, and the 600 s budget
of amendment 8 stays. The reports give the results of the two candidates side by side and never add them. From
this entry on, the numbers of record for the engine experiments and for S2 to S4 are those of `pfc2-v3`; the
`pfc2-v2` numbers remain in the reports, labelled. The exploratory reading of amendment 9 is rerun as well, with
the harness fix of amendment 10, into `bench/eval/corpus-exercism-laws-defined-v3-20261119`; it stays
exploratory.

**Why.** The author asked for the fix on 2026-11-19 so that `two-bucket`, `yacht` and the 18 mutants of
`pangram` get a verdict. The fix is meant to change no answer, only the time to reach it; the reruns are the
check of that on the registered populations, besides the tests of decision 0069.

**Outcomes already seen.** Everything obtained on `pfc2-v2`. On the fixed tree, before this entry: the test
suite, and one check of each of the two units at each level. Both now return in minutes and both are refused,
at `memory` on one obligation each (for `two-bucket`, an `ensures` at line 144 of its port), so the number of certified units is expected to stay at 16 of 21 with "not judged" becoming
"refused". The contracts were sealed before these verdicts could be seen and are not changed to obtain a
certificate. The seeds of the generated programs are the registered ones; that the reruns are regression runs on
programs whose `pfc2-v2` outcomes are known is part of how they must be read. As before, the repository has no
commit or tag, so this entry has no external date.

### 12 — 2026-11-19: how E2 and E5 are carried out

Written after both were implemented and tried on development seeds, before either ran on a confirmatory seed.

**Change, E5 (rewritings).** The four rewritings are made on the program text (`pfc2_eval/robustness.py`):
every name the program introduces gets the suffix `_zq`; the first two adjacent local declarations that do not
read each other and have no call, assignment, `++` or `--` change places; the operands of the first
parenthesised `+`, `*`, `==` or `!=` outside a clause change places, when neither has such an effect; and
every clause line and every lone `{` is joined to the line before it. "Re-layout (clauses and `{` joined on one
line; one statement per line)" is read as this one rewriting: the header on one line, the body one statement per
line as the generator writes it. Compared: the verdict, the number of blockers, and every decision as (kind,
line, removed) under the line map of the rewriting; for renaming and layout also the certified C after the
suffix, the proof identifiers and the positions are taken out. A rewriting that does not apply to a program is
counted as not applicable. The interpreter runs each program and its variant on 20 inputs; a difference there is
a defect of the harness, listed apart, and fails the run. Population as registered: the first 300 programs from
seed 100000 certified at `memory`. Each program gets 600 s for its five judgements (as amendments 1 and 5).

**Change, E2 (break-it).** `pfc2_eval/breakit.py` removes each top-level conjunct of each written `requires`,
alone, without moving a line. The function that carries the clause is run directly in the interpreter, so a
helper's precondition is judged on the helper's inputs. The small domain: up to 5,000 seeded draws per removal,
stopping at 300 inputs that only the removed conjunct had kept out; scalars from −51, −50, −49, −9, −3 to 10,
49, 50, 51 and the two extremes of `long`; lengths −1 to 9; elements from −2 to 2 and 9; buffers hold exactly
what their length says. Three outcomes of the search, where the design has two:

| Search finds | What must follow | Scored as |
| --- | --- | --- |
| an input that reaches a failing bounds or division check, a conversion out of range, a call its callee refuses, or a false `assert`, `ensures` or invariant | the certificate is lost | sensitivity |
| only inputs that reach an arithmetic overflow | the certificate is lost, or the line that overflowed keeps a trap in the new C | apart, its own rate |
| no such input | certified, every decision the same, and the same C once the entry checks (which restate the `requires`) are taken out | specificity |

The second row exists because the experiments run at `memory`, where an overflow is trapped and not proved: the
registered "loses the certificate" cannot hold for it by the level's definition. A removal on which the
interpreter cannot follow some input (a declared function, the step budget) and finds no witness is counted as
undecided and not scored. Populations: the first 200 programs from seed 100000 certified at `memory`, which
carry the criterion, and the certified programs of `examples`, reported apart as development data.
`thesis-derived` does not exist and is not included. 600 s per program.

**Also.** `tests/eval/test_eval_harness.py`, a file of the baseline inventory, asserted that the `breakit`
command is not implemented; that line now names `oracle`. The baseline inventory of `pfc2-v3` was written again
for it and for the new test files, between two campaigns of amendment 11. The protected inventory, which is the
candidate's identity, is unchanged (`115f5ad6…35b6ee`).

**Why.** The design names the rewritings and the search but not how they are made. These are the choices made
while implementing them; they are recorded before the confirmatory runs so that they cannot follow the outcome.

**Outcomes already seen.** Development seeds only (300 to 323). E5 on 12 programs: no difference; reordering
applied to 5 of 11 certified programs. E2 on 24 programs: every removal with a witness lost its certificate (77
of 77); 2 of 190 removals without a witness changed something, both the upper bound of an array length, where
an overflow trap is no longer removed and the overflow needs a length outside the domain; overflow-only 11 of
11. A first version of the domain lacked the length 7 and missed a witness that needs `n == 7`; the domain above
is the corrected one, and the first overflow rule ("a removed trap comes back") was replaced by the one in the
table because it wrongly failed removals whose trap had never been removed. Specificity below 100% is therefore
expected on the confirmatory seeds and will be reported as it comes out. No confirmatory seed had been used for
either experiment.

### 13 — 2026-11-19: how E4 is carried out

Written after the runner (`pfc2_eval/mutate.py`) was implemented and rehearsed, before any mutant of the
registered population was judged.

**Change.** The six registered operators are made on the syntax tree of each registered file:

| Operator | What it does |
| --- | --- |
| relational | `<` ↔ `<=`, `>` ↔ `>=`, `==` ↔ `!=`, `in` ↔ `not in`, `is` ↔ `is not`, in a comparison with one operator |
| arithmetic | `+` ↔ `-`, `*` ↔ `//`, `%` → `//` |
| boolean | `and` ↔ `or`; the condition of an `if` or `while` negated |
| constant | an integer literal plus one and minus one (not `True`/`False`) |
| statement deletion | an assignment, an expression statement or a `raise`, in a body of two statements or more, replaced by `pass` (not a docstring, not a bare annotation) |
| return replacement | `return None`; for a comparison, a boolean operation or a boolean literal also its negation |

A mutant must parse, and two sites that give the same text count once. The population is 3,768 mutants (`vc`
106, `wp` 495, `smt` 508, `authorization` 114, `emit` 523, `desugar` 158, `lower` 569, `gate` 77, `infer` 259,
`elaborate` 333, `clauses` 425, `preprocess` 201). Each is written into a private copy of the tree and two
layers run until one fails:

1. the whole test suite as it stands today, including the tests added with `pfc2-v3` and with the harness since,
   quickest files first by the timings in `docs/evaluation/test-durations.txt`, stopping at the first failure;
2. E1 on the first 50 programs of seed 100000, 100 inputs each: the mutant is killed when that run fails (a
   differing case, a missing trap, a failed case, a crash, or nothing certified to compare).

Four tests are left out of layer 1 because they ask whether the tree's bytes are the frozen candidate's, which
every mutant fails without any behaviour being observed: the two inventory tests, the harness test that calls
`candidate`, and the comparison of the committed site bundle (it embeds the engine's files). A layer that
exceeds its time (40 minutes for the tests, 60 for E1) stops the mutant; such mutants count as killed and are
reported apart. The score is killed over all mutants not classified equivalent. Survivors are classified by the
AI assistant afterwards, one by one, labelled as such; the author's review is a separate step. One run, ten
workers, not resumed.

**Why.** The design names the operators and the two layers and nothing else.

**Outcomes already seen.** None of the population. On the unmutated tree in a private copy the suite passes in
about 7 minutes and E1 on 50 programs in about 6, so a survivor costs about 13 minutes and the whole run about a
day on this machine. A rehearsal with two hand-made changes that are not in the population: a function renamed
away is stopped by the first test file in under a second; a comment added to `gate.py` was first "killed" by the
harness test that calls `candidate`, which is how the fourth excluded test was found, and after its exclusion
it survived both layers, in 16 minutes with other campaigns running beside it.

### 14 — 2026-11-19: the first run of E2 did not seal and is run again

**Change.** `bench/eval/breakit-20261119` stopped with an error of the harness after the 200 generated programs,
at the first example: an example's path (`01_count/count.c`) was used as the name of an evidence record, which
may not contain `/`. The directory has no summary and no seal; it is kept aside as
`bench/eval/breakit-20261119-partial` and is not evidence. The harness now names the record
`01_count-count.c` (a test seals a small campaign with an example in a subdirectory, which no test did), and E2
is run again in full, with the same command, into `bench/eval/breakit-20261119b`. Nothing else changes.

**Why.** A run that did not finish is not patched or resumed (design, section 7).

**Outcomes already seen.** None: the rows of the partial directory were not read. The generated programs and
the search are seeded, so the rerun judges the same removals.

### 15 — 2026-11-19: the first run of E4 was stopped by the machine and is run again with five workers

**Change.** `bench/eval/mutate-20261119` was stopped about twenty minutes after it started: the session that
had launched it killed the process because the machine was critically low on memory. It is not an error of
the harness and no command failed. Fifteen of the 3,768 mutants had a raw row; the directory has no summary
and no seal, is kept aside as `bench/eval/mutate-20261119-partial` and is not evidence. The workers' private
copies under `/tmp` were removed. E4 is run again in full into `bench/eval/mutate-20261119b`, with **five**
workers instead of the ten of amendment 13 (the author's decision, to halve the memory the run needs). Nothing
else changes: same population, same order of tests, same two layers, same time limits, one run, not resumed.

**Why.** A run that did not finish is not patched or resumed (design, section 7). The number of workers decides
how long the run takes, not what a mutant's outcome is, with one exception that is stated here in advance: a
layer's time limit is wall-clock, so fewer workers competing for the processor can only make a time-limit stop
less likely, never more.

**Outcomes already seen.** The fifteen rows of the stopped run were counted and their outcome column read once
when the directory was set aside: all fifteen "killed by tests". Nothing else of the population.

### 16 — 2026-11-19: `thesis-derived` is built, and how E7 compares PFC2 with Frama-C/WP

**Change.** (a) The corpus `thesis-derived`, named in the design and absent until now, is built by
`corpus/thesis-derived-notes/build.py` from the thesis repository: the six kernels, the eight ACSL-by-Example
ports and the three Zilu strata (30, 30 obfuscated, 15 composed), 89 programs. The rule is the include line
only: `#include "spec.h"` becomes `#include "pfc.h"`, an include of the program's own header is removed,
nothing else changes (`pfc.h` reads the older clause spellings). Sealed in `corpus/thesis-derived` with the
source hashes in `PROVENANCE.json`. Its role stays regression only.

(b) E7 is run by `python -m pfc2_eval verifier corpus/independent-verifier --output NEW`:

- **Cases.** 29: the 14 programs of the `kernels` and `acsl` strata of `thesis-derived`, with the ACSL files
  the thesis wrote by hand for the same function bodies (copied byte for byte, hashes checked against the
  thesis manifest); and 15 of the 21 examples, transcribed by hand for this experiment by the AI assistant.
  The six examples that include `pfc_rt.h` (calculator, greeter, the four console programs) are not stated:
  their behaviour is input and output through an unverified runtime and an opaque `string`. The Zilu strata
  are not transcribed (75 hand transcriptions of scalar loops); this is a limit of effort, stated as such.
- **Transcription rules.** Same executable body. `long a[n]` becomes `requires 0 <= n` and
  `\valid`/`\valid_read` of `a + (0 .. n-1)`; `separated` becomes `\separated` of the two ranges; arrays not
  declared separated may overlap, as in PFC2; an array is separated from the file's own globals (a caller
  cannot hold their address); `assigns` and `loop assigns` say what is written; written invariants are copied
  and the counter bounds PFC2 infers are written by hand; `decreases(e)` becomes `loop variant e`; functions
  carry `terminates \false` so that only loops with a variant are asked to terminate; a law becomes a function
  with the `where` clauses as `requires`, calls bound to locals and the claim as an `assert`.
- **Tool.** Frama-C 32.1 with Alt-Ergo 2.5.4 in the image pinned by the thesis repository
  (`framac/frama-c@sha256:4f0b7a2b…`), offline, one fresh container per case, options in `cases.json`: those
  of the thesis run plus `-warn-signed-downcast` (PFC2 has a conversion obligation), 10 s per goal.
- **Unit of comparison.** Sites cannot be paired mechanically between two differently laid out files, so the
  property is the pair (function, class), the classes being bounds, division, overflow, conversion,
  postcondition, assertion (with loop variants), call precondition, invariant on entry, invariant preserved.
  PFC2's obligations are read from `pfc2 check --json` at level `full` in a fresh process and counted by the
  function that holds their line; WP's goals are classed by their names. Outcomes: both prove everything in
  the cell (agree); neither does (agree, open); PFC2 does and WP leaves a goal open (inconclusive, by the
  design); WP does and PFC2 does not (**disagreement**); a class only one tool has goals in is listed apart
  and compared with nothing. WP's frame, termination and smoke goals have no PFC2 counterpart and are counted
  as support.
- **Negative controls.** The six of the thesis (missing bound, false invariant, non-preserved invariant,
  possible zero divisor, possible overflow, contradictory precondition): WP must leave the expected goal open.
- **Criterion.** As registered: 0 unclassified disagreements. The campaign passes with 0 disagreements, every
  case compared and every control detected; a disagreement is classified by hand afterwards, in the report.

**Why.** The design gives the population, the tool and the criterion and not the pairing. The class-level
pairing is coarser than a site-level one: a cell in which each tool leaves a different site open counts as
agreement. The counts on both sides are in the rows so that such a cell can be found.

**Outcomes already seen.** `thesis-derived`: all 89 certify at `memory` and 47 at `full` (checked right after
sealing). E7: one trial run of the `17_text` transcription while the options were being fixed (69 of 70 goals
valid; the postcondition of `digit_char` timed out). No comparison with PFC2 was computed before this entry.

### 17 — 2026-11-19: the held-out loop set as ported, and how E10 runs

**Change.** (a) **Two porting rules are added** to H1–H7, because the front end refuses what every upstream
task contains: (H8) a local declared without an initialiser is given the initialiser `0`, and a `main` that
falls off its end returns 0; (H9) a cast between integer types that H1 made the same type is removed. Both
keep every defined upstream execution: reading an uninitialised local is undefined upstream, and the cast is
the identity on `long`. Under H1–H7 alone **no** task ports (each declares `int i;` without a value); the
port rate is reported both ways. `main` becomes a function named after the task, with the parameters that
H2–H4 introduce.

(b) **Readings of the registered rules, fixed before any program was judged.** H5 "quantifier-free over
scalars": an assertion that reads an array element is not over scalars and is dropped, including the final
`sum[0] <= N` kind of `array-fpi`; the 67 ported `array-fpi` tasks are therefore about array bounds and
arithmetic only, and the five `loop-invgen` tasks keep all their assertions (they are inside loops, and all
are scalar). H3: an array allocated with `N` elements becomes `long a[N]`; a one-element array becomes an
array parameter with its own length parameter and `requires(len == 1)`. H4 cannot be applied when a
nondeterministic value is drawn inside a loop (no single parameter stands for it): such a task is excluded.
No `separated` is added: no rule adds one.

(c) **The set.** 96 tasks have a true verdict for `unreach-call` at the pinned commit (68 in `array-fpi`, 28
in `loop-invgen`). 72 are ported: 67 of `array-fpi` by `corpus/heldout-loops-notes/build.py`, which refuses
any line outside the family's pattern, and 5 of `loop-invgen` by hand with the same rules (`down`, `half_2`,
`id_build`, `seq-3`, `up`). 24 are excluded by rule: 19 use `goto` (11 of them are machine-reduced variants),
5 draw a nondeterministic value inside a loop. Only the front end was asked whether it reads each port. The
set is sealed in `corpus/heldout-loops` with `PROVENANCE.json`. It is external and public, **not blinded**.

(d) **The conditions**, run by `python -m pfc2_eval sources corpus/heldout-loops --output NEW --seed 100000
--live`, each ending in `adapter.check` or `adapter.admit` at level `memory`:

- N and I as registered.
- **B1.** Candidates of a loop: `x <= t` and `t <= x` for each scalar `x` in scope (parameters and locals
  declared before the loop) and each `t` among the other scalars in scope, 0, 1 and the integer literals of
  the function. Houdini: the loop carries the conjunction of the candidates alive; each candidate `c` is
  asserted as `houdini_probe != j || c` before the loop and at the end of the body (a `for` becomes a `while`
  with its update before the assertions), 24 candidates per probe program; a candidate is dropped only when
  its assertion fails with a counterexample; a round is one pass over all candidates; the budget is 5 rounds
  and, as the registered sensitivity analysis, 50. What is left is judged on the unchanged source.
- **B2.** The same filtering over candidates observed by the interpreter at each loop head on up to 200
  accepted inputs (at most 20,000 draws of the small domain of E2, seed `100000:<task>`), with at least 20
  states: `x == c`; `x == y + c` with |c| ≤ 8; `c <= x` and `x <= c` for an observed extreme with |c| ≤ 8;
  `x <= y + c` for the largest observed difference c in {−1, 0, 1}; `x == y + z`; `x == m*y + c` for m in
  {−2, −1, 2} and |c| ≤ 8; at most 60 per loop in that order.
- **L1 and L2.** `pfc2.llm.ask` as shipped (`gpt-6-astra`, reasoning effort low, 2,048 output tokens, no
  retries, JSON schema), one request per attempt. The instruction is the text `INSTRUCTION` of
  `pfc2_eval/sources.py`, written now and not changed afterwards: it differs from the product's in saying
  that overflow is trapped and need not be proved (the level is `memory`) and that there is one function and
  no law. L1: at most 5 attempts, each after the first with the previous reply and the checker's refusal
  (`pfc2.prove.feedback`). L2: the bare instruction up to 5 times, stopping at the first certificate. A failed
  request or a malformed reply uses up an attempt. R = 5 runs of each, per program. Every reply is kept in
  the evidence; the tasks are public.
- **Statistics** as registered: proportion certified with Wilson and Clopper–Pearson intervals; contrasts
  I − N, L1 − I, L1 − B2 (B2 at 5 rounds) paired by program (a program's value under a model condition is
  its proportion of certified runs), cluster bootstrap over programs with 10,000 resamples and seed 0, exact
  sign test, Holm over the three. E10 has no pass criterion; the campaign seals whatever it finds.

**Why.** The design names the conditions and leaves the families, the filtering and the instruction open.
Since H5 as read leaves 67 of 72 programs with nothing but bounds to prove, the built-in inference is
expected to certify most of the set, in which case the design's own clause applies (more than 90% under I:
no power for contrasts 2 and 3). That expectation is written here before the run.

**Outcomes already seen.** None on the set: no ported program was judged by PFC2, the interpreter, a baseline
or the model before this entry. The runner was tested on two toy programs written for its tests.

### 18 — 2026-11-19: the first run of E7 left one case uncompared and is run again

**Change.** `bench/eval/verifier-20261119` sealed with 28 of 29 cases compared, 0 disagreements and 6 of 6
controls detected, and therefore **not passed**: the case `example-15_matrix` was not compared. WP shortens a
function name of 62 characters (`the_determinant_of_a_product_is_the_product_of_the_determinants`) inside
its goal names, and the harness, which reads the function from the goal name, found no function for those
goals. The directory stays sealed as it is. The harness now also reads the `function` and `property` fields
of WP's report when the name does not fit (a test reproduces the shortened name), and E7 is run again in full
into `bench/eval/verifier-20261119b`. Cases, transcriptions, options and criterion are unchanged.

**Why.** A case that was not compared is not agreement; a run is not patched (design, section 7).

**Outcomes already seen.** All of the first run: per class, 198 cells in which both tools prove everything,
7 overflow cells that neither closes, 2 cells in which WP leaves a goal open that PFC2 proves (the
postcondition of `digit_char`, one bounds goal of `matvec`), 10 cells with PFC2 obligations and no WP goal.
The matrix case was run once more by hand to read WP's report format.

### 19 — 2026-11-19: how the Verina stratum is ported, specified and measured

**Change.** The design gives one line to Verina ("one task, re-expressed in C by hand from its description";
its tests; "its specification is written by others"). This entry fixes the procedure before any task is
ported. All 189 tasks of `datasets/verina` at the pinned commit are candidates, in the order of their
identifiers.

- **Interface, generated.** `corpus/verina-notes/interface.py` reads only each task's `task.json` (the Lean
  signature) and `test.json`, and writes: the C signature the port must have, a C test file, and the test
  transcriptions (`tests.json`). Mapping: `Int`, `Nat`, `Char`, `UInt8` parameters are `long`; arrays and
  lists of `Int`/`Nat` are `long x_len, const long x[x_len]`; `String` and arrays/lists of `Char` are
  `long s_len, const char s[s_len]`; an `Int`/`Nat` result is returned; a `Bool` result is returned as 1 or
  0; an array, list or string result is written to `out[out_cap]` and its length returned; a pair of numbers
  is `out[0], out[1]`; an `Option` is `out[0]` (1 or 0) and the value after it. The output buffer's capacity
  in the tests is the smallest power of two that is at least 8 and at least twice the longest array of the
  task's tests plus two.
- **Exclusion.** X1 (a `Float` in the signature) and X4 (a function parameter) as registered, and one new
  rule: **(X7)** the signature is outside the mapping above (nested lists, lists of pairs or of strings, a
  pair that holds a list, a map), or none of the task's tests can be written on the interface. A task whose
  description needs something the rules exclude (X2, X3, X5, X6) is excluded when it is ported, with the
  reason. 16 tasks are excluded by the generator: 2 by X1, 1 by X4, 13 by X7.
- **Tests.** Each test of `test.json` becomes one C test: the port is called on the test's input and the
  result must equal `expected` and differ from each value in `unexpected` (Verina's negative tests). A test
  with a value outside `long` or outside ASCII is recorded as not expressible and stays in the denominator of
  S3. `reject_inputs.json` (inputs outside the precondition) is not used: calling a C function outside its
  precondition is not a test. The tests run through the Unity files of the pinned Exercism checkout.
- **Port (first seal).** One function per task, written by hand by the AI assistant from `description.txt`,
  the generated signature and the generated tests; `task.lean` (reference code, specification, proof) is
  **not opened** in this step. Rules P1–P14 apply where they have something to act on, P8 above all: an
  ordinary, direct implementation of what the description says, not shaped for the prover. A port carries no
  contract except what the front end needs (`requires` on `out_cap`, on a `Nat` being non-negative, or on an
  index, when the port would otherwise not be valid C for the inputs the description allows — recorded per
  unit). It must pass the generated tests as plain C under sanitizers; fixes are counted. The ports are
  sealed in `corpus/verina-ports`.
- **Contract (second seal).** Verina's own precondition and postcondition (`task.lean`) restated in PFC2 on
  the sealed code: every part the language can state is stated; a part that needs a quantifier, a multiset,
  or a recursive definition is dropped and recorded per unit (`notes.json`: `stated` is `all`, `part` or
  `none`). No precondition is added beyond Verina's own, the `Nat` types, the capacity of `out` and the
  separation of `out` from the inputs: in particular values are not bounded to make arithmetic provable, so
  a unit whose arithmetic can overflow certifies at `memory` or not at all. Invariants, measures and
  assertions are added as the proof needs. The code must be identical to the sealed port (`same_code`).
  Sealed in `corpus/verina`; the 20% review sample is drawn with the registered seed after sealing.
- **Measures.** S1–S4 by the same harness and settings as the Exercism stratum (`python -m pfc2_eval corpus`,
  600 s per verdict), H4a and H4b computed the same way. The two strata are reported side by side and are
  not added together: in one the specification is ours, in the other it is Verina's restated by us.
- **Who.** Ports and contracts are drafted by the AI assistant, in several parallel sessions that follow
  `corpus/verina-notes/PROTOCOL.md`; this is stated wherever a number of this stratum appears.

**Why.** Without a fixed interface each port would choose its own, and tests and transcriptions would be
hand work that can drift; generated from the task's own data they cannot. Keeping `task.lean` closed while
porting keeps the port from being a transliteration of the reference solution.

**Outcomes already seen.** The tally of signature types and of test counts over the 189 tasks (to design the
mapping); the files of `verina_basic_1`, opened to learn the dataset's layout, whose port was written to try
the checking script (its tests pass). No other task was opened; no contract exists; nothing was measured.

### 20 — 2026-11-19: how E11 is run

**Change.** E11 is run by `python -m pfc2_eval runtime --output NEW --seed 100000 [--cpu N]`. The programs
are fixed in `pfc2_eval/runtime.py` before any is timed: the 14 programs of the `kernels` and `acsl` strata
of `thesis-derived` and 11 functions of the examples that take an array (`fill`, `sum`, `binary_search`,
`copy`, `play`, `handle`, `path_max`, `multiply`, `count_char`, `index_of`, `to_upper`), 25 in all. Arrays
have 2^24 elements, except where the contract fixes the size (`multiply`: 9 cells; `path_max`: 1,000,000;
`matvec`: a 4096 by 4096 matrix); a function that does constant or logarithmic work per call is called 2^20
times per repetition. Element values are small (`i % 7`, `i % 5`) so that no kept overflow trap fires. Each
program is built three ways with the flags of `C_FLAGS`: the source as plain C, the checked C, and the C
released at level `memory`. A driver appended to the translation unit refills the arrays before each of four
repetitions outside the timed region, calls the function through a volatile pointer, and prints the
nanoseconds spent in the calls and a checksum of every returned value and written array. The three builds
must print the same checksum; otherwise the program is a failure and is not timed. Three warm-ups, three
blocks of ten rounds, the builds in rotating order within a round; medians, and ratios paired by round with a
percentile bootstrap (2,000 resamples, seeded). Label as registered: `controlled` only with the
`performance` governor and an instruction counter, otherwise `exploratory`; the load average at the start
and the end is recorded. No instruction counts are taken (no counter is installed here).

**Why.** The design names the builds, the sizes and the protocol, and leaves the programs' inputs and the
driver open.

**Outcomes already seen.** None: no listed program was built or timed with this driver. The runner's test
times `fill` and `sum` of the examples on 1,000 elements to check that the builds agree.

### 21 — 2026-11-19: Verina ports sealed; one more exclusion rule, named after it was needed

**Change.** Step A of amendment 19 is done: of 189 tasks, 16 are excluded by the generator of the interface
(2 X1, 1 X4, 13 X7), 162 are ported and 11 are excluded while porting. Those 11 (longest increasing
subsequence, longest common subsequence and merge sort: `verina_advanced_2`, `_3`, `_4`, `_24`, `_25`, `_27`,
`_31`, `_32`, `_33`, `_34`, `_48`) need a scratch array as long as an input. The registered X2 does not cover
them (their storage *is* bounded by an input length); the working protocol told the porter to call them X2,
which was my wording and is wrong against the design. They are recorded under a new rule, **(X8)**: the
ordinary implementation needs a scratch array whose length depends on the length of an input; PFC2 has no
allocation and the generated interface passes no scratch buffer. This is a limit of PFC2 and of the fixed
interface, not of the tasks, and is reported as such; an interface with a caller-provided scratch parameter
would port them. The porters' own notes keep the label they wrote; `SELECTION.json` carries X8 with the
original reason beside it. Two fixes were needed in all (`verina_basic_30`: the tests expect the source
language's non-negative remainder; `verina_advanced_52`: a test calls with `k = 0`). The ports were written
by five parallel sessions of the AI assistant, each with `task.lean` closed, and every port was re-checked
afterwards in one run (162 pass their generated tests under sanitizers; none carries an `ensures`, an
invariant, an assertion or a law). Sealed in `corpus/verina-ports`.

**Why.** An exclusion must carry the rule that actually excludes it.

**Outcomes already seen.** The porters' remarks on descriptions that under-specify (recorded in each
`notes.json`) and that the ports pass their tests. No contract exists and nothing has been judged by PFC2
beyond the front end reading each port.

### 22 — 2026-11-19: Verina contracts written; what the writers did that the protocol did not foresee

**Change.** Step B of amendment 19 is done for the 162 ported tasks, by six parallel sessions of the AI
assistant working on the sealed code. Before the second seal, four things are recorded that the procedure of
amendment 19 did not settle, as the writers handled them:

1. **A length is a `Nat`.** The generated interface spells an array as `long x_len, const T x[x_len]`. PFC2
   reads a length named after its array as the older spelling and does **not** assume `0 <= x_len` (its
   documentation said it does; `docs/09-limits.md` now says what it does). Where a proof needed it, the
   writers added `requires(x_len >= 0)`, counting a list's length under "a `Nat` being non-negative" (each
   such clause is in the unit's source and its `notes.json`). Other
   writers left the bound out and wrote invariants that do not need it. Both are accepted; the difference is
   a property of the units and is not corrected after the fact.
2. **`stated` is not a comparable label across writers.** Some counted a restated precondition as "part",
   others required a conjunct of the postcondition; several stated consequences that are not conjuncts of
   Verina's specification (a Boolean result is 0 or 1, a length is in range) and labelled the unit "none".
   The label is therefore reported only as the writers' own classification, with this caveat, and no result
   is conditioned on it. What S3 measures does not depend on it.
3. **Clauses kept although the unit is then refused.** Where a part of the postcondition is statable but
   true only under a precondition that is not (a quantified one), some writers kept the `ensures` and the
   unit is refused (`verina_advanced_5`, `_54`, `_62`), others dropped it and recorded it as weakened
   (`verina_advanced_76`, `_78`, `_80`, `verina_basic_102`, `_69`). Both follow the protocol's text; the
   refused units stay in the corpus as refused. One writer added `requires(k <= nums_len)`
   (`verina_advanced_52`), a consequence of Verina's precondition and not a literal part of it.
4. **A shared scratch directory.** The sessions shared one scratch directory and two of them ran another
   session's generator script by mistake, which rewrote that session's units from its own script. Every unit
   was therefore re-checked afterwards in one run (tests, identity of code with the sealed port, verdict)
   and each verdict compared with the one its writer recorded.

Findings recorded while writing, none of them a result of the study yet: two ports disagree with Verina's
specification outside the tests (`verina_basic_107`: the average of a negative odd sum, where the source
language's division rounds differently from C's; `verina_advanced_43`: a division that is undefined in C
for one extreme input). They are port defects, to be listed as such under S5.

**Why.** The second seal freezes the contracts; what is known to be uneven about them is written before it.

**Outcomes already seen.** The writers saw PFC2's verdict on each unit while writing its contract, as the
design expects (step 3 of the protocol), and reported: 107 certified at `full`, 48 at `memory`, 7 refused.
No assertion was asked of a contract and no mutant was made before this entry.

### 23 — 2026-11-20: how the Verina mutants that the tests miss are read, and three descriptive breakdowns

**What.** Analyses of the sealed campaign `bench/eval/corpus-verina-20261119`. Nothing is rerun and nothing
sealed is edited; every mutant is regenerated from the sealed unit by the same function that made it
(`pfc2_eval.corpus.mutants`) and matched by its identifier and line.

1. **Which mutants.** The 300 mutants on which the upstream tests pass: 61 that the proof refuses with a
   failed obligation ("proof only") and 239 that neither catches (238 certified, one not judged).
2. **A seeded differential probe** (`corpus/verina-notes/probe.py`, seed 20261120). For each unit a host
   driver draws 4,000 inputs through the unit's own interface: array lengths 0 to 6, values from a small
   range (six draws in ten), a medium range (three in ten) or the extremes of `long` (one in ten); the
   output capacity is 32. An input is used only when the `requires` clauses written in the sealed unit hold
   on it (they are pasted into the driver as C) and when the sealed port itself runs on it without a
   sanitizer report and within 5 s. On every used input the mutant's result and its whole output array are
   compared with the port's, both built as plain C under AddressSanitizer and UBSan.
3. **Classes.** *Witnessed*: an input on which the mutant differs, by kind — the result, an output cell
   below the returned length, an output cell at or beyond it, a sanitizer report, or no answer in 5 s.
   *No witness*: nothing differed on any used input; such a mutant is then read by hand and classified as
   equivalent (with the reason) or as different (with an input found by hand, which is then run). A unit
   whose `requires` cannot be compiled as C, or with no used input, is reported as not probed.
4. **What a witness does not show.** For the 36 units whose notes record a Verina precondition as not
   statable, an input that satisfies the written `requires` may violate Verina's precondition. Witnesses
   in those units are counted apart as "under the written contract only".
5. **For the proof-only mutants,** the kinds of the failed obligations are recorded too (bounds, division,
   overflow, `ensures`, invariant, `decreases`, callee precondition), from a fresh check at the unit's level.
6. **Descriptive breakdowns, from the sealed rows and the sealed notes alone:** clause lines per code line
   (per unit, and by level); the subsumed fraction of assertions by the writers' label of the unit (`all`,
   `part`, `none`; amendment 22 item 2 says how uneven that label is) and by whether the function returns
   through an output array; the 2×2 table by mutation operator.

**Why.** The design asks for the surviving mutants to be classified, and the reading "proofs catch what tests
miss" needs to know whether a proof-only mutant is a fault or a refusal of a correct program. A probe with a
recorded input is checkable by anyone; a classification by reading alone is not.

**Who classifies.** The AI assistant, labelled as such; the author's review is pending. The probe's inputs are
random and small: "no witness" is not equivalence until read, and a hand classification as equivalent is an
argument, not a proof.

**Outcomes already seen.** The counts of the sealed campaign (the 2×2 table, H4a, H4b). No mutant text had
been regenerated or read before this entry.

### 24 — 2026-11-20: two additions asked for by the author — the thesis's held-out set through PFC2, and whole programs

**What.** The author asked for the experiments that a text presenting both compilers (`pfc`, the thesis's, and
PFC2) would need. Two are added. Neither is in DESIGN.md; both are **exploratory and post hoc**, are reported
apart from E1–E11 and the corpus study, and enter no registered hypothesis.

**A. The thesis's sealed held-out set, through PFC2 (experiment "bridge").**

1. *The set.* The 43 programs of `heldout/` in the thesis repository (SV-COMP `array-tiling` and
   `array-multidimensional`, ported for `pfc` by its rules R1–R8, sealed there on 2026-11-10). It is external
   but not blinded, and the thesis's results on it are known: B1 13/43, B2 35/43 and the model 43/43 at five
   rounds; B1 34/43 and B2 42/43 at fifty.
2. *The rule* (`corpus/thesis-heldout-notes/build.py`): R1–R3 of amendment 16 (the include line; nothing else
   re-spelled), and R4: every line that is an `INVARIANT(...)` clause is removed, because the experiment asks
   who supplies them. The canary comment of each kernel is kept. Nothing is excluded: a program PFC2 rejects
   is a row.
3. *The run.* `pfc2_eval sources` on the sealed copy, seed 100000, without the model: conditions N, I, B1 and
   B2 at 5 and at 50 rounds, level `memory`, exactly as amendment 17 fixed them for E10. No model request is
   made: the thesis already measured a model on this set and the question here is what PFC2 does without one.
4. *What may be said.* Counts per condition with their intervals, beside the thesis's counts, as a
   description. No difference between the two compilers is tested: the admission rules differ on purpose
   (PFC2 keeps an overflow trap where `pfc` kept a guard), the baselines were re-implemented, and I do not
   know whether PFC2's inference was written with this set in view. The programs are the same; the
   measurements are not paired.

**B. Whole programs.**

1. *The tool's own examples* (`examples/`, every file outside `wrong/`): lines of code, clause lines, level,
   obligations, guards and traps removed and kept, the unverified parts listed in the proof file, check time.
   A description of what exists; these programs were written with the tool and say nothing about effort.
2. *Ten programs written from prose by fresh AI sessions* (`corpus/whole-programs/`). The ten tasks, each
   with its input and expected output, are written in `corpus/whole-programs-notes/TASKS.md` before any
   session starts and are not changed afterwards. Each session is an AI assistant that has not seen this
   conversation; it is given the language documentation (`docs/01`–`docs/09`), one task, and a logged
   checker (`corpus/whole-programs-notes/check.py`), which appends one record per invocation: the SHA-256 of
   the source, the verdict, the level, and the kinds of the failed obligations. A task is *done* when the
   program is certified (at `full`, or at `memory` with the reason written down) and its certified build
   prints the expected output on the task's input; a session may give up and say why.
3. *What is reported, per task:* done or not; level; code and clause lines; number of logged checks and of
   distinct source versions; refusals by kind; the session's own notes on what was hard. Qualitative, no
   statistics, as the plan says of this step.
4. *Limits, stated before the outcome:* the writer is an AI model, so "effort" is a count of checker
   round-trips, not of a person's hours; the tasks were chosen by the same assistant that runs the study, to
   be small and to fit the language (console input, integers, fixed arrays, state machines); ten programs of
   this size are not evidence about large software. The transcripts of the expected output are written by
   hand before any implementation exists; a transcript found wrong is corrected in the open and the task
   marked.

**Why.** A text with both compilers needs one measurement on the same programs, and the plan's last step of
Phase 4 (about ten whole small programs) had not been done.

**Outcomes already seen.** For A: the thesis's results on the set, as listed; three development kernels of
`thesis-derived` were run through the same code path to check that it reads the older spelling, and no
held-out program was. For B.1: `examples/examples.json` records the expected level of every example. For
B.2: none.

### 25 — 2026-11-21: E4 runs each mutant under a memory limit, and a stopped layer stops its whole process group

**What was registered.** E4 (design section 6, amendments 13 and 15): every mutant is judged in a private copy by
the test suite and then by E1 on 50 programs; a layer that exceeds its wall-clock limit (40 and 60 minutes) counts
as killed and is reported apart. Nothing was said about memory.

**What happened.** Three campaigns did not seal. `mutate-20261119` (ten workers) and `mutate-20261119b` (five
workers, about 2,180 of 3,768 mutants after 32 hours) were killed by the tool that launched them when the machine
ran short of memory. `mutate-20261121` (five workers, nothing else running) was killed the same way after half an
hour and 29 mutants, and this time memory was logged every five minutes: used memory went from 6 GB to 28 GB of
31, and the largest process was one `python3` of 10 GB. Some mutants make a test or solver process grow without
bound; the harness had a time limit and no memory limit. Separately, one mutant's test binary was found still
running ten hours after its layer had timed out, because the time limit stopped the layer's first process and not
the processes it had started.

**What changes, before the next campaign starts.** In `pfc2_eval/mutate.py`:

1. Each layer runs in a session of its own. Twice a second the harness adds up the resident memory of every
   process of that session. If the sum exceeds **4 GiB** the whole session is killed and the mutant's outcome is
   `memory limit in tests` or `memory limit in e1`.
2. When a layer exceeds its wall-clock limit, the whole session is killed, not only its first process. The
   outcome names are unchanged.
3. A mutant stopped by the memory limit **counts as killed**, like one stopped by the time limit, and is
   **reported apart** in its own two columns. The report gives the score with those mutants as killed (the
   registered reading extended) and also the score with both limit columns left out of numerator and denominator,
   so a reader can see how much of the score rests on limits.
4. Every row records the largest sum observed (`peak_rss_mb`), so the choice of 4 GiB can be judged afterwards.

**Why 4 GiB.** Five workers at the limit use 20 GiB on a machine with 31, which leaves room for the rest; the
unmutated test suite and E1 on 50 programs were observed to add well under 1 GiB to the machine's used memory
when run alone on 2026-11-20 and 21. Before the campaign, a change that alters no behaviour (a comment added to a
target file) is judged through both real layers with the limit in force; if it does not survive, or its peak is
near the limit, the limit is wrong and the campaign does not start. The peak of that rehearsal is recorded in the
Phase 3 report.

**What is not changed.** The population, the operators, the two layers, their order, their time limits, the 50
programs and their seed, the threshold of 0.90, and the rule that survivors are classified one by one.

**Limits of this change.** A mutant stopped by either limit was not shown wrong by an assertion: it is
"detected" only in the sense that it cannot pass unnoticed. A mutant that would have failed a later test but
exhausts memory first is recorded under the limit, not under the test. The limit is on resident memory sampled
twice a second, so a process can exceed it briefly. `tests/eval/test_eval_mutate.py` is in the baseline inventory
and changes with this; the inventories are rewritten with `tools/freeze.py --write pfc2-v3` and the protected
digest must come out as before (`115f5ad6…35b6ee`).

**Outcomes already seen.** The partial rows of the three unfinished campaigns (interim counts were looked at on
2026-11-20: at 2,018 rows, 1,600 killed, 401 survived, 17 time-limit). None of those rows is used; the new
campaign judges every mutant again from zero in a new directory.

**Addition, the same day, before the campaign.** The full check run before the campaign failed once in
`tests/eval/test_eval_differential.py` (the test of a program that cannot be judged in time), and passed three
times alone. Cause: the harness's timer fired while the solver binding was converting an argument, and `ctypes`
reported the timer's exception as its own `ArgumentError`, which `differential.one_program` did not recognise as
"out of time". In E4 that test is part of the first layer, so the race could stop a mutant that the tests did not
in fact notice. `one_program` now treats an `ArgumentError` that names the timer's exception as out of time and
re-raises any other (one test added, seen failing first). The registered outcome "not judged within the time
budget" is unchanged. The same timer pattern exists in `breakit.py`, `surfaces.py`, `inject.py` and
`robustness.py`, which E4 does not run; they are not changed. The sealed E1 campaigns ran the earlier code: a
program hit by this race there would have ended its worker with an error, and none did. In the E4 report, every
mutant whose `stopped_by` names this test is read by hand.

### 26 — 2026-11-23: E4 sealed below its threshold; a flaky harness test in its first layer, found after the seal

**What was registered.** E4: mutation score of at least 0.90 over the twelve files, limits reported apart
(amendments 13, 15, 25). Amendment 25's addition: the timer race was repaired in `differential.one_program`
only, on the stated ground that E4 does not run `breakit.py`, `surfaces.py`, `inject.py` or `robustness.py`;
every mutant whose `stopped_by` names the timer test is read by hand.

**What happened.** `bench/eval/mutate-20261121b` sealed on 2026-11-23: 3,036 of 3,768 killed, score 0.806
[0.793, 0.818], **criterion not met**; 47 stopped by a limit (0.803 without them). The hand reading found that
68 kills name `tests/eval/test_eval_surfaces.py::test_a_program_that_cannot_be_judged_in_time_is_a_row_that_compares_nothing`.
The ground stated in amendment 25 was wrong: E4 does not run the `surfaces` experiment, but its first layer runs
that module's tests, and `surfaces.within_budget` has the unrepaired race. On the unmutated tree the test failed
2 times in 35 runs alone.

**What was done, after the outcome was known (post hoc, not evidence of the campaign).** Three rechecks on
private copies, outside the sealed directory (`docs/evaluation/reports/PHASE-3-e4-timer-recheck/`): 23 of the 68
are stopped by another test; 13 fail the timer test three times of three; **32 pass the whole test layer and E1
on 50 programs once that one test is deselected**. Those 32 were recorded as killed because a flaky test failed.

**How it is reported.** The sealed directory is not edited and the campaign is not run again. The registered
number stays 0.806; every statement of it carries the corrected reading beside it: 3,004 of 3,768 = 0.797
[0.784, 0.810]. The verdict is "not met" under both. The corrected reading is labelled post hoc wherever it
appears and is never the number of record.

**What is not changed.** The population, the layers, the limits, the threshold, and the rule that survivors are
classified one by one (none is yet; "0 equivalent" means none read).

**Open, and each needs its own entry when done.** Repairing `surfaces.within_budget` and reading `breakit.py`,
`inject.py` and `robustness.py` for the same race (a harness change with a test first, and the inventories
rewritten); the classification of the survivors; any test added for a survivor, and any rerun after it, which
would be a post hoc campaign reported apart.

**Limits of the correction.** One run per recheck. Only kills that name that one test were examined: a second
flaky test at a lower rate would not have been seen. A flaky failure can only turn a survivor into a kill, so the
732 recorded survivors are unaffected and the corrected score is an upper reading, not a lower one.

### 27 — 2026-11-23: the timer race is repaired in the four remaining harness modules

**What was open (entry 26).** `surfaces.within_budget` and the `one_program` of `robustness.py`, `inject.py` and
`breakit.py` treat only the timer's own exception as "out of time"; when the timer fires while `ctypes` converts
an argument of a solver call, `ctypes` raises its `ArgumentError` naming that exception instead.

**What changes.** Each of the four now treats an `ArgumentError` that names the timer's exception as out of time
and re-raises any other, exactly as `differential.one_program` does since entry 25. One parametrised test per
module (the wrapped timer is "not judged"; another `ArgumentError` is still raised), each seen failing first.
The registered outcome "not judged within the time budget" is unchanged, and no other behaviour changes.

**Check.** The test that failed 2 times in 35 runs before the change
(`test_eval_surfaces.py::test_a_program_that_cannot_be_judged_in_time_is_a_row_that_compares_nothing`) passed 40
times of 40 after it. That is evidence the race is closed, not a proof.

**What it does not touch.** No sealed campaign is rerun or edited. The sealed E2, E3, E5 and E12 campaigns ran
the earlier code: a program hit by this race there would have ended its worker with an error, and none did. E4's
sealed score keeps the 32 kills that the flaky test caused (entry 26). Four test files of the baseline inventory
changed; the inventories were rewritten with `tools/freeze.py --write pfc2-v3` and the protected digest is
unchanged (`115f5ad6…35b6ee`).

### 28 — 2026-11-23: the E4 survivors are classified by the AI assistant, and tests are added for the unsound direction

**What was registered.** Survivors are classified one by one; the score excludes mutants classified equivalent;
the classifier and the review status are stated (design, E4; amendment 13).

**What was done, at the author's request, after the outcome was known.** (a) All 732 sealed survivors and the 32
mutants of entry 26 were classified by the AI assistant, one session per target file, into equivalent, unreached,
report only and verdict (with a direction), by reading and, for 521 of the 764, by running the mutated file in a
private copy against small programs. The record is `docs/evaluation/reports/PHASE-3-e4-survivors.json`; the
author has not reviewed it. (b) For every mutant of the unsound direction (128) and three tamper cases of
`authorization`, tests were written (`tests/test_mutation_gaps_*.py`, 285 cases) and each mutant was seen to fail
them in a private copy while the unmutated tree passes (`docs/evaluation/reports/PHASE-3-e4-gap-tests/`).

**Numbers.** 84 equivalent, 94 unreached, 237 report only, 317 verdict (125 unsound direction, 76 conservative,
26 crash, 90 other). Score excluding equivalents: 3,036 of 3,684 = 0.824 [0.812, 0.836], **not met**; with the
correction of entry 26, 3,004 of 3,677 = 0.817.

**How it is reported.** The classes are the assistant's and are labelled so everywhere. The sealed directory is
not edited; its summary still says "classified equivalent: 0" because it was sealed before the reading. The tests
are post hoc: they change no sealed number, and no campaign was run with them. The new test files join the
baseline inventory (`tools/freeze.py --write pfc2-v3`); the protected digest is unchanged (`115f5ad6…35b6ee`).

**Limits.** Equivalence by reading is an argument. A probe that finds no difference shows nothing; the sessions
were warned of two ways a probe can silently run the unmutated code and reran the affected ones, by their own
account. The class boundaries are judgements (a changed resource limit is "report only" in some files and
"verdict" in `vc`; a traceback in place of a diagnostic on a refused program is "report only"), stated per
entry. Tests derived from witnesses close the weaknesses found and say nothing about those not found.

### 29 — 2026-11-23: the author's first review, on a seeded sample, with AI assistance

**What was registered.** Classifications are the AI assistant's and are labelled so until the author reviews
them (design; amendments 23 and 28).

**What happened.** `tools/author_review.py sample` (seed 20261123) drew 50 mutants (20 E4 survivors, 20 Verina,
10 Exercism) and 15 contracts, stratified by the assistant's label, with the labels hidden. The author answered
all of them and declared that the judgments are his, made with an AI assistant that ran twelve private-copy
probes and drafted the notes (`docs/evaluation/reports/author-review/`: `ANSWERS.json`, `REVIEW-NOTES.md`,
`PROBES.json`, `REVIEW-PROVENANCE.json`).

**Agreement with the assistant's labels** (`tools/author_review.py score`):

| Stratum | Items | Agreement | Cohen's kappa |
| --- | ---: | ---: | ---: |
| E4 engine mutants | 20 | 0.95 | 0.90 |
| Verina corpus mutants | 20 | 0.95 | 0.90 |
| Exercism corpus mutants | 10 | 1.00 | 1.00 |
| All mutants | 50 | 0.96 | 0.92 |
| Verina contracts, how much of the specification is stated | 12 | 0.75 | 0.60 |
| Exercism contracts, same question | 3 | 1.00 | undefined |

Both mutant disagreements are items the assistant called equivalent and the author different, and both turn on
the definition: `smt-0332` changes a timing field that no output prints, and `verina_advanced_59/m012` changes
the result of a helper that its only caller reads through `!`. The three contract disagreements are between
adjacent categories. On "the contract restates the body" the author agrees with the assistant's separate reading
(`PHASE-4-contract-restatement.json`) in 7 of the 9 units both judged, including the three Exercism units.

**How it is reported.** As the author's review of a sample with AI assistance, never as a review of the whole
classification. The sample is stratified, so these figures describe the sampled items and are not an error rate.
The reviewer was not blind to the aggregate results or to the manuscript. No classification file was changed on
the strength of the two disagreements.

### 30 — 2026-11-23: a constructed shared-error case, and "restates" split by origin

**What was registered.** S3 (subsumption) and S4 (detection) as the two measures of what a contract adds.

**What was added, post hoc, for the thesis text.** (a) `corpus/shared-error-notes/` (script `run.py`, result
`docs/evaluation/reports/PHASE-4-shared-error.json`): the same error is put into the code and into the contract of
`queen-attack`, for each of the four sealed mutants that the upstream tests do not kill, and the unit is measured
with the unchanged harness (`pfc2_eval.corpus.measure`). Every constructed program is certified at `full`, all 13
upstream assertions still follow from its contract, the proof refuses every mutant of its code (17 of 17 or 18 of
18), the upstream tests pass, and each returns a different value from the reference solution on one recorded call.
On both measures the wrong program scores as the correct one. A constructed case on one unit; not part of any
sealed campaign. (b) `PHASE-4-contract-restatement.json` gains, for the 17 contracts classified as restating the
body, an origin: 12 *definitional* (the upstream requirement is itself that expression), 3 *copy* (an independent
property was available), 2 *unclear*; under the opposite precedence rule the counts are 15, 0 and 2, and both are
recorded. This is the AI assistant's classification, unreviewed. (c) `tools/author_review.py restatement-sample`
writes a sheet for the author with those 17 units and no labels; `restatement-score` scores it.

**How it is reported.** S3 and S4 measure how strongly a contract constrains the code; they do not show that the
contract states the requirement, nor that it is independent of the implementation. The origin counts are quoted
only as the assistant's reading until the author fills the sheet.

### 31 — 2026-11-23: the author's judgment of the origin of the 17 restating contracts

The author judged the sheet of entry 30 (`author-review/RESTATEMENT-ANSWERS.json`, provenance beside it): 8
definitional, 3 copy, 6 unclear, the six being those where an alternative formulation exists but may be only a
rewrite of the same definition. Against the assistant's labels (12, 3, 2): agreement 11 of 17, Cohen's kappa 0.41.
Two of the three contracts each reading calls a copy are the same (`abs`, `min`). **How it is reported:** the
split by origin is not reliable enough to be quoted as counts; what both readings support is that most restating
contracts are not clear copies and that a few are. No classification file was changed.

### 32 — 2026-11-23: an unlabelled sheet of all 32 contracts for an independent second rater

**What was registered.** Nothing on who reads the contracts: the classification of the 32 contracts (29 Verina, 3
Exercism) as restating the function body or not (`PHASE-4-contract-restatement.json`: 17 restates, 7 partly, 8
independent) is the AI assistant's, and entries 30 and 31 concern only the origin of the 17.

**What was added, post hoc, at a reviewer's request.** `tools/author_review.py second-rater-sheet` writes
`docs/evaluation/reports/second-rater/`: `SHEET.md` (the rule, two worked examples that are not among the units,
then all 32 units in an order drawn with seed 20261123, each under an opaque identifier with the upstream
requirement, the contract and the body, and none of the assistant's labels or reasons), `ANSWERS.json` (empty),
`KEY.json` and `README.md`. One binary question, restates the body or states a property in different terms, with
an `unclear` option. `second-rater-score` refuses an unfinished form, never writes the answers file, and writes
`SCORE.json`: units, agreement count, Cohen's kappa over the two labels, the count of `unclear` (left out of both
figures) and the disagreeing units. The assistant's `partly` and `independent` both count as "different"; the score
is also given without the 7 `partly` units. Both readings were fixed before any answer existed.

**How it is reported.** The answers are the second rater's alone; neither the assistant nor the author fills them.
The sheet has not been answered. Until it is scored, the text keeps "order of magnitude" for the share of restating
contracts and quotes no agreement figure. No classification file was changed.

### 33 — 2026-11-23: the sheet of the 32 contracts was answered by the author (post hoc)

**What changed from entry 32.** No reader from outside the project was available. By the author's decision the
author filled `second-rater/ANSWERS.json` himself, reading only `SHEET.md` (`NOTE-AUTHOR.md`,
`PROVENANCE.json`). Entry 32 said the author would not fill it; this entry replaces that sentence.

**Result.** Agreement with the first reading on 27 of 32, Cohen's kappa 0.69; on the 23 units the author had not
judged before, 19 of 23, kappa 0.66. The five disagreements go one way: the author read "different" where the first
reading had "restates" (`verina_basic_50`, `91`, `92`, `93`, `96`). Restating contracts by reading: Verina 9
(author) or 14 (first reading) of 29; Exercism 3 of 3 in both.

**How it is reported.** As a reading by the author, blind to the labels, not as an independent rater; the share
of restating contracts is quoted as the range 9 to 14 of 29. No classification file was changed.
