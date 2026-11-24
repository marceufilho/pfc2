#include "pfc.h"

/* Verina verina_basic_54: minimum absolute difference between an element of a and an element of b, both sorted. */
long CanyonSearch(long a_len, const long a[a_len], long b_len, const long b[b_len])
    requires(a_len >= 1)
    requires(b_len >= 1)
    ensures(result >= 0)
{
    long i = 0;
    long j = 0;
    long best = a[0] - b[0];

    if (best < 0) {
        best = -best;
    }
    while (i < a_len && j < b_len) invariant(0 <= i && i <= a_len && 0 <= j && j <= b_len && best >= 0) {
        long diff = a[i] - b[j];

        if (diff < 0) {
            diff = -diff;
        }
        if (diff < best) {
            best = diff;
        }
        if (a[i] < b[j]) {
            i++;
        } else {
            j++;
        }
    }
    return best;
}
