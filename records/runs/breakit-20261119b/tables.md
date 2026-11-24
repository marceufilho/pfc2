# E2: one `requires` conjunct removed at a time

## Generated programs (the registered population)

| What the small-domain search found | As expected | Removals | Rate |
| --- | ---: | ---: | ---: |
| a witness: the certificate must be lost (sensitivity) | 622 | 622 | 1.000 |
| no witness in the domain: nothing may change (specificity) | 1945 | 1990 | 0.977 |
| only an overflow: a trap kept again, or the certificate lost | 130 | 130 | 1.000 |

Not decided by the interpreter: 0; not accepted by the front end: 0.

## Examples (development data, reported apart)

| What the small-domain search found | As expected | Removals | Rate |
| --- | ---: | ---: | ---: |
| a witness: the certificate must be lost (sensitivity) | 28 | 28 | 1.000 |
| no witness in the domain: nothing may change (specificity) | 11 | 12 | 0.917 |
| only an overflow: a trap kept again, or the certificate lost | 34 | 34 | 1.000 |

Not decided by the interpreter: 3; not accepted by the front end: 0.

Domain: up to 5000 draws per removal, stopping at 300 usable; scalars [-9223372036854775808, -51, -50, -49, -9, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 49, 50, 51, 9223372036854775807]; lengths [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]; elements [-2, -1, 0, 1, 2, 9].
