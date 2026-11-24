#include "pfc.h"

long zilu26(long x, long y)
{
    REQUIRES(x < y);
    while (x < y) {
        INVARIANT(x <= y);
        x = x + 1;
    }
    ASSERT(x == y);
    return x;
}
