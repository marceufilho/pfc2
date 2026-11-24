#include "pfc.h"

/* Verina verina_advanced_79: the lexicographically first pair i < j with nums[i] + nums[j] == target, as
 * out[0] = 1, out[1] = i, out[2] = j; out[0] = 0 when there is none. */
long twoSum(long nums_len, const long nums[nums_len], long target, long out_cap, long out[out_cap])
    requires(out_cap >= 3)
    requires(separated(out, nums))
    ensures(out[0] == 0 || out[0] == 1)
    ensures(out[0] != 1 || (0 <= out[1] && out[1] < out[2] && out[2] < nums_len && nums[out[1]] + nums[out[2]] == target))
{
    for (long i = 0; i < nums_len; i++) invariant(0 <= i && i <= nums_len) {
        for (long j = i + 1; j < nums_len; j++) invariant(i + 1 <= j && j <= nums_len) {
            if (nums[i] + nums[j] == target) {
                out[0] = 1;
                out[1] = i;
                out[2] = j;
                return 0;
            }
        }
    }
    out[0] = 0;
    return 0;
}
