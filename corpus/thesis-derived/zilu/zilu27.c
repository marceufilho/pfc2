#include "pfc.h"

long zilu27(long i, long j, long k)
{
    REQUIRES(i < j && k > i - j);
    while (i < j) {
        INVARIANT(k > i - j);
        k = k + 1;
        i = i + 1;
    }
    ASSERT(k > 0);
    return k;
}
