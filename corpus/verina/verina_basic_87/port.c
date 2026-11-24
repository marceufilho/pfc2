#include "pfc.h"

/* Verina verina_basic_87: selection sort of a into out (non-decreasing); returns the length. */
long SelectionSort(long a_len, const long a[a_len], long out_cap, long out[out_cap])
    requires(out_cap >= a_len)
    ensures(result == a_len)
{
    for (long i = 0; i < a_len; i++) {
        out[i] = a[i];
    }
    for (long i = 0; i < a_len; i++) {
        long smallest = i;

        for (long j = i + 1; j < a_len; j++) invariant(i + 1 <= j && i <= smallest && smallest < a_len) {
            if (out[j] < out[smallest]) {
                smallest = j;
            }
        }
        long kept = out[i];

        out[i] = out[smallest];
        out[smallest] = kept;
    }
    return a_len;
}
