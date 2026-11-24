# 2. Language

A PFC2 source file is a C11 translation unit that includes `pfc.h`. Everything on this page is checked by the
compiler: a construct outside it is refused with a rule name and a position, never skipped.

## The C that is accepted

| | Accepted | Not accepted |
| --- | --- | --- |
| Types | `long`, `_Bool`; `int` and `char` as array elements; `string` with `pfc_rt.h` | `int` and `char` variables, unsigned, floats, pointers, structs, typedefs |
| Functions | return `long` or `_Bool`; `int main(void)` | `void` functions, recursion, function pointers, varargs |
| Arrays | parameters: `long a[n]`, `const char s[n]`; locals: `long t[8] = {0};` | local arrays without an initial value or with a variable length, global arrays, arrays of arrays |
| Globals | `long x = 0;`, `_Bool on = 1;` (literal initial value) | `const`, `static`, uninitialised globals |
| Locals | declared with an initial value | uninitialised locals, shadowing |
| Statements | assignment, `if`/`else`, `while`, `for`, `return`, `break`, `continue`, blocks | `goto`, `switch`, `do` |
| Updates | `i++`, `i--`, `++i`, `--i`, `+=`, `-=`, `*=`, `/=`, `%=` as statements | the same inside a larger expression |
| Expressions | `+ - * / %`, comparisons, `&& \|\| !`, unary `-`, indexing, calls | bitwise operators, `?:`, casts, comma |
| Literals | decimal up to 9223372036854775807; `L` suffix; `'a'`, `'\n'` | octal/hex above 32767 (2147483647 with `L`); characters outside 7-bit ASCII |

Functions must be declared or defined before they are called, and every path must end in a `return` with a value.

### Arrays carry their length

```c
long sum(long n, const long a[n]);
```

`a[n]` is real C and tells PFC2 that `a` has `n` elements; `n` must be a `long` parameter of the same function.
Indexing is `a[i]`, and every index is proved to satisfy `0 <= i && i < n`. The declaration also states `0 <= n`:
that is assumed inside the function, proved by every caller and checked at entry in the emitted C. A caller that
passes an array `b` for `a` must prove that the value it passes for `n` is at most the length of `b`.

The older spelling `const long a[], long a_len` is still accepted.

### Local arrays

```c
long buffer[16] = {0};
const long days[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
const char digits[11] = "0123456789";
```

A local array has a literal length (1 to 65536) and an initial value in braces, or a string for a `char`
array. C sets the elements after the listed ones to zero, so no element is ever indeterminate; a declaration
without an initial value is refused. The prover knows the array is a new object that overlaps no other array,
and it knows the initial value of every element of an array of at most 64 elements. For a longer array it knows
only the listed ones.

### Narrow elements

Arrays may hold `char` or `int`; variables, parameters and results stay `long` or `_Bool`.

```c
long digit(long n, const char s[n], long i)
    requires(0 <= i && i < n && '0' <= s[i] && s[i] <= '9')
    ensures(0 <= result && result <= 9)
{
    return s[i] - '0';
}
```

Reading an element gives a value of its type's range, promoted to `int` as in C. Storing into a narrower element
is a conversion that C leaves to the implementation when the value does not fit, so PFC2 requires a proof that
it fits (obligation `conversion`); there is no trap to fall back on. Whether `char` is signed is a property of
the target: PFC2 reads it from clang, proves with that range, and the emitted C asserts it. A character constant
is an `int`, limited to 7-bit characters and the simple escapes.

### `break` and `continue`

Both work as in C, inside `while` and `for`. After `continue` the update of a `for` still runs, and the loop
invariant must hold there. After `break` the code following the loop sees the state at the `break`; the
invariant is not re-checked on that path, because the loop is over. A loop that contains `continue` cannot carry
`decreases` yet.

### Remainder

`a % b` is C's remainder: `(a / b) * b + a % b == a` with `/` truncating toward zero, so the result has the sign
of `a`. Like `/`, it must be proved that `b` is not zero and that the quotient exists.

### Several operators in one expression

`a + b + c`, `x / y / z` and the like are checked operator by operator. In a diagnostic, the second and later
operators of such a chain are reported at the operator itself; a single operator is reported at its left operand.

### Calls

A call may appear anywhere in an expression or as a statement of its own:

```c
long y = f(a) + g(b);
print_int(count(n));
tick();
```

The calls of a statement are evaluated first, left to right, into hidden locals, before its other operands are
read. C leaves the order of operand evaluation unspecified, so this is one of the orders a C compiler may choose,
and it is the order the certified C uses. A call in the index of `a[f()] += 1` or `a[f()]++` runs once, as in C.

An `assert` cannot contain a call (`assert-call`): an ordinary compiler never evaluates an assert, so the checked
program would run a call the source does not. Assign the call to a variable first, or state the property in a
law, where calls are allowed because a law is proved and never emitted. Where C makes evaluation conditional or
repeated, PFC2 refuses to move the call instead of changing the meaning:

