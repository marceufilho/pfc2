#include "pfc.h"

long zilu16(long i, long k, long steps)
{
    REQUIRES(0 <= k && k <= 1 && i == 1 && 0 <= steps);
    long step = 0;
    while (step < steps) {
        INVARIANT(1 <= i + k && i + k <= 2 && i >= 1);
        i = i + 1;
        k = k - 1;
        step = step + 1;
    }
    ASSERT(1 <= i + k && i + k <= 2 && i >= 1);
    return i;
}
