#include "pfc.h"

long zilu24(long i, long k, long n)
{
    REQUIRES(i == 0 && k == n && n >= 0);
    while (i < n) {
        INVARIANT(2 * k + i == 2 * n && i <= n + 1);
        k = k - 1;
        i = i + 2;
    }
    ASSERT(2 * k >= n - 1);
    return k;
}
