#include "pfc.h"

long zilu12(long x, long y, long t, long steps)
{
    REQUIRES(x != y && y == t && 0 <= steps);
    long step = 0;
    while (step < steps) {
        INVARIANT(y >= t);
        if (x > 0) {
            y = y + x;
        }
        step = step + 1;
    }
    ASSERT(y >= t);
    return y;
}
