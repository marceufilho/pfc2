# E10: sources of invariants

Programs: 72. Success is a certificate at level `memory`.

| Condition | Certified | Trials | Proportion | Wilson 95% | Clopper-Pearson 95% |
| --- | ---: | ---: | ---: | --- | --- |
| N | 0 | 72 | 0.0 | [0.0, 0.0507] | [0.0, 0.0499] |
| I | 67 | 72 | 0.9306 | [0.8475, 0.97] | [0.8453, 0.9771] |
| B1 | 4 | 72 | 0.0556 | [0.0218, 0.1343] | [0.0153, 0.1362] |
| B2 | 69 | 72 | 0.9583 | [0.8845, 0.9857] | [0.883, 0.9913] |
| L1 | 355 | 360 | 0.9861 | [0.9679, 0.9941] | [0.9679, 0.9955] |
| L2 | 355 | 360 | 0.9861 | [0.9679, 0.9941] | [0.9679, 0.9955] |
| B1 (50 rounds) | 68 | 72 | 0.9444 | [0.8657, 0.9782] | [0.8638, 0.9847] |
| B2 (50 rounds) | 69 | 72 | 0.9583 | [0.8845, 0.9857] | [0.883, 0.9913] |

## Registered contrasts

| Contrast | Difference | 95% interval | Sign test p | Holm | Supported |
| --- | ---: | --- | ---: | ---: | --- |
| I - N | 0.9306 | [0.8611, 0.9861] | 1.355e-20 | 4.066e-20 | yes |
| L1 - I | 0.0556 | [0.0139, 0.1111] | 0.125 | 0.25 | no |
| L1 - B2 | 0.0278 | [0.0, 0.0694] | 0.5 | 0.5 | no |

No power for the model contrasts (more than 90% under I): True.

## array-fpi

| Condition | Certified | Trials |
| --- | ---: | ---: |
| N | 0 | 67 |
| I | 66 | 67 |
| B1 | 3 | 67 |
| B2 | 66 | 67 |
| L1 | 330 | 335 |
| L2 | 330 | 335 |
| B1 (50 rounds) | 66 | 67 |
| B2 (50 rounds) | 66 | 67 |

## loop-invgen

| Condition | Certified | Trials |
| --- | ---: | ---: |
| N | 0 | 5 |
| I | 1 | 5 |
| B1 | 1 | 5 |
| B2 | 3 | 5 |
| L1 | 25 | 25 |
| L2 | 25 | 25 |
| B1 (50 rounds) | 2 | 5 |
| B2 (50 rounds) | 3 | 5 |
