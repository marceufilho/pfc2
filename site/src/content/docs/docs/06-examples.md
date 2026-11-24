---
title: "6. Examples"
sidebar:
  order: 6
source: docs/06-examples.md
source_sha256: 0fc3c1ff444aa2d9e57e70998f9f04c2da303357c280924de3427d2f2084780b
---

All examples live in `examples/`. Their expected verdicts are written by hand in
`examples/examples.json`, and `tests/test_integration.py` checks every one: the verdict, the
number of checks removed, replay of the proof file, and that the certified C and the plain C build of the same
source compile without warnings and, for programs, print the same output.

```console
$ pfc2 check examples/05_binary_search/binary_search.c
binary_search.c: certified (full)
  obligations proved: 25 of 25 (Z3 5.3.3.0)
  bounds/division checks removed: 3 of 3
  overflow checks removed: 3 of 3
  entry checks kept for unverified callers: 2
  loops proved to terminate: 1 of 1
```

## Functions

| File | Shows | Level |
| --- | --- | --- |
| `01_count/count.c` | a contract, a law, loop bounds inferred | full |
| `02_fill/fill.c` | an array that carries its length; a write proved in bounds | full |
| `03_sum/sum.c` | an addition that cannot be proved: one trap kept and listed | memory |
| `04_bounded_sum/bounded_sum.c` | a written invariant that makes the arithmetic provable | full |
| `05_binary_search/binary_search.c` | three proved accesses and a termination measure | full |
| `06_copy/copy.c` | two arrays stated not to overlap | full |
| `07_countdown/countdown.c` | `decreases` | full |
| `08_counter/counter.c` | globals; what a call changes and what it leaves | full |
| `11_flag/flag.c` | a game as a state machine: no sequence of moves reaches the flag | full |
| `12_rest_api/api.c` | the handlers of a REST API: any request, no access outside the table, a law | full |
| `13_progression/progression.c` | an arithmetic progression computed by a loop, and five laws about every term | full |
| `14_tree/tree.c` | a binary tree stored in an array: child and parent indices, six laws that make it one tree | full |
| `16_calendar/calendar.c` | `%`, a table in a local array, a call in a loop; four laws about every year | full |
| `17_text/text.c` | `char` arrays: counting, searching with `break`, changing case with `continue`, a string table | full |
| `15_matrix/matrix.c` | 3 x 3 matrices: the cell layout, proved multiplication accesses, det(AB) = det(A) det(B) | memory |

## Programs

Each has a `stdin.txt` and an `expected.txt`.

| File | Shows |
| --- | --- |
| `09_calculator/calculator.c` | reading numbers, testing their range, proved arithmetic and division |
| `10_greeter/greeter.c` | strings, `read_line`, `str_eq`, a terminating loop that prints |
| `console/minimal.c` | the smallest program |
| `console/arithmetic.c` | a chain of calls over a global; `main` proves the final value from the contracts |
| `console/repeat.c` | a string and a count passed to a function |
| `console/echo.c` | read a line and print it back |

```console
$ pfc2 run examples/09_calculator/calculator.c --stdin examples/09_calculator/stdin.txt
two numbers, one per line:
sum 17
product 60
quotient 2
```

## Laws are not tests

A test runs the program on inputs someone chose and compares the answers. It tells you about those inputs:

```c
assert(term(0, 1, 5) == 5);     /* three cases */
assert(term(2, 3, 4) == 14);
assert(term(7, 0, 9) == 7);
```

A law has parameters, and it is proved for **every** value they can take. Nothing is run:

```c
law consecutive_terms_differ_by_the_step(
    long start where(-1000 <= start && start <= 1000),
    long step where(-1000 <= step && step <= 1000),
    long n where(0 <= n && n < 1000))
{
    assert(term(start, step, n + 1) - term(start, step, n) == step);
}
```

That one law covers about four billion combinations of `start`, `step` and `n`, including the ones nobody would
have thought to test. A law that fixes its inputs (`assert(term(0, 1, 5) == 5)`) is allowed, but it is only a test
written in another place: the laws in the examples all quantify over their inputs, because that is the point.

A law is proved from the **contract** of the functions it calls, not from their bodies. So the usual shape is: the
contract says exactly what the function computes (`ensures(result == start + n * step)`), the checker proves the
body against it once, and each law is then a consequence anyone can read without reading the loop.

### Kinds of law in the examples

