#include "pfc.h"

long zilu37(long x, long y)
{
    REQUIRES(x == y && x >= 0);
    while (x > 0) {
        INVARIANT(x == y && x >= 0);
        x = x - 1;
        y = y - 1;
    }
    ASSERT(y >= 0);
    return y;
}
