#include "pfc.h"

/* Verina verina_advanced_53: minimum number of right shifts that sort a list of distinct integers, or -1. */
long minimumRightShifts(long nums_len, const long nums[nums_len])
{
    long drops = 0;
    long drop = 0;

    for (long i = 0; i + 1 < nums_len; i++) {
        if (nums[i] > nums[i + 1]) {
            drops++;
            drop = i;
        }
    }
    if (drops == 0) {
        return 0;
    }
    if (drops == 1 && nums[nums_len - 1] < nums[0]) {
        return nums_len - 1 - drop;
    }
    return -1;
}
