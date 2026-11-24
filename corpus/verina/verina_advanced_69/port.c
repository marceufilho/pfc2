#include "pfc.h"

/* Verina verina_advanced_69: index of target in a strictly increasing list, or where it would be inserted. */
long searchInsert(long xs_len, const long xs[xs_len], long target)
    requires(0 <= xs_len)
    ensures(0 <= result && result <= xs_len)
    ensures(result >= xs_len || target <= xs[result])
    /* One instance of the dropped "every element before result is smaller": the element just before. */
    ensures(result == 0 || xs[result - 1] < target)
{
    long low = 0;
    long high = xs_len;

    while (low < high) invariant(0 <= low && low <= high && high <= xs_len && (high == xs_len || target <= xs[high]) && (low == 0 || xs[low - 1] < target)) decreases(high - low) {
        long mid = low + (high - low) / 2;

        if (xs[mid] < target) {
            low = mid + 1;
        } else {
            high = mid;
        }
    }
    return low;
}
