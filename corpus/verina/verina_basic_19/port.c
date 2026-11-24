#include "pfc.h"

/* Verina verina_basic_19: 1 when a is in non-decreasing order, else 0. */
long isSorted(long a_len, const long a[a_len])
    ensures(result == 0 || result == 1)
{
    for (long i = 0; i + 1 < a_len; i++) invariant(0 <= i && (i == 0 || i < a_len)) {
        if (a[i] > a[i + 1]) {
            return 0;
        }
    }
    return 1;
}
