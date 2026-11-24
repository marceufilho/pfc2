#include "pfc.h"

/* Verina verina_advanced_51: merge two ascending arrays into one ascending array in out; returns its length. */
long mergeSorted(long a_len, const long a[a_len], long b_len, const long b[b_len], long out_cap, long out[out_cap])
    requires(0 <= a_len)
    requires(0 <= b_len)
    requires(out_cap >= a_len + b_len)
    /* Consequence of the dropped permutation: the result has every element of both inputs. */
    ensures(result == a_len + b_len)
{
    long i = 0;
    long j = 0;
    long k = 0;

    while (i < a_len && j < b_len) invariant(0 <= i && i <= a_len && 0 <= j && j <= b_len && k == i + j) {
        if (a[i] <= b[j]) {
            out[k] = a[i];
            i++;
        } else {
            out[k] = b[j];
            j++;
        }
        k++;
    }
    while (i < a_len) invariant(0 <= i && i <= a_len && 0 <= j && j <= b_len && k == i + j) decreases(a_len - i) {
        out[k] = a[i];
        i++;
        k++;
    }
    while (j < b_len) invariant(i == a_len && 0 <= j && j <= b_len && k == i + j) decreases(b_len - j) {
        out[k] = b[j];
        j++;
        k++;
    }
    return k;
}
