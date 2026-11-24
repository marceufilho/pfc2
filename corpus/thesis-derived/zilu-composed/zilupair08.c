#include "pfc.h"

long zilupair08(long x, long i2, long x2, long y2, long k2, long steps2)
{
    REQUIRES(x < 0 && x2 + y2 == k2 && 0 <= steps2);
    long j2 = 0;
    long step2 = 0;
    while (x < 10) {
        INVARIANT(x <= 10);
        x = x + 1;
    }
    ASSERT(x == 10);
    while (step2 < steps2) {
        INVARIANT(x2 + y2 == k2);
        if (j2 == i2) {
            x2 = x2 + 1;
            y2 = y2 - 1;
        } else {
            y2 = y2 + 1;
            x2 = x2 - 1;
        }
        j2 = j2 + 1;
        step2 = step2 + 1;
    }
    ASSERT(x2 + y2 == k2);
    return x;
}
