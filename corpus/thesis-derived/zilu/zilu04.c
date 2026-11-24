#include "pfc.h"

long zilu04(long k, long j, long n)
{
    REQUIRES(n >= 1 && k >= n && j == 0);
    while (j <= n - 1) {
        INVARIANT(k + j >= n && j <= n);
        j = j + 1;
        k = k - 1;
    }
    ASSERT(k >= 0);
    return k;
}
