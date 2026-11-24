#include "pfc.h"

/* Verina verina_advanced_69: index of target in a strictly increasing list, or where it would be inserted. */
long searchInsert(long xs_len, const long xs[xs_len], long target)
{
    long low = 0;
    long high = xs_len;

    while (low < high) {
        long mid = low + (high - low) / 2;

        if (xs[mid] < target) {
            low = mid + 1;
        } else {
            high = mid;
        }
    }
    return low;
}
