#include "pfc.h"

long zilu33(long x)
{
    REQUIRES(x >= 0);
    while (x < 100 && x >= 0) {
        INVARIANT(x >= 0);
        x = x + 1;
    }
    ASSERT(x >= 100);
    return x;
}
