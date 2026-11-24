#include "pfc.h"

/* Verina verina_basic_74: maximum element of a non-empty array. */
long maxArray(long a_len, const long a[a_len])
    requires(a_len >= 1)
{
    long best = a[0];

    for (long i = 1; i < a_len; i++) {
        if (a[i] > best) {
            best = a[i];
        }
    }
    return best;
}
