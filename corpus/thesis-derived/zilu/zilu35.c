#include "pfc.h"

long zilu35(long x)
{
    REQUIRES(x >= 0);
    while (x >= 0 && x < 10) {
        INVARIANT(x >= 0);
        x = x + 1;
    }
    ASSERT(x >= 10);
    return x;
}
