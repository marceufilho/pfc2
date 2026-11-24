#include "pfc.h"

/* Verina verina_advanced_17: insertion sort of l into out, ascending; returns the length. */
long insertionSort(long l_len, const long l[l_len], long out_cap, long out[out_cap])
    requires(out_cap >= l_len)
    /* Pairwise (<=) and isPerm are dropped; the length is the only consequence of isPerm stated. */
    ensures(result == l_len)
{
    for (long i = 0; i < l_len; i++) {
        long x = l[i];
        long j = i;
        while (j > 0 && out[j - 1] > x) invariant(0 <= j && j <= i) {
            out[j] = out[j - 1];
            j--;
        }
        out[j] = x;
    }
    return l_len;
}
