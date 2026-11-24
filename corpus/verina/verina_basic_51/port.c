#include "pfc.h"

/* Verina verina_basic_51: first index of a sorted array whose element is >= key (the array's size when there is none). */
long BinarySearch(long a_len, const long a[a_len], long key)
    requires(a_len >= 0)
    ensures(0 <= result && result <= a_len)
{
    long lo = 0;
    long hi = a_len;

    while (lo < hi) invariant(0 <= lo && lo <= hi && hi <= a_len) decreases(hi - lo) {
        long mid = lo + (hi - lo) / 2;

        if (a[mid] < key) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}
