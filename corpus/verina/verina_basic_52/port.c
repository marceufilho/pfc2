#include "pfc.h"

/* Verina verina_basic_52: a sorted in non-decreasing order by bubble sort, written to out; returns the length. */
long BubbleSort(long a_len, const long a[a_len], long out_cap, long out[out_cap])
    requires(out_cap >= a_len)
{
    for (long i = 0; i < a_len; i++) {
        out[i] = a[i];
    }
    for (long i = 0; i < a_len; i++) {
        for (long j = 0; j + 1 < a_len - i; j++) invariant(0 <= j && j < a_len) {
            if (out[j] > out[j + 1]) {
                long tmp = out[j];

                out[j] = out[j + 1];
                out[j + 1] = tmp;
            }
        }
    }
    return a_len;
}
