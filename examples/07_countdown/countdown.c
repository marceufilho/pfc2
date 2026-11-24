#include "pfc.h"

/* decreases(e): e is never negative when the body starts and is smaller when it ends, so the
 * loop cannot run forever. Without it PFC2 proves what the loop computes, not that it stops. */
long countdown(long n)
    requires(0 <= n)
    ensures(result == 0)
{
    long left = n;

    while (left > 0) decreases(left) {
        left--;
    }
    return left;
}

/* For every starting value, the countdown ends at zero. */
law every_countdown_reaches_zero(long n where(0 <= n))
{
    assert(countdown(n) == 0);
}
