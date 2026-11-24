#include "pfc.h"

long zilu34(long j, long k, long n)
{
    REQUIRES(j == 0 && k == n && n > 0);
    while (j < n && n > 0) {
        INVARIANT(j + k == n && j <= n);
        j = j + 1;
        k = k - 1;
    }
    ASSERT(k == 0);
    return k;
}
