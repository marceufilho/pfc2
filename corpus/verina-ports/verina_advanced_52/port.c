#include "pfc.h"

/* Verina verina_advanced_52: how many elements must be removed from the end of nums until every integer from
 * 1 to k has been collected. */
long minOperations(long nums_len, const long nums[nums_len], long k)
{
    long collected = 0;
    long i = nums_len;

    while (collected < k && i > 0) {
        i--;
        long value = nums[i];

        if (value >= 1 && value <= k) {
            long seen = 0;

            for (long j = i + 1; j < nums_len; j++) {
                if (nums[j] == value) {
                    seen = 1;
                    break;
                }
            }
            if (!seen) {
                collected++;
            }
        }
    }
    return nums_len - i;
}
