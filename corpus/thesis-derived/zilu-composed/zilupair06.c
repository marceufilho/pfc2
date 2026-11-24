#include "pfc.h"

long zilupair06(long x, long y, long x2)
{
    REQUIRES(x < y && x2 >= 0);
    while (x < y) {
        INVARIANT(x <= y);
        x = x + 1;
    }
    ASSERT(x == y);
    while (x2 < 100 && x2 >= 0) {
        INVARIANT(x2 >= 0);
        x2 = x2 + 1;
    }
    ASSERT(x2 >= 100);
    return x;
}
