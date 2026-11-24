#include "pfc.h"

long zilu17(long i, long k, long n)
{
    REQUIRES(i == 0 && k == 0);
    while (i < n) {
        INVARIANT(i == k);
        i = i + 1;
        k = k + 1;
    }
    ASSERT(k >= n);
    return k;
}
