#include "pfc.h"

/* Verina verina_advanced_56: the non-zero elements in their order, then the zeroes; returns the length. */
long moveZeroes(long xs_len, const long xs[xs_len], long out_cap, long out[out_cap])
    requires(out_cap >= xs_len)
{
    long k = 0;

    for (long i = 0; i < xs_len; i++) {
        if (xs[i] != 0) {
            out[k] = xs[i];
            k++;
        }
    }
    while (k < xs_len) {
        out[k] = 0;
        k++;
    }
    return xs_len;
}
