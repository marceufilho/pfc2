---
title: "4. Programs"
sidebar:
  order: 4
source: docs/04-programs.md
source_sha256: 67f735f149e6135e5f3ab65bc82fcfc06a38c9dff0bc34ccd39670b117fc6c43
---

Everything needed for a small console program: state, text, input, output and an entry point.

## Globals

```c
long hits = 0;
long limit = 100;

long hit(void)
    requires(0 <= hits)
    ensures(0 <= hits)
    ensures(result == hits)
{
    if (hits < limit) {
        hits++;
    }
    return hits;
}
```

A global is a `long` or `_Bool` at file scope with a literal initial value.

- Inside a function a global may hold any value its type allows, unless a `requires` says more. Only `main` may
  rely on the initial values, because nothing has run before it.
- In `ensures`, a global means its value when the function returns.
- After a call, the caller forgets what it knew about the globals the callee **may write** (directly or through
  its own callees) and learns only what the callee's `ensures` says. Globals the callee does not write are
  untouched:

  ```c
  long before = limit;
  hit();
  assert(limit == before);     /* proved: hit never assigns limit */
  ```
- The emitted C declares globals `static`, so no other translation unit can change them behind the proof.

There is no way yet to mention the value a global had on entry (`old(hits)`), so "`hit` adds one" cannot be
stated; see [Limits](../09-limits/).

## Functions implemented elsewhere

```c
long sensor(void)
    ensures(0 <= result && result <= 100);

long use(void)
    ensures(result <= 200)
{
    return sensor() + sensor();
}
```

A declaration without a definition is an *external* function. Its contract is taken on trust: callers must
prove its `requires` and may assume its `ensures`. PFC2 does not see its body, so the proof file lists it under
`unverified.functions`.

Because the contract is trusted, PFC2 first checks that it is possible. A contract nothing can satisfy
(`ensures(result < 0 && result > 100)`) would let anything after the call be proved, so the file is refused. So is
a contract that promises a result some allowed input cannot have (`ensures(result + result == x)` has no answer
for an odd `x`), and the refusal names such an input. Array contents are part of the question: the function may
choose the cells of the arrays it receives without `const`, and nothing else, so `ensures(result == a[0] &&
a[0] > 0)` on a `const` array is refused (the caller's array may hold a negative value). If the solver cannot
decide the question the file is refused too.

This rules out impossible contracts. It cannot tell whether the real function behaves as its contract says: that
is still the one place where a certified program can be wrong, so keep such contracts small.

An external function may write the arrays it receives (unless `const`). It cannot write the program's globals,
which are `static`. PFC2 also assumes it does not call back into the functions of this file: such a call could
change a global behind the caller's back, and nothing in one file can check it.

## Strings and the console

```c
#include "pfc.h"
#include "pfc_rt.h"
```

`pfc_rt.h` declares the console runtime as external functions:

| Function | Effect | Returns |
| --- | --- | --- |
| `print_int(n)` | writes `n` | 0 |
| `print_str(s)`, `println_str(s)` | writes `s`, the second with a newline | 0 |
| `println()` | writes a newline | 0 |
| `read_int()` | reads a line as a decimal integer | the value; 0 if the line is not an integer |
| `read_line()` | reads a line without its newline | a `string` |
| `str_eq(a, b)` | compares characters | 1 or 0 |

`string` is the type of text. A string can be a literal, a variable, a parameter or a result; it can be printed
and compared with `str_eq`. The proofs treat it as an opaque value: nothing is known or proved about its
characters or its length. (`==` on two strings compares identity, not characters, as in C.)

C has no overloading, so there is one function per kind of value: `print_int(42)`, `print_str("answer")`.

What the checker knows about input is exactly the contract: `read_int()` may return any `long`. A program that
needs a range tests it, as the calculator does, and the proof then covers every value that passes the test.

## `main`

```c
int main(void)
{
    ...
    return 0;
}
```

`main` is checked like any function. It is the only function declared `int`; internally it is `pfc2_main`
returning `long`, and the release adds the C entry point that calls it.

## What the released C contains

```console
$ pfc2 build examples/10_greeter/greeter.c
```

writes the emitted functions followed by a short, fixed tail:

```c
/* PFC2 boundary (not part of the proof): string constants and the program entry. */
long pfc2_str_1(void) { return (long)"hello, "; }
long pfc2_str_2(void) { return (long)"your name? "; }
long pfc2_str_3(void) { return (long)""; }
long pfc2_str_4(void) { return (long)"stranger"; }
int main(void) { return (int)pfc2_main(); }
```

A string is carried as a `long` holding its address, which is why PFC2 programs with strings need a target
where `long` and pointers have the same size (the runtime asserts it). These lines and the external functions
are listed in the proof file:

```json
"unverified": {
  "functions": ["print_int", "print_str", "println", "println_str", "read_int", "read_line", "str_eq"],
  "lines": ["long pfc2_str_1(void) { return (long)\"hello, \"; }", "...", "int main(void) { return (int)pfc2_main(); }"]
}
```

## Running

```console
$ pfc2 run examples/10_greeter/greeter.c
your name? Ada
hello, Ada
hello, Ada
```

`run` certifies the program, compiles the released C together with `pfc2/runtime/pfc_rt.c` using the selected
clang and `-std=c11 -O2 -Wall -Wextra -Werror -Wno-self-assign -Wno-tautological-compare`, and executes it; `--stdin FILE` supplies the input. A refused
program is not run. To build by hand:

```console
$ pfc2 build examples/10_greeter/greeter.c --output build/pfc2/greeter
$ clang-19 -std=c11 -O2 -Wall -Wextra -Werror build/pfc2/greeter/greeter.c pfc2/runtime/pfc_rt.c -o greeter
```

The source also compiles directly, without PFC2, against the same runtime:

```console
$ clang-19 -std=c11 -O2 -Wall -Wextra -Werror -Ipfc2/include -Iinclude \
    examples/10_greeter/greeter.c pfc2/runtime/pfc_rt.c -o greeter-plain
```

The tests run both binaries on the same input and require the same output.

## What is and is not verified

| Verified | Not verified |
| --- | --- |
| every function defined in the file, `main` included | `pfc2/runtime/pfc_rt.c` |
| every array index, division, call and (at `full`) arithmetic operation | the contracts of external functions |
| every contract, assertion and law | the boundary lines above |
| termination of loops that have `decreases` | termination of other loops; anything about string contents |
