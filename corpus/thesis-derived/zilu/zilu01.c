#include "pfc.h"

long zilu01(long x, long y, long steps)
{
    REQUIRES(x == 1 && y == 1 && 0 <= steps);
    long step = 0;
    while (step < steps) {
        INVARIANT(x >= 1 && y >= 1);
        x = x + y;
        y = x;
        step = step + 1;
    }
    ASSERT(y >= 1);
    return y;
}
