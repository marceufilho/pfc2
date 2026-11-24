#include "pfc.h"

/* Verina verina_advanced_78: indices i < j with nums[i] + nums[j] == target, written to out[0], out[1]. */
long twoSum(long nums_len, const long nums[nums_len], long target, long out_cap, long out[out_cap])
    requires(out_cap >= 2)
{
    for (long i = 0; i < nums_len; i++) {
        for (long j = i + 1; j < nums_len; j++) {
            if (nums[i] + nums[j] == target) {
                out[0] = i;
                out[1] = j;
                return 0;
            }
        }
    }
    return 0;
}
