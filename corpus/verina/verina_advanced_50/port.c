#include "pfc.h"

/* Verina verina_advanced_50: merge two ascending arrays into one ascending array in out; returns its length. */
long mergeSorted(long a1_len, const long a1[a1_len], long a2_len, const long a2[a2_len], long out_cap, long out[out_cap])
    requires(0 <= a1_len)
    requires(0 <= a2_len)
    requires(out_cap >= a1_len + a2_len)
    /* Consequence of the dropped permutation: the result has every element of both inputs. */
    ensures(result == a1_len + a2_len)
{
    long i = 0;
    long j = 0;
    long k = 0;

    while (i < a1_len && j < a2_len) invariant(0 <= i && i <= a1_len && 0 <= j && j <= a2_len && k == i + j) {
        if (a1[i] <= a2[j]) {
            out[k] = a1[i];
            i++;
        } else {
            out[k] = a2[j];
            j++;
        }
        k++;
    }
    while (i < a1_len) invariant(0 <= i && i <= a1_len && 0 <= j && j <= a2_len && k == i + j) decreases(a1_len - i) {
        out[k] = a1[i];
        i++;
        k++;
    }
    while (j < a2_len) invariant(i == a1_len && 0 <= j && j <= a2_len && k == i + j) decreases(a2_len - j) {
        out[k] = a2[j];
        j++;
        k++;
    }
    return k;
}
