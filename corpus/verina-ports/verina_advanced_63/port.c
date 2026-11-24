#include "pfc.h"

/* Verina verina_advanced_63: number of distinct elements of a sorted array. */
long removeDuplicates(long nums_len, const long nums[nums_len])
{
    if (nums_len == 0) {
        return 0;
    }
    long k = 1;

    for (long i = 1; i < nums_len; i++) {
        if (nums[i] != nums[i - 1]) {
            k++;
        }
    }
    return k;
}
