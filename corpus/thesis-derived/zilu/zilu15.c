#include "pfc.h"

long zilu15(long low, long mid, long high)
{
    REQUIRES(low == 0 && mid >= 1 && high == 2 * mid);
    while (mid > 0) {
        INVARIANT(high == low + 2 * mid && mid >= 0);
        low = low + 1;
        high = high - 1;
        mid = mid - 1;
    }
    ASSERT(low == high);
    return low;
}
