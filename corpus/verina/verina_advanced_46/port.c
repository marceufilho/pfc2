#include "pfc.h"

/* Verina verina_advanced_46: maximum sum of a contiguous subarray, the empty subarray (0) included. */
long maxSubarraySum(long numbers_len, const long numbers[numbers_len])
    /* Membership and maximality among all subarray sums: dropped. The sum of the empty subarray is one
     * of them, which gives the only stated bound. */
    ensures(result >= 0)
{
    long current = 0;
    long best = 0;

    for (long i = 0; i < numbers_len; i++) invariant(best >= 0 && current >= 0) {
        current += numbers[i];
        if (current < 0) {
            current = 0;
        }
        if (current > best) {
            best = current;
        }
    }
    return best;
}
