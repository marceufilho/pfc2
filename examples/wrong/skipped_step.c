#include "pfc.h"

/* Wrong: on the `continue` path the counter stays behind, so `seen == i` is not kept. */
long evens(long n)
    requires(0 <= n && n <= 1000)
    ensures(result == n)
{
    long seen = 0;

    for (long i = 0; i < n; i++) invariant(seen == i) {
        if (i % 2 == 1) {
            continue;
        }
        seen++;
    }
    return seen;
}
