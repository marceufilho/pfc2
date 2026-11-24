#include "pfc.h"

long zilupair09(long x, long y, long steps, long x2, long n2)
{
    REQUIRES(y == x && 0 <= steps && x2 == 0 && n2 > 0);
    long step = 0;
    while (step < steps) {
        INVARIANT(x == y);
        x = x + 1;
        y = y + 1;
        step = step + 1;
    }
    ASSERT(x == y);
    while (x2 < n2) {
        INVARIANT(x2 <= n2);
        x2 = x2 + 1;
    }
    ASSERT(x2 == n2);
    return x;
}
