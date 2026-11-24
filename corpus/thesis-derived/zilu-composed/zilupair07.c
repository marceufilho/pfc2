#include "pfc.h"

long zilupair07(long i, long j, long k, long k2, long j2, long n2)
{
    REQUIRES(i < j && k > i - j && n2 >= 1 && k2 >= n2 && j2 == 0);
    while (i < j) {
        INVARIANT(k > i - j);
        k = k + 1;
        i = i + 1;
    }
    ASSERT(k > 0);
    while (j2 <= n2 - 1) {
        INVARIANT(k2 + j2 >= n2 && j2 <= n2);
        j2 = j2 + 1;
        k2 = k2 - 1;
    }
    ASSERT(k2 >= 0);
    return k;
}
