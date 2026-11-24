#include "pfc.h"

long zilu05(long x, long y, long n)
{
    REQUIRES(x >= 0 && x <= y && y < n);
    while (x < n) {
        INVARIANT(x <= y && y <= n);
        x = x + 1;
        if (x > y) {
            y = y + 1;
        }
    }
    ASSERT(y == n);
    return y;
}
