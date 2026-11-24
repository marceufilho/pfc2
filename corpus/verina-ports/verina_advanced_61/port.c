#include "pfc.h"

/* Verina verina_advanced_61: out[i] is the product of every element of nums except nums[i], without division;
 * returns the length. */
long productExceptSelf(long nums_len, const long nums[nums_len], long out_cap, long out[out_cap])
    requires(out_cap >= nums_len)
{
    long prefix = 1;
    long suffix = 1;

    for (long i = 0; i < nums_len; i++) {
        out[i] = prefix;
        prefix *= nums[i];
    }
    for (long i = nums_len - 1; i >= 0; i--) {
        out[i] *= suffix;
        suffix *= nums[i];
    }
    return nums_len;
}
