#include "pfc.h"

/* Verina verina_advanced_29: length of the longest contiguous subarray in which no value occurs more than
 * k times. */
long longestGoodSubarray(long nums_len, const long nums[nums_len], long k)
{
    long best = 0;

    for (long start = 0; start < nums_len; start++) {
        for (long end = start; end < nums_len; end++) {
            long count = 0;
            for (long i = start; i <= end; i++) {
                if (nums[i] == nums[end]) {
                    count++;
                }
            }
            if (count > k) {
                break;
            }
            if (end - start + 1 > best) {
                best = end - start + 1;
            }
        }
    }
    return best;
}
