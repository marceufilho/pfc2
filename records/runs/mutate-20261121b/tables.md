# E4: mutation of the engine

Mutants: 3768; killed: 3036; survivors: 732; score 0.806 (threshold 0.9); classified equivalent: 0.

Stopped by a time or memory limit (counted as killed): 47; score with those mutants left out of both counts: 0.8032786885245902.

| File | killed by tests | killed by e1 | timeout in tests | timeout in e1 | memory limit in tests | memory limit in e1 | survived |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pfc2/clauses.py | 331 | 0 | 10 | 0 | 0 | 0 | 84 |
| pfc2/core/authorization.py | 75 | 0 | 5 | 0 | 0 | 0 | 34 |
| pfc2/core/desugar.py | 135 | 0 | 1 | 0 | 0 | 0 | 22 |
| pfc2/core/emit.py | 403 | 3 | 9 | 0 | 0 | 0 | 108 |
| pfc2/core/lower.py | 469 | 0 | 1 | 0 | 3 | 0 | 96 |
| pfc2/core/smt.py | 394 | 0 | 2 | 0 | 0 | 0 | 112 |
| pfc2/core/vc.py | 71 | 0 | 0 | 0 | 4 | 0 | 31 |
| pfc2/core/wp.py | 404 | 0 | 0 | 0 | 0 | 0 | 91 |
| pfc2/elaborate.py | 291 | 0 | 1 | 0 | 1 | 0 | 40 |
| pfc2/gate.py | 64 | 0 | 0 | 0 | 0 | 0 | 13 |
| pfc2/infer.py | 209 | 0 | 3 | 0 | 0 | 0 | 47 |
| pfc2/preprocess.py | 140 | 0 | 7 | 0 | 0 | 0 | 54 |

| Operator | killed by tests | killed by e1 | timeout in tests | timeout in e1 | memory limit in tests | memory limit in e1 | survived |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| arithmetic | 78 | 0 | 0 | 0 | 1 | 0 | 20 |
| boolean | 715 | 1 | 8 | 0 | 0 | 0 | 102 |
| constant | 468 | 0 | 8 | 0 | 5 | 0 | 335 |
| relational | 470 | 1 | 7 | 0 | 0 | 0 | 93 |
| return-replacement | 303 | 0 | 1 | 0 | 0 | 0 | 46 |
| statement-deletion | 952 | 1 | 15 | 0 | 2 | 0 | 136 |
