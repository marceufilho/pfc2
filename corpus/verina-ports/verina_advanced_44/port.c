#include "pfc.h"

/* Verina verina_advanced_44: the largest sum of a contiguous subarray whose length is a positive multiple
 * of k; 0 when there is no such subarray. */
long maxSubarraySumDivisibleByK(long arr_len, const long arr[arr_len], long k)
    requires(k > 0)
{
    long found = 0;
    long best = 0;

    for (long start = 0; start < arr_len; start++) {
        long sum = 0;
        for (long end = start; end < arr_len; end++) {
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
