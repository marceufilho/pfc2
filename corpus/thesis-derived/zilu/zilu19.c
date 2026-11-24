#include "pfc.h"

long zilu19(long j, long k, long n)
{
    REQUIRES(j == n && k == n && n > 0);
    while (j > 0 && n > 0) {
        INVARIANT(j == k && j >= 0);
        j = j - 1;
        k = k - 1;
    }
    ASSERT(k == 0);
    return k;
}
