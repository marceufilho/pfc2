#include "pfc.h"

/* Verina verina_basic_102: the lexicographically smallest pair i < j with nums[i] + nums[j] == target. */
long twoSum(long nums_len, const long nums[nums_len], long target, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
    requires(nums_len > 1)
{
    for (long i = 0; i < nums_len; i++) invariant(0 <= i && i <= nums_len) {
        for (long j = i + 1; j < nums_len; j++) invariant(i + 1 <= j && j <= nums_len) {
            if (nums[i] + nums[j] == target) {
                out[0] = i;
                out[1] = j;
                return 0;
            }
        }
    }
    return 0;
}
