---
title: "1. Tour"
sidebar:
  order: 1
source: docs/01-tour.md
source_sha256: 38b1d497142d600d4a573fdd934ba8c9a6cb9e60a0729bd938a1fdf12d118587
---

All commands run from the repository root. `pfc2` below stands for `uv run pfc2`.

## A function and its contract

<!-- check: full -->
```c
#include "pfc.h"

long fill(long n, long a[n], long value)
{
    for (long i = 0; i < n; i++) {
        a[i] = value;
    }
    return n;
}
```

`long a[n]` says the array has `n` elements. That is all the checker needs here:

```console
$ pfc2 build examples/02_fill/fill.c --output build/pfc2/fill
fill.c: certified (full)
  proof fill: loop at line 7 invariant ((0 <= i) && (i <= n)) (inferred)
  obligations proved: 4 of 4 (Z3 5.3.3.0)
  bounds/division checks removed: 1 of 1
  overflow checks removed: 1 of 1
  entry checks kept for unverified callers: 1
  loops proved to terminate: 0 of 1
  wrote build/pfc2/fill/fill.c
  wrote build/pfc2/fill/fill.proof.json
```

Reading the report:

- **inferred**: you wrote no loop invariant. PFC2 proposed `0 <= i` and `i <= n` from the shape of the loop and
  kept them because the checker proved them.
- **bounds/division checks removed: 1 of 1**: the write `a[i] = value` is proved inside the array, so the emitted
  C has no bounds check. Each removal cites the proof:

  ```c
  // proved: obligation bounds:b7230da2…
  a[i] = value;
  ```
- **overflow checks removed: 1 of 1**: `i++` is proved not to overflow.
- **entry checks kept: 1**: an array of `n` elements means `0 <= n`. Code that PFC2 did not check may still call
  `fill`, so that one comparison stays at the top of the function and traps if a caller breaks it.
- **loops proved to terminate: 0 of 1**: nothing was claimed about termination. See [decreases](../03-proofs/#termination).

`fill.proof.json` records every obligation and can be recomputed offline:

```console
$ pfc2 replay build/pfc2/fill/fill.proof.json
build/pfc2/fill/fill.proof.json: reproduced (certified, level full, 0 network requests)
```

## A mistake

Change `i < n` to `i <= n`:

<!-- check: refused -->
```c
#include "pfc.h"

long fill(long n, long a[n], long value)
{
    for (long i = 0; i <= n; i++) {
        a[i] = value;
    }
    return n;
}
```

```console
$ pfc2 check examples/wrong/off_by_one.c
off_by_one.c: not certified (full): 2 obligation(s) not proved
  off_by_one.c:7:9: this index may be outside the array [failed]
      cannot prove: ((0 <= i) && (i < n))
      for example:  n = 0, value = 0, i = 0
```

The checker names the line, the formula it could not prove and a state in which it is false: with `n = 0` the
loop still runs once and writes `a[0]`. A refused file releases no C.

## Stating what a function does

`requires` is what callers must guarantee, `ensures` what the function guarantees back, and `result` is the
returned value:

<!-- check: full -->
```c
#include "pfc.h"

long bounded_sum(long n, long step)
    requires(0 <= n && n <= 1000)
    requires(0 <= step && step <= 1000)
    ensures(result == n * step)
{
    long total = 0;

    for (long i = 0; i < n; i++) invariant(total == i * step) {
        total += step;
    }
    return total;
}
```

The counter bounds are inferred; the relation between `total` and `i` is not something PFC2 can guess, so it is
written as an `invariant` between the loop head and its `{`.

## Laws

A law is a property proved for every input: here, for every `n` from 0 up. It is never run and never emitted.
Unlike a test, it does not pick cases ([Laws are not tests](../06-examples/#laws-are-not-tests)):

```c
law counting_to_n_gives_n(long n where(0 <= n))
{
    assert(count(n) == n);
}
```

A false law is refused with the value that contradicts it:

```console
$ pfc2 check examples/wrong/false_law.c
  false_law.c:18:5: this assertion may not hold here [failed]
      cannot prove: (result == (n + 1))
      for example:  n = 0, result = 0
```

## When a proof is out of reach

Summing arbitrary elements can overflow, and no contract here says otherwise:

<!-- check: memory -->
```c
#include "pfc.h"

long sum(long n, const long a[n])
{
    long s = 0;

    for (long i = 0; i < n; i++) {
        s += a[i];
    }
    return s;
}
```

```console
$ pfc2 check examples/03_sum/sum.c
sum.c: not certified (full): 1 obligation(s) not proved
  sum.c:10:9: this arithmetic may overflow [failed]
      for example:  n = 1, s = -9223372036854775808, i = 0, base_a = 0, a[0] = -1
  hint: --level memory certifies memory safety and keeps the overflow traps listed above

$ pfc2 check examples/03_sum/sum.c --level memory
sum.c: certified (memory)
  bounds/division checks removed: 1 of 1
  overflow checks removed: 1 of 2; 1 overflow trap kept
      kept at sum.c:10:9
```

At `--level memory` every array access is still proved; the one addition that could not be proved keeps a
runtime trap, and the report says where.

## A whole program

<!-- check: full -->
```c
#include "pfc.h"
#include "pfc_rt.h"

long divide(long x, long y)
    requires(y != 0)
    requires(-1000000 <= x && x <= 1000000)
{
    return x / y;
}

int main(void)
{
    println_str("two numbers, one per line:");
    long a = read_int();
    long b = read_int();

    if (a < -1000000 || a > 1000000 || b < -1000000 || b > 1000000) {
        println_str("too large");
        return 1;
    }
    print_str("sum ");
    print_int(a + b);
    println();
    if (b != 0) {
        print_str("quotient ");
        print_int(divide(a, b));
        println();
    }
    return 0;
}
```

```console
$ pfc2 run examples/09_calculator/calculator.c --stdin examples/09_calculator/stdin.txt
two numbers, one per line:
sum 17
product 60
quotient 2
```

`run` proves the program, compiles the certified C with the console runtime and executes it. The proof covers
every value `read_int` can return; the runtime itself is ordinary C and is listed as unverified
([Programs](../04-programs/)).

Next: [the language](../02-language/).
