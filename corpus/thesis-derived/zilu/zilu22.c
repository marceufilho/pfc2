#include "pfc.h"

long zilu22(long x, long y, long steps)
{
    REQUIRES(x == 1 && y == 0 && 0 <= steps);
    long step = 0;
    while (step < steps) {
        INVARIANT(x >= y && y >= 0 && x >= 1);
        x = x + y;
        y = y + 1;
        step = step + 1;
    }
    ASSERT(x >= y);
    return x;
}
