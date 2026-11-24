# E10: sources of invariants

Programs: 43. Success is a certificate at level `memory`.

| Condition | Certified | Trials | Proportion | Wilson 95% | Clopper-Pearson 95% |
| --- | ---: | ---: | ---: | --- | --- |
| N | 0 | 43 | 0.0 | [0.0, 0.082] | [0.0, 0.0822] |
| I | 43 | 43 | 1.0 | [0.918, 1.0] | [0.9178, 1.0] |
| B1 | 6 | 43 | 0.1395 | [0.0656, 0.2726] | [0.053, 0.2793] |
| B2 | 29 | 43 | 0.6744 | [0.5252, 0.7951] | [0.5146, 0.8092] |
| L1 | 0 | 0 | None | None | None |
| L2 | 0 | 0 | None | None | None |
| B1 (50 rounds) | 25 | 43 | 0.5814 | [0.4333, 0.7162] | [0.4213, 0.7299] |
| B2 (50 rounds) | 35 | 43 | 0.814 | [0.6738, 0.9026] | [0.666, 0.9161] |

## Registered contrasts

| Contrast | Difference | 95% interval | Sign test p | Holm | Supported |
| --- | ---: | --- | ---: | ---: | --- |
| I - N | 1.0 | [1.0, 1.0] | 2.274e-13 | 2.274e-13 | yes |

No power for the model contrasts (more than 90% under I): True.

## array-multidimensional

| Condition | Certified | Trials |
| --- | ---: | ---: |
| N | 0 | 20 |
| I | 20 | 20 |
| B1 | 0 | 20 |
| B2 | 9 | 20 |
| L1 | 0 | 0 |
| L2 | 0 | 0 |
| B1 (50 rounds) | 12 | 20 |
| B2 (50 rounds) | 14 | 20 |

## array-tiling

| Condition | Certified | Trials |
| --- | ---: | ---: |
| N | 0 | 23 |
| I | 23 | 23 |
| B1 | 6 | 23 |
| B2 | 20 | 23 |
| L1 | 0 | 0 |
| L2 | 0 | 0 |
| B1 (50 rounds) | 13 | 23 |
| B2 (50 rounds) | 21 | 23 |
