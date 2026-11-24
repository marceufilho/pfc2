#include "pfc.h"

long zilu30(long x, long y, long steps)
{
    REQUIRES(y == x && 0 <= steps);
    long step = 0;
    while (step < steps) {
        INVARIANT(x == y);
        x = x + 1;
        y = y + 1;
        step = step + 1;
    }
    ASSERT(x == y);
    return x;
}
