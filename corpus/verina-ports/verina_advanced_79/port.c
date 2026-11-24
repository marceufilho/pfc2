#include "pfc.h"

/* Verina verina_advanced_79: the lexicographically first pair i < j with nums[i] + nums[j] == target, as
 * out[0] = 1, out[1] = i, out[2] = j; out[0] = 0 when there is none. */
long twoSum(long nums_len, const long nums[nums_len], long target, long out_cap, long out[out_cap])
    requires(out_cap >= 3)
{
    for (long i = 0; i < nums_len; i++) {
        for (long j = i + 1; j < nums_len; j++) {
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
