#include "pfc.h"

long zilupair01(long x, long y, long n, long low2, long mid2, long high2)
{
    REQUIRES(x >= 0 && x <= y && y < n && low2 == 0 && mid2 >= 1 && high2 == 2 * mid2);
    while (x < n) {
        INVARIANT(x <= y && y <= n);
        x = x + 1;
        if (x > y) {
            y = y + 1;
        }
    }
    ASSERT(y == n);
    while (mid2 > 0) {
        INVARIANT(high2 == low2 + 2 * mid2 && mid2 >= 0);
        low2 = low2 + 1;
        high2 = high2 - 1;
        mid2 = mid2 - 1;
    }
    ASSERT(low2 == high2);
    return y;
}
