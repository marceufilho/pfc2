#include "pfc.h"

/* Verina verina_advanced_37: the element that appears more than half the time (one is assumed to exist), by
 * majority vote. */
long majorityElement(long nums_len, const long nums[nums_len])
{
    long candidate = 0;
    long count = 0;

    for (long i = 0; i < nums_len; i++) {
        if (count == 0) {
            candidate = nums[i];
            count = 1;
        } else if (nums[i] == candidate) {
            count++;
        } else {
            count--;
        }
    }
    return candidate;
}
