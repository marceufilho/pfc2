#include "pfc.h"

long zilu29(long x, long y)
{
    REQUIRES(x < y);
    while (x < y) {
        INVARIANT(x <= y + 99);
        x = x + 100;
    }
    ASSERT(x >= y && x <= y + 99);
    return x;
}
