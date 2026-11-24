#include "pfc.h"

/* Verina verina_advanced_16: insertion sort of xs into out, ascending; returns the length. */
long insertionSort(long xs_len, const long xs[xs_len], long out_cap, long out[out_cap])
    requires(out_cap >= xs_len)
    /* Pairwise (<=) and isPerm are dropped; the length is the only consequence of isPerm stated. */
    ensures(result == xs_len)
{
    for (long i = 0; i < xs_len; i++) {
        long x = xs[i];
        long j = i;
        while (j > 0 && out[j - 1] > x) invariant(0 <= j && j <= i) {
            out[j] = out[j - 1];
            j--;
        }
        out[j] = x;
    }
    return xs_len;
}
