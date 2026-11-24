# The author's reasons, unit by unit

Written by the author after `ANSWERS.json` was fixed and scored (2026-11-23); recorded here as he sent them. The
answers were not changed afterwards.

| Unit | Answer | Reason |
| --- | --- | --- |
| U01 | different | `result == n % 10` copies the return expression, but `0 <= result && result < 10` adds a bound on the result. The rule says that additional property determines the label. |
| U02 | different | The body doubles `x` and adds `x`. The contract undoes multiplication through division, requiring both recovery of `x` and exact divisibility by three. |
| U03 | different | The first clause copies the assignments. The second adds a change property: when the inputs differ, each output differs from the input originally occupying that position. |
| U04 | different | As in U03, the conditional inequalities compare the outputs with their original positions, adding a relation beyond the copied assignments. |
| U05 | different | The body successively updates a candidate minimum. The contract instead characterizes the answer through lower bounds and membership among the inputs, without reproducing those updates. |
| U06 | different | The zero-divisor case repeats the body, but the other case specifies the quotient–remainder identity, remainder bounds, and nonnegative quotient, rather than copying `%` and `/`. |
| U07 | different | The contract characterizes the maximum as at least every input and equal to one of them. It does not reproduce the candidate-update algorithm. |
| U08 | different | The body selects through a comparison. The contract characterizes the result as one of the inputs and no greater than either, rather than specifying the branch outcomes. |
| U09 | different | The actual C body directly assigns the swapped values. The additional clause states that unequal inputs cause both positions to change, as in U03. |
| U10 | restates | The postcondition contains exactly the returned expression: `colors[0] * 10 + colors[1]`. |
| U11 | different | `x + result == 0` treated as an inverse arithmetic characterization of the negative case, rather than a copy of `return -x`. A close call, discussed below. |
| U12 | restates | Both body and contract use the exact test `n % 11 == 0` and associate its two outcomes with 1 and 0. The C contract does not use the upstream existential characterization of divisibility. |
| U13 | different | The contract characterizes the answer through allowed values, divisibility by the returned value, and absence of smaller candidate factors. In particular, `n % result == 0` states a relation involving the selected result rather than copying a particular branch. |
| U14 | restates | The two clauses are the implications "equal inputs imply 1" and "unequal inputs imply 0". These reproduce the body's cases exactly. |
| U15 | restates | The contract repeats the body's remainder test and its corresponding Boolean outputs. Writing the cases as a disjunction does not add a different characterization. |
| U16 | different | Despite the function's name, the shown body uses direct assignments. The additional conditional inequalities state the same change property as U03, U04, and U09. |
| U17 | different | The body increments a counter. The contract characterizes the final answer by two bounds identifying the integer square root. This follows the distinction illustrated by the worked `half` example. |
| U18 | different | The body accumulates successive integers. The contract gives a closed-form equation for the final sum, rather than describing that accumulation. |
| U19 | restates | Each clause translates a body branch into an implication: return `x` when `x <= y`; otherwise return `y`. |
| U20 | restates | `result == a * b` directly copies `return a * b`. |
| U21 | different | The contract uses division and exact divisibility to characterize tripling. It reproduces neither the special zero branch nor the expression `x + 2 * x`. |
| U22 | restates | The Boolean formula read as a compressed version of the body's same divisibility cases and outcomes. Moving the divisible-by-400 case outside the divisible-by-4 branch preserves those cases because divisibility by 400 implies divisibility by 4. |
| U23 | different | The first equality copies an assignment, but the second expresses a relation between the two outputs, `out[1] == 2 * out[0]`, where the body computes `out[1]` directly as `4 * x`. |
| U24 | different | The body multiplies by three; the contract checks the answer by dividing it by three and requiring exact reconstruction. |
| U25 | different | The shown C body and contract are identical to U24, so the judgment is identical. The upstream description's mention of branches does not affect this comparison. |
| U26 | restates | The three clauses reproduce the body's invalid-position test, attack test, and fallback case, with exactly the corresponding return constants. The implication syntax changes the presentation. |
| U27 | restates | The contract repeats the exact opposite-sign predicate and maps its truth or falsity to the same 1 or 0 returned by the body. |
| U28 | different | The body adds fourth powers of successive odd numbers. The postcondition characterizes that accumulation through a closed-form polynomial equation. Its appearance in an invariant does not affect the judgment because invariants are excluded. |
| U29 | restates | The complete arithmetic expression in the postcondition is exactly the expression returned by the body. Its mathematical interpretation as a sum does not change that textual relationship. |
| U30 | restates | The postcondition directly copies the returned formula `6 * size * size`. |
| U31 | restates | The postcondition directly copies the same array access, `arr[k - 1]`. The upstream Lean membership clause is not present in the C contract being judged. |
| U32 | different | The first equality copies the sum assignment. `out[1] + y == x` treated as an inverse check of the subtraction, expressed by adding `y` back to the output. Another close call. |

## The two close calls

U11 and U32 are the author's least certain judgments. He read "inverse operation" as covering their arithmetic
relations. However, `x + result == 0` can be rearranged into `result == -x`, and `out[1] + y == x` into
`out[1] == x - y`. If "trivial rewriting" includes those algebraic rearrangements, both would reasonably be
`restates`.

## Sensitivity (computed by the assistant from the same files; the answers stay as given)

If both close calls were read as `restates`: agreement stays at 27 of 32 (U11 would then agree with the first
reading, U32 would stop agreeing), kappa 0.69, and the Verina count of restating contracts by the author's reading
would be 11 instead of 9. The reported range, 9 to 14 of 29, covers both.
