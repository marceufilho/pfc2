#include "pfc.h"

long zilupair11(long i, long x2, long y2, long steps2)
{
    REQUIRES(i >= 0 && i <= 200 && x2 == y2 && y2 == 0 && 0 <= steps2);
    long step2 = 0;
    while (i > 0) {
        INVARIANT(i >= 0);
        i = i - 1;
    }
    ASSERT(i >= 0);
    while (step2 < steps2) {
        INVARIANT(x2 == y2 && x2 >= 0);
        x2 = x2 + 1;
        y2 = y2 + 1;
        step2 = step2 + 1;
    }
    ASSERT(x2 == y2 && x2 >= 0);
    return i;
}
