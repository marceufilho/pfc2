#include "pfc.h"

/* Verina verina_advanced_29: length of the longest contiguous subarray in which no value occurs more than
 * k times. */
long longestGoodSubarray(long nums_len, const long nums[nums_len], long k)
    requires(nums_len >= 0) /* a length; this spelling of the parameter does not give the checker 0 <= nums_len */
    requires(k > 0)
    /* (nums = [] and result = 0) or (nums != [] and ...): the empty case is stated; the enumeration of
     * subarrays and their frequency counts is dropped. */
    ensures(nums_len != 0 || result == 0)
    ensures(0 <= result && result <= nums_len)
{
    long best = 0;

    for (long start = 0; start < nums_len; start++) invariant(0 <= best && best <= nums_len) {
        for (long end = start; end < nums_len; end++) invariant(start <= end && 0 <= best && best <= nums_len) {
            long count = 0;
            for (long i = start; i <= end; i++) invariant(start <= i && i <= end + 1 && 0 <= count && count <= i - start) {
                if (nums[i] == nums[end]) {
                    count++;
                }
            }
            if (count > k) {
                break;
            }
            if (end - start + 1 > best) {
                best = end - start + 1;
            }
        }
    }
    return best;
}