```c
if (n > 0 && f(n) > 0) { ... }      /* refused: subset-call-order */
while (f(i) < n) { ... }            /* refused: subset-call-order */
```

Assign the call to a variable first.

### Literals

A decimal literal without a suffix is an `int` when it fits 32 bits and a `long` otherwise, as in C on a target
with a 32-bit `int` and a 64-bit `long`. The checker refuses any other target (`target-literal`) rather than
guess a type.

## The words PFC2 adds

### `requires`, `ensures`, `result`

```c
long divide(long x, long y)
    requires(y != 0)
    requires(-1000000 <= x && x <= 1000000)
    ensures(result == x / y)
{
    return x / y;
}
```

Clauses follow the declarator, before `{`. Several clauses of a kind are allowed. `requires(p)` is assumed inside
the function and proved at every call. `ensures(q)` is proved at every `return` and assumed after every call;
inside it `result` is the returned value. A contract that no input can satisfy (`requires(n < 0 && n > 0)`) is
refused: nothing may be certified vacuously.

A declaration may repeat the clauses of its definition; they must be the same.

### `invariant`, `decreases`

```c
while (lo < hi) invariant(0 <= lo && lo <= hi && hi <= n) decreases(hi - lo) {
    ...
}
```

Both go between the loop head and its `{`; the body must be in braces. An invariant is proved before the loop
(initiation) and after one arbitrary iteration (preservation), and is all the checker knows about the variables
the loop changes. `decreases(e)` proves termination: `e` is never negative when the body starts and is smaller
when it ends. Simple counter bounds need not be written; see [Proofs](03-proofs.md#inferred-loop-bounds).

### `assert`

```c
assert(limit == before);
```

A fact proved where it stands, then available to what follows. It is erased from the emitted C.

### `where`

```c
long clamp(long x where(0 <= x), long hi where(x <= hi))
    ensures(result <= hi)
{
    return x;
}

long i where(0 <= i && i <= n) = 0;        /* inside a function */
```

A refinement type. On a parameter it is a precondition; on a local it is re-proved after every assignment to
the variable (or to anything the predicate mentions) and becomes part of the invariant of every loop that
changes it. The declaration of a typed local stays on one line.

### `separated`

```c
long copy(long n, long dst[n], const long src[n])
    requires(separated(dst, src))
```

The two arrays do not overlap, each taken at its full length. Without it the checker assumes that two arrays of
the same element type may be the same memory.

### `law`

```c
law counting_to_n_gives_n(long n where(0 <= n)) { assert(count(n) == n); }

law fill_returns_its_count(long n, long a[n], long v)
{
    assert(fill(n, a, v) == n);
}
```

A law is written like a function, at file scope, and proved for every value of its parameters; `where` on a
parameter restricts the inputs it speaks about. It is never called (`law-call`) and never emitted. Write `(void)`
for a law without parameters.

A law is proved through the contracts of the functions it calls, so those contracts must say enough: a law
never gives a function a contract.

### Declared functions

```c
long sensor(void)
    ensures(0 <= result && result <= 100);
```

A declaration with no definition in the file describes a function implemented elsewhere. Calls check its
`requires` and assume its `ensures`; the function itself is not verified and is listed in the proof file as an
unverified boundary. See [Programs](04-programs.md#functions-implemented-elsewhere).

## Preprocessor

PFC2 reads its sources itself; no external preprocessor runs. It understands comments, `#include "pfc.h"`,
`#include "pfc_rt.h"`, `#include <stdbool.h>` (for `bool`, `true`, `false`), `#ifdef` / `#ifndef` / `#else` /
`#endif`, and constants:

```c
#define LIMIT 100
```

Macros with parameters, `#if`, other headers and line continuations are refused. A diagnostic gives the line
and column of the source file as you wrote it.

## Reserved names

Names starting with `pfc_`, `pfc2_` or `__spec_`, and `RESULT`. Inside `ensures`, `result` always means the
returned value, so a parameter or global cannot be called `result`. A macro cannot be named like a word of the
language (`long`, `return`, `requires`, ...). The length of `long a[n]` is declared before the array, as C
requires: `long n, long a[n]`.

## For ordinary compilers

`pfc.h` defines every added word away when `PFC_CHECK` is not set (`requires(...)` expands to nothing, a law
becomes an unused static function, `assert` is type-checked and never evaluated). So

```console
$ clang-19 -std=c11 -O2 -Wall -Wextra -Werror -Ipfc2/include -Iinclude -c examples/02_fill/fill.c
```

compiles the same source, and the tests compare that build with the certified one.

## Older spellings

`REQUIRES(p)`, `ENSURES(q)`, `INVARIANT(i)` and `ASSERT(p)` as the first statements of a body, `RESULT`,
`SEPARATED(a, a_len, b, b_len)`, and `where(RESULT == n)` after a declarator are still read. New code should use
the forms above.
