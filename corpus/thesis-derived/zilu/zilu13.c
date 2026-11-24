#include "pfc.h"

long zilu13(long i, long j, long k)
{
    REQUIRES(i == 0 && j == 0);
    while (i <= k) {
        INVARIANT(i == j);
        i = i + 1;
        j = j + 1;
    }
    ASSERT(j == i);
    return j;
}
