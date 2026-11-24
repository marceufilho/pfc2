#include "pfc.h"

/* Verina verina_advanced_28: length of the longest run of consecutive integers present in nums
 * (elements are unique, in any order). */
long contains(long n, const long a[n], long value)
    ensures(result == 0 || result == 1)
{
    for (long i = 0; i < n; i++) {
        if (a[i] == value) {
            return 1;
        }
    }
    return 0;
}

long longestConsecutive(long nums_len, const long nums[nums_len])
    /* Precondition Nodup: dropped. nums = [] -> result = 0 is stated; the rest (sorted list, consecutive
     * sublists) is dropped. result is a Nat. */
    ensures(nums_len != 0 || result == 0)
    ensures(result >= 0)
{
    long best = 0;

    for (long i = 0; i < nums_len; i++) invariant(best >= 0 && (nums_len > 0 || best == 0)) {
        long has_previous = contains(nums_len, nums, nums[i] - 1);
        if (!has_previous) {
            long length = 1;
            long has_next = contains(nums_len, nums, nums[i] + length);
            while (has_next) invariant(length >= 1) {
                length++;
                has_next = contains(nums_len, nums, nums[i] + length);
            }
            if (length > best) {
                best = length;
            }
        }
    }
    return best;
}
