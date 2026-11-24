#include "pfc.h"

long zilupair04(long x, long y, long t, long steps, long j2, long k2, long n2)
{
    REQUIRES(x != y && y == t && 0 <= steps && j2 == 0 && k2 == n2 && n2 > 0);
    long step = 0;
    while (step < steps) {
        INVARIANT(y >= t);
        if (x > 0) {
            y = y + x;
        }
        step = step + 1;
    }
    ASSERT(y >= t);
    while (j2 < n2 && n2 > 0) {
        INVARIANT(j2 + k2 == n2 && j2 <= n2);
        j2 = j2 + 1;
        k2 = k2 - 1;
    }
    ASSERT(k2 == 0);
    return y;
}
