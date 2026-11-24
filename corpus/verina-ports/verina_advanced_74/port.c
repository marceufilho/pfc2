#include "pfc.h"

/* Verina verina_advanced_74: sum, over all subarrays, of the square of the number of distinct elements. */
long solution(long nums_len, const long nums[nums_len])
{
    long total = 0;

    for (long i = 0; i < nums_len; i++) {
        long distinct = 0;

        for (long j = i; j < nums_len; j++) {
            long seen = 0;

            for (long t = i; t < j; t++) {
                if (nums[t] == nums[j]) {
                    seen = 1;
                    break;
                }
            }
            if (!seen) {
                distinct++;
            }
            total += distinct * distinct;
        }
    }
    return total;
}
