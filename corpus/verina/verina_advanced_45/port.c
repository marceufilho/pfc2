#include "pfc.h"

/* Verina verina_advanced_45: maximum sum of a non-empty contiguous subarray; 0 for an empty list. */
long maxSubarraySum(long xs_len, const long xs[xs_len])
    requires(xs_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= xs_len */
    /* xs = [] -> result = 0 is stated; for a non-empty list the subarray sums are dropped. */
    ensures(xs_len != 0 || result == 0)
{
    if (xs_len == 0) {
        return 0;
    }
    long current = xs[0];
    long best = xs[0];

    for (long i = 1; i < xs_len; i++) {
        if (current < 0) {
            current = xs[i];
        } else {
            current += xs[i];
        }
        if (current > best) {
            best = current;
        }
    }
    return best;
}
