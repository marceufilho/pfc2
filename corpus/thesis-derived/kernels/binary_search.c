#include "pfc.h"

long binary_search(const long a[], long a_len, long n, long needle)
{
    REQUIRES(0 <= n && n <= a_len);
    long lo = 0;
    long hi = n - 1;
    while (lo <= hi) {
        INVARIANT(0 <= lo && lo <= hi + 1 && hi < n);
        long mid = lo + (hi - lo) / 2;
        long value = a[mid];
        if (value < needle) {
            lo = mid + 1;
        } else {
            if (needle < value) {
                hi = mid - 1;
            } else {
                return mid;
            }
        }
    }
    return -1;
}
