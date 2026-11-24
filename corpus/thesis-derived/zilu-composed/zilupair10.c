#include "pfc.h"

long zilupair10(long i, long k, long steps, long x2, long y2)
{
    REQUIRES(0 <= k && k <= 1 && i == 1 && 0 <= steps && x2 < y2);
    long step = 0;
    while (step < steps) {
        INVARIANT(1 <= i + k && i + k <= 2 && i >= 1);
        i = i + 1;
        k = k - 1;
        step = step + 1;
    }
    ASSERT(1 <= i + k && i + k <= 2 && i >= 1);
    while (x2 < y2) {
        INVARIANT(x2 <= y2 + 99);
        x2 = x2 + 100;
    }
    ASSERT(x2 >= y2 && x2 <= y2 + 99);
    return i;
}
