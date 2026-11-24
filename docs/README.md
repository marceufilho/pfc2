# PFC2

PFC2 is a small, proved subset of C. You write ordinary C11 with a few extra words that state what the code
must do; the checker proves those statements for every input and only then releases C in which the runtime
checks it proved unnecessary are gone.

```c
#include "pfc.h"

long count(long n)
    requires(0 <= n)
    ensures(result == n)
{
    long i = 0;

    while (i < n) {
        i++;
    }
    return i;
}

law counting_to_n_gives_n(long n where(0 <= n))
{
    assert(count(n) == n);
}
```

```console
$ pfc2 check examples/01_count/count.c
count.c: certified (full)
  law counting_to_n_gives_n(long n where(0 <= n)) { assert(count(n) == n); }
  proof count: loop at line 11 invariant ((0 <= i) && (i <= n)) (inferred)
  obligations proved: 6 of 6 (Z3 5.3.3.0)
```

The same file is valid C for any compiler: `pfc.h` erases the extra words.

## Status

PFC2 is a research prototype. It grew out of PFC, the compiler of a thesis, and it is **not** the compiler that
thesis evaluated: none of those results describe PFC2 ([PFC and PFC2](10-pfc-and-pfc2.md)). What PFC2's own tests
cover and what they do not is in [Limits](09-limits.md).

## Read in this order

| Page | What it answers |
| --- | --- |
| [1. Tour](01-tour.md) | Ten minutes from an empty file to a certified program |
| [2. Language](02-language.md) | Every construct that is accepted, and every word PFC2 adds |
| [3. Proofs](03-proofs.md) | What is proved, the two levels, inferred bounds, termination, proof files |
| [4. Programs](04-programs.md) | Globals, strings, console I/O, `main`, and what stays unverified |
| [5. Commands](05-commands.md) | `check`, `build`, `run`, `replay`, `elaborate`, `lsp` and their options |
| [6. Examples](06-examples.md) | The example programs, the wrong ones included |
| [7. Design](07-design.md) | Why the language looks like this and what is trusted |
| [8. Implementation](08-implementation.md) | The pipeline, the modules, how to add a feature |
| [9. Limits](09-limits.md) | What PFC2 does not do and does not claim |
| [10. PFC and PFC2](10-pfc-and-pfc2.md) | How PFC2 differs from the thesis compiler it grew from |
| [11. Editor](11-editor.md) | Proofs as you type: the language server and the VS Code extension |

## Requirements

Python 3.11 or 3.12, [uv](https://docs.astral.sh/uv/) and `clang-19` (or another clang selected with `--clang`).
No external preprocessor is used.

```console
$ uv sync
$ uv run pfc2 --help
$ uv run pfc2 check examples/01_count/count.c
```
