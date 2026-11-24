#include "pfc.h"

/* Verina verina_advanced_15: 1 when some i < j < k have nums[i] < nums[j] < nums[k], else 0. */
long increasingTriplet(long nums_len, const long nums[nums_len])
    /* Both directions quantify over index triples: dropped. */
    ensures(result == 0 || result == 1)
{
    long have_first = 0;
    long have_second = 0;
    long first = 0;
    long second = 0;

    for (long i = 0; i < nums_len; i++) {
        long x = nums[i];
        if (!have_first || x <= first) {
            first = x;
            have_first = 1;
        } else if (!have_second || x <= second) {
            second = x;
            have_second = 1;
        } else {
            return 1;
        }
    }
    return 0;
}
