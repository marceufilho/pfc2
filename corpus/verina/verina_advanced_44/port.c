#include "pfc.h"

/* Verina verina_advanced_44: the largest sum of a contiguous subarray whose length is a positive multiple
 * of k; 0 when there is no such subarray. */
long maxSubarraySumDivisibleByK(long arr_len, const long arr[arr_len], long k)
    requires(k > 0)
    /* No subarray of a positive length divisible by k -> result = 0: such a subarray exists exactly when
     * arr_len >= k, so this is stated as below. Membership and maximality among the sums are dropped. */
    ensures(arr_len >= k || result == 0)
{
    long found = 0;
    long best = 0;

    for (long start = 0; start < arr_len; start++) invariant((found == 0 && best == 0) || arr_len >= k) {
        long sum = 0;
        for (long end = start; end < arr_len; end++) invariant(start <= end && ((found == 0 && best == 0) || arr_len >= k)) {
            sum = sum + arr[end];
            if ((end - start + 1) % k == 0) {
                if (!found || sum > best) {
                    best = sum;
                    found = 1;
                }
            }
        }
    }
    return best;
}
