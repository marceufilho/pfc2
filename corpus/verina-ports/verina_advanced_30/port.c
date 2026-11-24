#include "pfc.h"

/* Verina verina_advanced_30: length of the longest strictly increasing contiguous run; 0 for an empty list. */
long longestIncreasingStreak(long nums_len, const long nums[nums_len])
{
    if (nums_len == 0) {
        return 0;
    }
    long best = 1;
    long current = 1;

    for (long i = 1; i < nums_len; i++) {
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
