#include "pfc.h"

/* Verina verina_advanced_46: maximum sum of a contiguous subarray, the empty subarray (0) included. */
long maxSubarraySum(long numbers_len, const long numbers[numbers_len])
{
    long current = 0;
    long best = 0;

    for (long i = 0; i < numbers_len; i++) {
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
