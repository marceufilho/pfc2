#include "pfc.h"

long zilu25(long x)
{
    REQUIRES(x < 0);
    while (x < 10) {
        INVARIANT(x <= 10);
        x = x + 1;
    }
    ASSERT(x == 10);
    return x;
}
