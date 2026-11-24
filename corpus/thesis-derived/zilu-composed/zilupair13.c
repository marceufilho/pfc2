#include "pfc.h"

long zilupair13(long i, long j, long k, long n2, long l2)
{
    REQUIRES(i == 0 && j == 0 && l2 > 0);
    long i2 = l2;
    while (i <= k) {
        INVARIANT(i == j);
        i = i + 1;
        j = j + 1;
    }
    ASSERT(j == i);
    while (i2 < n2) {
        INVARIANT(l2 > 0);
        i2 = i2 + 1;
    }
    ASSERT(l2 >= 1);
    return j;
}
