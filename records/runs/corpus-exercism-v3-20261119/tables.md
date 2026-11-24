# Tests versus proofs on ported units

| Unit | Verdict | Upstream tests | On port | On certified C | Code lines | Clause lines |
| --- | --- | ---: | --- | --- | ---: | ---: |
| collatz-conjecture | memory | 6 | pass | pass | 16 | 4 |
| difference-of-squares | full | 9 | pass | pass | 18 | 8 |
| hamming | full | 9 | pass | pass | 13 | 3 |
| hello-world | full | 1 | pass | pass | 4 | 1 |
| high-scores | full | 7 | pass | pass | 36 | 11 |
| largest-series-product | refused-failed | 13 | pass | None | 49 | 7 |
| leap | full | 9 | pass | pass | 13 | 1 |
| luhn | refused-failed | 22 | pass | None | 38 | 4 |
| nth-prime | memory | 5 | pass | pass | 22 | 6 |
| pangram | full | 11 | pass | pass | 27 | 5 |
| perfect-numbers | full | 14 | pass | pass | 31 | 7 |
| queen-attack | full | 13 | pass | pass | 13 | 5 |
| resistor-color-duo | full | 7 | pass | pass | 4 | 2 |
| resistor-color-trio | full | 10 | pass | pass | 20 | 8 |
| reverse-string | full | 6 | pass | pass | 11 | 4 |
| rna-transcription | full | 6 | pass | pass | 17 | 5 |
| robot-simulator | memory | 18 | pass | pass | 46 | 12 |
| scrabble-score | refused-failed | 11 | pass | None | 19 | 4 |
| sum-of-multiples | full | 16 | pass | pass | 11 | 7 |
| two-bucket | refused-failed | 9 | pass | None | 97 | 22 |
| yacht | refused-failed | 29 | pass | None | 87 | 27 |

Upstream assertions restated as laws over the contract alone.

| Unit | Assertions | Subsumed | Not subsumed | Not expressible | Not judged or error |
| --- | ---: | ---: | ---: | ---: | ---: |
| collatz-conjecture | 6 | 3 | 3 | 0 | 0 |
| difference-of-squares | 9 | 0 | 9 | 0 | 0 |
| hamming | 9 | 5 | 4 | 0 | 0 |
| hello-world | 1 | 0 | 0 | 1 | 0 |
| high-scores | 12 | 6 | 6 | 0 | 0 |
| leap | 9 | 9 | 0 | 0 | 0 |
| nth-prime | 5 | 0 | 5 | 0 | 0 |
| pangram | 11 | 2 | 9 | 0 | 0 |
| perfect-numbers | 14 | 3 | 11 | 0 | 0 |
| queen-attack | 13 | 13 | 0 | 0 | 0 |
| resistor-color-duo | 7 | 7 | 0 | 0 | 0 |
| resistor-color-trio | 20 | 0 | 20 | 0 | 0 |
| reverse-string | 6 | 1 | 5 | 0 | 0 |
| rna-transcription | 6 | 1 | 5 | 0 | 0 |
| robot-simulator | 54 | 6 | 48 | 0 | 0 |
| sum-of-multiples | 16 | 2 | 14 | 0 | 0 |

Mutants: tests kill / proof refuses with a failed obligation.

| Unit | Mutants | Both | Tests only | Proof only | Neither | Proof inconclusive | Rejected by front end |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| collatz-conjecture | 20 | 5 | 15 | 0 | 0 | 0 | 0 |
| difference-of-squares | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| hamming | 6 | 5 | 1 | 0 | 0 | 0 | 0 |
| hello-world | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| high-scores | 30 | 20 | 1 | 5 | 4 | 0 | 0 |
| leap | 21 | 19 | 0 | 0 | 2 | 0 | 0 |
| nth-prime | 15 | 12 | 2 | 0 | 1 | 0 | 0 |
| pangram | 20 | 2 | 11 | 0 | 7 | 15 | 0 |
| perfect-numbers | 29 | 16 | 9 | 0 | 4 | 0 | 0 |
| queen-attack | 18 | 14 | 0 | 4 | 0 | 0 | 0 |
| resistor-color-duo | 7 | 7 | 0 | 0 | 0 | 0 | 0 |
| resistor-color-trio | 31 | 16 | 8 | 3 | 4 | 0 | 0 |
| reverse-string | 4 | 3 | 0 | 0 | 1 | 0 | 0 |
| rna-transcription | 11 | 9 | 0 | 2 | 0 | 0 | 0 |
| robot-simulator | 57 | 15 | 32 | 4 | 6 | 0 | 0 |
| sum-of-multiples | 7 | 3 | 4 | 0 | 0 | 0 | 0 |
