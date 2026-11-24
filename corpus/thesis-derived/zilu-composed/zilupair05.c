#include "pfc.h"

long zilupair05(long x, long y, long j2, long k2, long n2)
{
    REQUIRES(x == y && x >= 0 && j2 == n2 && k2 == n2 && n2 > 0);
    while (x > 0) {
        INVARIANT(x == y && x >= 0);
        x = x - 1;
        y = y - 1;
    }
    ASSERT(y >= 0);
    while (j2 > 0 && n2 > 0) {
        INVARIANT(j2 == k2 && j2 >= 0);
        j2 = j2 - 1;
        k2 = k2 - 1;
    }
    ASSERT(k2 == 0);
    return y;
}
