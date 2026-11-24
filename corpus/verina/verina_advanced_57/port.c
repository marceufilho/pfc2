#include "pfc.h"

/* Verina verina_advanced_57: for each nums1[i], the first element greater than it to its right in nums2, or
 * -1; returns the length of nums1. */
long nextGreaterElement(long nums1_len, const long nums1[nums1_len], long nums2_len, const long nums2[nums2_len], long out_cap, long out[out_cap])
    requires(0 <= nums1_len)
    requires(0 <= nums2_len)
    requires(out_cap >= nums1_len)
    ensures(result == nums1_len)
{
    for (long i = 0; i < nums1_len; i++) invariant(0 <= i && i <= nums1_len) {
        long j = 0;

        while (j < nums2_len && nums2[j] != nums1[i]) invariant(0 <= j && j <= nums2_len) {
            j++;
        }
        out[i] = -1;
        for (long k = j + 1; k < nums2_len; k++) invariant(j + 1 <= k) {
            if (nums2[k] > nums1[i]) {
                out[i] = nums2[k];
                break;
            }
        }
    }
    return nums1_len;
}
