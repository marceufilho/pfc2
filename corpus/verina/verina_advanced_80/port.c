#include "pfc.h"

/* Verina verina_advanced_80: indices i < j of the two numbers that add up to target, in out[0], out[1]. */
long twoSum(long nums_len, const long nums[nums_len], long target, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
    requires(nums_len >= 2)
    requires(separated(out, nums))
    ensures(result == 2 || result == 0)
    ensures(result != 2 || (0 <= out[0] && out[0] < out[1] && out[1] < nums_len && nums[out[0]] + nums[out[1]] == target))
{
    for (long i = 0; i < nums_len; i++) invariant(0 <= i && i <= nums_len) {
        for (long j = i + 1; j < nums_len; j++) invariant(i + 1 <= j && j <= nums_len) {
            if (nums[i] + nums[j] == target) {
                out[0] = i;
                out[1] = j;
                return 2;
            }
        }
    }
    return 0;
}
