#include "pfc.h"

long zilu23(long i, long j)
{
    REQUIRES(i == 0 && j == 0);
    while (i < 100) {
        INVARIANT(j == 2 * i && i <= 100);
        j = j + 2;
        i = i + 1;
    }
    ASSERT(j == 200);
    return j;
}
