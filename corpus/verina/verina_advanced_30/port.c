#include "pfc.h"

/* Verina verina_advanced_30: length of the longest strictly increasing contiguous run; 0 for an empty list. */
long longestIncreasingStreak(long nums_len, const long nums[nums_len])
    requires(nums_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= nums_len */
    /* Case 1 (nums = [] -> result = 0) is stated. Cases 2 and 3 quantify over streak positions: dropped. */
    ensures(nums_len != 0 || result == 0)
    ensures(0 <= result && result <= nums_len)
{
    if (nums_len == 0) {
        return 0;
    }
    long best = 1;
    long current = 1;

    for (long i = 1; i < nums_len; i++) invariant(1 <= current && current <= i && 1 <= best && best <= i) {
        if (nums[i] > nums[i - 1]) {
            current++;
        } else {
            current = 1;
        }
        if (current > best) {
            best = current;
        }
    }
    return best;
}
