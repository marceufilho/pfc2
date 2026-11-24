#include "pfc.h"

long zilu11(long x, long n)
{
    REQUIRES(x == 0 && n > 0);
    while (x < n) {
        INVARIANT(x <= n);
        x = x + 1;
    }
    ASSERT(x == n);
    return x;
}
