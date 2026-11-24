#include "pfc.h"

/* Verina verina_advanced_43: the largest product of a non-empty subset of nums. Multiply every non-zero
 * value; when the count of negatives is odd, leave out the negative closest to zero. */
long maxStrength(long nums_len, const long nums[nums_len])
    requires(nums_len > 0)
    /* The postcondition ranges over the products of all non-empty sublists: dropped. */
{
    long product = 1;
    long nonzero = 0;
    long negatives = 0;
    long zeros = 0;
    long closest_negative = 0;

    for (long i = 0; i < nums_len; i++) invariant(negatives >= 0 && (negatives == 0 || closest_negative < 0)) {
        long x = nums[i];
        if (x == 0) {
            zeros++;
        } else {
            product = product * x;
            nonzero++;
            if (x < 0) {
                if (negatives == 0 || x > closest_negative) {
                    closest_negative = x;
                }
                negatives++;
            }
        }
    }

    if (nonzero == 0) {
        return 0;
    }
    if (negatives % 2 == 1) {
        if (nonzero == 1) {
            if (zeros > 0) {
                return 0;
            }
            return product;
        }
        return product / closest_negative;
    }
    return product;
}