| Kind | Says | Example |
| --- | --- | --- |
| Functional | the result equals a formula, for all inputs | `counting_to_n_gives_n` (01), `every_countdown_reaches_zero` (07) |
| Recurrence | how the result changes when an input moves by one | `consecutive_terms_differ_by_the_step` (13), `one_more_step_adds_the_step` (04) |
| Symmetry | two different calls agree | `the_count_and_the_step_can_be_swapped` (04) |
| Algebraic identity | an equation between results | `a_term_is_the_average_of_its_neighbours` (13), `the_determinant_of_a_product_is_the_product_of_the_determinants` (15) |
| Round trip | doing and undoing returns to the start | `the_parent_of_a_left_child_is_the_node` (14), `every_cell_is_a_position` (15), `stepping_back_returns_to_the_start` (13) |
| No collision | different inputs never give the same result | `positions_do_not_collide` (15), `left_children_do_not_collide` (14) |
| Structure | the pieces fit together as one whole | `every_node_is_a_child_of_its_parent` (14), `cells_are_in_row_major_order` (15) |
| Soundness of an answer | whatever is returned is right | `a_found_index_holds_the_key` (05) |
| Safety | something bad never happens, whatever the input | `nobody_ever_wins` (11), `negative_id_is_not_found` (12) |

### What a law cannot say yet

PFC2 has no quantifiers inside a predicate, so a law cannot speak about *every element* of an array at once. That
rules out "the array is sorted", "after `fill`, every element is the value", "`sum` returns the sum of the
elements", and a full statement of matrix multiplication. The examples say so where it applies: binary search
proves that a found index holds the key, not that -1 means absent; `multiply` proves its accesses, not its result.
The matrix example states the 2 x 2 determinant identity on scalars for that reason.

One law the checker refused while these examples were written: `stepping_back_returns_to_the_start` was first
stated for every start up to 1000, and the checker answered with `start = 47, step = 1, n = 960`, a case where the
first result is 1007 and is no longer an input `term` accepts. The law was wrong as stated; a test would have
needed to hit that case by luck.

## Two larger examples

**A game you cannot win** (`11_flag/flag.c`). Capture the flag on an 8 by 5 board with a wall in column 4. The
function `play` runs any list of moves and its contract says the result is always 0: nobody wins. PFC2 proves it
for every list of moves at once. `wrong/flag_without_wall.c` changes one line (the wall column becomes one that
does not exist); the claim is then false and the file is refused. The site has a playable version whose moves
are computed by the compiled program.

**A REST API** (`12_rest_api/`). `api.c` is the logic of the API; `server.py` is an unverified HTTP server that
calls it. The handlers accept any method, id and value, and are proved never to touch memory outside the table.
`wrong/rest_api_missing_check.c` drops one comparison and is refused with the request `id = -1`.
`tests/test_rest_api.py` sends 17 real HTTP requests to the certified code.

```console
$ pfc2 check examples/wrong/rest_api_missing_check.c
rest_api_missing_check.c: not certified (full): 12 obligation(s) not proved
  rest_api_missing_check.c:42:13: this index may be outside the array [failed]
      cannot prove: ((0 <= id) && (id < n))
      for example:  reply = 0, n = 0, method = 0, id = -1, value = 0
```

## Programs that must be refused

`examples/wrong/` holds one mistake per file. Each is refused at the line its comment names, and releases
no C.

| File | Mistake | Refused as |
| --- | --- | --- |
| `off_by_one.c` | `i <= n` writes past the end | index may be outside the array |
| `false_law.c` | a law claims `count(0) == 1` | assertion may not hold; example `result = 0` |
| `no_progress.c` | the loop body does not move the measure | assertion may not hold |
| `forgotten_global.c` | relies on a global after a call that writes it | assertion may not hold |
| `unchecked_division.c` | divides with nothing said about the divisor | division may be by zero or overflow |
| `broken_call.c` | passes a value the callee's contract forbids | call may break the callee's requires |
| `narrow_store.c` | adds 13 to a letter and stores it in a `char` | value may not fit the element; example `s[0] = 115` |
| `skipped_step.c` | `continue` skips the statement that keeps the invariant | an iteration may break the loop invariant; example `i = 1` |
| `contradictory_extern.c` | declares a function whose contract nothing can satisfy | the contract cannot be satisfied |
| `flag_without_wall.c` | the game with its wall removed, still claiming nobody wins | an iteration may break the loop invariant |
| `rest_api_missing_check.c` | the API without the `id < 0` test | index may be outside the array; example `id = -1` |

## Adding an example

1. Write the file under `examples/NN_name/`.
2. Add its line to `examples.json` with the verdict you expect, derived by reading the program, not by copying
   the tool's output.
3. For a program, add `stdin` and `expected` files.
4. Run `uv run pytest -q tests/test_integration.py`.
