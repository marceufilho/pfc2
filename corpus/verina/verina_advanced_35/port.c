#include "pfc.h"

/* Verina verina_advanced_35: the element that appears more than half the time (one is assumed to exist), by
 * majority vote. */
long majorityElement(long nums_len, const long nums[nums_len])
    requires(nums_len > 0)
    /* The rest of the precondition (a majority element exists) and the postcondition are occurrence
     * counts: dropped. */
{
    long candidate = 0;
    long count = 0;

    for (long i = 0; i < nums_len; i++) invariant(0 <= count && count <= i) {
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
