#include "pfc.h"

long zilupair15(long i, long k, long n, long x2)
{
    REQUIRES(i == 0 && k == 0 && x2 >= 0);
    while (i < n) {
        INVARIANT(i == k);
        i = i + 1;
        k = k + 1;
    }
    ASSERT(k >= n);
    while (x2 >= 0 && x2 < 10) {
        INVARIANT(x2 >= 0);
        x2 = x2 + 1;
    }
    ASSERT(x2 >= 10);
    return k;
}
