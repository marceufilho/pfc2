#include "pfc.h"

/* Verina verina_advanced_76: the k most frequent values of nums, from the most to the least frequent, written
 * to out; returns how many were written. */
long topKFrequent(long nums_len, const long nums[nums_len], long k, long out_cap, long out[out_cap])
    requires(out_cap >= k)
{
    long m = 0;

    while (m < k) {
        long best = 0;
        long best_count = 0;

        for (long i = 0; i < nums_len; i++) {
            long taken = 0;

            for (long t = 0; t < m; t++) {
                if (out[t] == nums[i]) {
                    taken = 1;
                    break;
                }
            }
            if (taken) {
                continue;
            }
            long count = 0;

            for (long j = 0; j < nums_len; j++) {
                if (nums[j] == nums[i]) {
                    count++;
                }
            }
            if (count > best_count) {
                best = nums[i];
                best_count = count;
            }
        }
        if (best_count == 0) {
            break;
        }
        out[m] = best;
        m++;
    }
    return m;
}
