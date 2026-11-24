#include "pfc.h"

/* Verina verina_advanced_70: adjacent swaps needed to bring 1 to the front and n to the back of a permutation
 * of 1..n. */
long semiOrderedPermutation(long nums_len, const long nums[nums_len])
    requires(nums_len > 0)
    /* Consequence of the dropped equation between result and the positions of 1 and n. */
    ensures(0 <= result)
{
    long first = 0;
    long last = 0;

    if (nums_len == 0) {
        return 0;
    }
    for (long i = 0; i < nums_len; i++) invariant(0 <= i && i <= nums_len && 0 <= first && first < nums_len && 0 <= last && last < nums_len) decreases(nums_len - i) {
        if (nums[i] == 1) {
            first = i;
        }
        if (nums[i] == nums_len) {
            last = i;
        }
    }
    long swaps = first + (nums_len - 1 - last);

    if (first > last) {
        swaps--;
    }
    return swaps;
}
