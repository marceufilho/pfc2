#include "pfc.h"

/* Verina verina_advanced_54: the one number of 0..n missing from a list of n distinct numbers in that range. */
long missingNumber(long nums_len, const long nums[nums_len])
{
    long sum = 0;

    for (long i = 0; i < nums_len; i++) {
        sum += nums[i];
    }
    return nums_len * (nums_len + 1) / 2 - sum;
}
