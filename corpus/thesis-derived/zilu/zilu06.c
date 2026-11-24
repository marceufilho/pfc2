#include "pfc.h"

long zilu06(long i, long x, long y, long k, long steps)
{
    REQUIRES(x + y == k && 0 <= steps);
    long j = 0;
    long step = 0;
    while (step < steps) {
        INVARIANT(x + y == k);
        if (j == i) {
            x = x + 1;
            y = y - 1;
        } else {
            y = y + 1;
            x = x - 1;
        }
        j = j + 1;
        step = step + 1;
    }
    ASSERT(x + y == k);
    return x;
}
