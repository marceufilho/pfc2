#include "pfc.h"

long zilu18(long i, long k, long n)
{
    REQUIRES(i == 0 && k == 0 && n > 0);
    while (i < n) {
        INVARIANT(i == k && i <= n);
        i = i + 1;
        k = k + 1;
    }
    ASSERT(i == k && k == n);
    return k;
}
