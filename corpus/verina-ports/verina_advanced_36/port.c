#include "pfc.h"

/* Verina verina_advanced_36: the element that appears more than half the time (one is assumed to exist), by
 * majority vote. */
long majorityElement(long xs_len, const long xs[xs_len])
{
    long candidate = 0;
    long count = 0;

    for (long i = 0; i < xs_len; i++) {
        if (count == 0) {
            candidate = xs[i];
            count = 1;
        } else if (xs[i] == candidate) {
            count++;
        } else {
            count--;
        }
    }
    return candidate;
}
