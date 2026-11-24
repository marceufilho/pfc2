#include "pfc.h"

/* Verina verina_advanced_74: sum, over all subarrays, of the square of the number of distinct elements. */
long solution(long nums_len, const long nums[nums_len])
    requires(1 <= nums_len && nums_len <= 100)
    ensures(result >= 0)
{
    long total = 0;

    for (long i = 0; i < nums_len; i++) invariant(0 <= i && i <= nums_len && 0 <= total && total <= 1000000 * i) {
        long distinct = 0;

        for (long j = i; j < nums_len; j++) invariant(i <= j && j <= nums_len && 0 <= distinct && distinct <= j - i && 0 <= total && total <= 1000000 * i + 10000 * (j - i)) {
            long seen = 0;

            for (long t = i; t < j; t++) invariant(i <= t && t <= j) {
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
