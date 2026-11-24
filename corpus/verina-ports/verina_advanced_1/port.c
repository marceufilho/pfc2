#include "pfc.h"

/* Verina verina_advanced_1: the element that appears exactly once when every other appears twice. */
long FindSingleNumber(long nums_len, const long nums[nums_len])
{
    for (long i = 0; i < nums_len; i++) {
        long count = 0;
        for (long j = 0; j < nums_len; j++) {
            if (nums[j] == nums[i]) {
                count++;
            }
        }
        if (count == 1) {
            return nums[i];
        }
    }
    return 0;
}
