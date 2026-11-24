#include "pfc.h"

long zilu36(long x, long y, long steps)
{
    REQUIRES(x == y && y == 0 && 0 <= steps);
    long step = 0;
    while (step < steps) {
        INVARIANT(x == y && x >= 0);
        x = x + 1;
        y = y + 1;
        step = step + 1;
    }
    ASSERT(x == y && x >= 0);
    return x;
}
